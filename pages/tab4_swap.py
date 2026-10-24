"""
Tab 3 — Vibe Customization & Dynamic Activity Swap
Interactive controls to modify specific slots and regenerate single days.
"""

import streamlit as st
from utils.gemini_client import swap_activity
from utils.config import is_demo_mode

TIME_EMOJI = {
    "Morning":   "🌅",
    "Lunch":     "🍽️",
    "Afternoon": "☀️",
    "Evening":   "🌆",
    "Dinner":    "🍷",
    "Night":     "🌙",
}

SWAP_REASONS = [
    "Too expensive",
    "Not interested in this activity",
    "Looking for something outdoors",
    "Want vegetarian / vegan options",
    "Swap museum for outdoor market",
    "Find something more family-friendly",
    "Looking for nightlife",
    "Want something free / budget",
    "Need something closer by",
    "Custom reason (type below)",
]


def render():
    st.markdown("## 🔄 Activity Swap & Vibe Customization")
    st.markdown("Swap any individual activity slot without rebuilding your entire itinerary.")

    itinerary = st.session_state.get("itinerary")
    if not itinerary or not itinerary.get("days"):
        st.warning("⚠️ No itinerary loaded yet. Go to **Tab 2** to generate one first.")
        return

    if is_demo_mode():
        st.warning("🎮 **Demo Mode** — swap suggestions use sample data. Add a Gemini API key for live results.", icon="ℹ️")

    destination = itinerary.get("destination", st.session_state.get("fixed_destination", ""))
    days        = itinerary.get("days", [])
    budget      = st.session_state.get("budget", "Mid-Range")
    interests   = st.session_state.get("interests", ["Food", "History"])

    st.markdown("---")
    st.markdown("### 🎯 Select an Activity to Swap")

    # Step 1 — pick day
    day_options = {f"Day {d['day']} — {d.get('theme','')}": d for d in days}
    selected_day_label = st.selectbox("Choose a day:", list(day_options.keys()))
    selected_day_data  = day_options[selected_day_label]
    day_num            = selected_day_data.get("day", 1)
    slots              = selected_day_data.get("slots", [])

    # Step 2 — pick slot
    slot_options = {
        f"{TIME_EMOJI.get(s.get('time_slot',''), '•')} {s.get('time_slot','')} — {s.get('activity','')}": s
        for s in slots
    }
    selected_slot_label = st.selectbox("Choose a time slot to swap:", list(slot_options.keys()))
    selected_slot       = slot_options[selected_slot_label]

    time_slot        = selected_slot.get("time_slot", "")
    current_activity = selected_slot.get("activity", "")
    current_location = selected_slot.get("location", "")
    current_cost     = selected_slot.get("cost_usd", 0)
    current_cat      = selected_slot.get("category", "")

    # Show current slot card
    st.markdown(f"""
    <div style="background:#fef9c3; border:1px solid #fde68a; border-radius:10px;
                padding:0.9rem 1.2rem; margin:0.5rem 0;">
        <div style="font-size:0.8rem; color:#92400e; font-weight:600; margin-bottom:0.3rem;">
            CURRENT ACTIVITY — {time_slot}
        </div>
        <div style="font-size:1rem; font-weight:700; color:#0f172a;">{current_activity}</div>
        <div style="font-size:0.85rem; color:#475569; margin-top:0.2rem;">
            📍 {current_location} &nbsp;|&nbsp; 💰 ${current_cost} USD &nbsp;|&nbsp; 🏷️ {current_cat}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Step 3 — reason
    st.markdown("### 💬 Why do you want to swap?")
    reason_choice = st.selectbox("Select a reason:", SWAP_REASONS)
    custom_reason = ""
    if reason_choice == "Custom reason (type below)":
        custom_reason = st.text_input("Describe what you're looking for:")
    final_reason = custom_reason if reason_choice == "Custom reason (type below)" else reason_choice

    # Swap button
    if st.button("🔄 Find Alternative Activity", type="primary", use_container_width=True):
        if not final_reason:
            st.warning("Please select or type a reason.")
            return
        with st.spinner("🤖 Finding the perfect alternative..."):
            suggestion = swap_activity(
                destination=destination,
                day=day_num,
                time_slot=time_slot,
                current_activity=current_activity,
                swap_reason=final_reason,
                budget=budget,
                interests=interests,
            )
            st.session_state["swap_suggestion"]   = suggestion
            st.session_state["swap_day_num"]      = day_num
            st.session_state["swap_slot_label"]   = selected_slot_label
            st.session_state["swap_target_slot"]  = selected_slot

    suggestion = st.session_state.get("swap_suggestion")
    if not suggestion:
        return

    st.markdown("---")
    st.markdown("### ✨ Suggested Alternative")

    new_act  = suggestion.get("activity", "")
    new_loc  = suggestion.get("location", "")
    new_dur  = suggestion.get("duration_hrs", 0)
    new_cost = suggestion.get("cost_usd", 0)
    new_cat  = suggestion.get("category", "")
    new_tip  = suggestion.get("tip", "")
    new_why  = suggestion.get("reason", "")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#f0fdfa,#ecfdf5);
                border:2px solid #6ee7b7; border-radius:12px;
                padding:1rem 1.4rem; margin:0.5rem 0;">
        <div style="font-size:0.8rem; color:#065f46; font-weight:700;
                    text-transform:uppercase; margin-bottom:0.4rem;">
            ✅ Recommended Swap
        </div>
        <div style="font-size:1.1rem; font-weight:700; color:#0f172a;">{new_act}</div>
        <div style="font-size:0.85rem; color:#475569; margin-top:0.3rem;">
            📍 {new_loc} &nbsp;|&nbsp; ⏱ {new_dur}h &nbsp;|&nbsp; 💰 ${new_cost} USD &nbsp;|&nbsp; 🏷️ {new_cat}
        </div>
        {"<div style='background:#f0fdf4; border-left:3px solid #22c55e; padding:0.35rem 0.6rem; margin-top:0.5rem; border-radius:4px; font-size:0.82rem; color:#166534;'>💡 " + new_tip + "</div>" if new_tip else ""}
        <div style="font-size:0.85rem; color:#0f766e; margin-top:0.5rem; font-style:italic;">
            🎯 {new_why}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_accept, col_reject = st.columns(2)

    with col_accept:
        if st.button("✅ Accept Swap — Update Itinerary", type="primary", use_container_width=True):
            # Apply swap to itinerary in session state
            target_slot = st.session_state.get("swap_target_slot", {})
            swap_day    = st.session_state.get("swap_day_num", 1)

            updated_days = []
            for d in days:
                if d.get("day") == swap_day:
                    new_slots = []
                    for s in d.get("slots", []):
                        if s.get("activity") == target_slot.get("activity") and \
                           s.get("time_slot") == target_slot.get("time_slot"):
                            # Replace with suggestion
                            new_slots.append({
                                "time_slot":   time_slot,
                                "activity":    new_act,
                                "location":    new_loc,
                                "duration_hrs": new_dur,
                                "cost_local":  new_cost,
                                "cost_usd":    new_cost,
                                "category":    new_cat,
                                "tip":         new_tip,
                            })
                        else:
                            new_slots.append(s)
                    d = dict(d)
                    d["slots"] = new_slots
                updated_days.append(d)

            updated_itinerary = dict(itinerary)
            updated_itinerary["days"] = updated_days
            st.session_state["itinerary"] = updated_itinerary
            st.session_state.pop("swap_suggestion", None)
            st.success(f"✅ Swap applied! **{new_act}** is now in your Day {swap_day} itinerary.")
            st.rerun()

    with col_reject:
        if st.button("❌ Keep Original Activity", use_container_width=True):
            st.session_state.pop("swap_suggestion", None)
            st.info("Original activity kept.")
            st.rerun()
