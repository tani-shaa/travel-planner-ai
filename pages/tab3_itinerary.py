"""
Tab 2 — Day-by-Day Optimized Itinerary Generator
Generates structured day-by-day plans with geographic clustering and cost tracking.
"""

import streamlit as st
from utils.gemini_client import generate_itinerary
from utils.config import is_demo_mode

TIME_EMOJI = {
    "Morning":   "🌅",
    "Lunch":     "🍽️",
    "Afternoon": "☀️",
    "Evening":   "🌆",
    "Dinner":    "🍷",
    "Night":     "🌙",
}

CATEGORY_COLORS = {
    "Sightseeing":          "#3B82F6",
    "Food":                 "#F59E0B",
    "Food & Sightseeing":   "#F59E0B",
    "Adventure":            "#10B981",
    "Entertainment":        "#8B5CF6",
    "Culture & Art":        "#EC4899",
    "Nightlife":            "#6366F1",
    "Shopping":             "#F97316",
    "Nature":               "#22C55E",
}
DEFAULT_CAT_COLOR = "#64748B"


def render():
    st.markdown("## 🗓️ Day-by-Day Itinerary Generator")

    # Determine destination
    destination = (
        st.session_state.get("fixed_destination", "").strip()
        or st.session_state.get("selected_destination", "").strip()
    )

    if not destination:
        st.warning("👈 Please select a destination first — go to **Tab 1** for AI recommendations, or set one in **Settings**.")
        dest_override = st.text_input("Or type a destination directly:")
        if dest_override:
            st.session_state["fixed_destination"] = dest_override
            destination = dest_override
        if not destination:
            return

    duration     = st.session_state.get("duration", 5)
    budget       = st.session_state.get("budget", "Mid-Range")
    pace         = st.session_state.get("pace", "Moderate")
    travel_style = st.session_state.get("travel_style", "Solo")
    interests    = st.session_state.get("interests", ["Food", "History"])
    currency     = st.session_state.get("currency", "USD")

    if is_demo_mode():
        st.warning("🎮 **Demo Mode** — showing sample itinerary. Add a Gemini API key in Settings for live AI results.", icon="ℹ️")

    # Summary bar
    st.markdown(f"""
    <div style="background:linear-gradient(90deg,#0D9488,#0f766e);
                border-radius:10px; padding:0.8rem 1.2rem; color:white;
                display:flex; gap:2rem; flex-wrap:wrap; margin-bottom:0.5rem;">
        <span>📍 <b>{destination}</b></span>
        <span>📅 <b>{duration} days</b></span>
        <span>💰 <b>{budget}</b></span>
        <span>⚡ <b>{pace}</b></span>
        <span>🌍 <b>{travel_style}</b></span>
        <span>💱 <b>{currency}</b></span>
    </div>
    """, unsafe_allow_html=True)

    gen_col, _ = st.columns([2, 3])
    with gen_col:
        generate_btn = st.button("✨ Generate My Itinerary", type="primary", use_container_width=True)

    if generate_btn:
        with st.spinner(f"🤖 Building your {duration}-day {destination} adventure..."):
            itinerary = generate_itinerary(
                destination=destination,
                duration=duration,
                budget=budget,
                pace=pace,
                travel_style=travel_style,
                interests=interests,
                currency=currency,
            )
            st.session_state["itinerary"] = itinerary
            st.session_state["itinerary_destination"] = destination

    itinerary = st.session_state.get("itinerary")
    if not itinerary:
        st.markdown("""
        <div style="text-align:center; padding:3rem; color:#94a3b8;">
            <div style="font-size:3rem;">🗓️</div>
            <p>Click <b>Generate My Itinerary</b> to build your personalised day-by-day plan.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    if "error" in itinerary:
        st.error(f"Generation failed: {itinerary['error']}")
        return

    days       = itinerary.get("days", [])
    total_cost = itinerary.get("total_estimated_cost_usd", 0)
    curr       = itinerary.get("currency", currency)

    # Top stats
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📅 Days Planned", len(days))
    m2.metric("💰 Est. Total Cost", f"${total_cost:,} USD")
    m3.metric("📍 Destination", itinerary.get("destination", destination))
    m4.metric("💱 Currency", curr)
    st.markdown("---")

    # View mode
    view_mode = st.radio("View mode:", ["All Days", "Single Day"], horizontal=True)
    day_options = [f"Day {d['day']} — {d.get('theme','')}" for d in days]

    if view_mode == "Single Day" and day_options:
        selected_label = st.selectbox("Select a day:", day_options)
        selected_idx   = day_options.index(selected_label)
        days_to_show   = [days[selected_idx]]
    else:
        days_to_show = days

    # Render each day
    for day_data in days_to_show:
        day_num   = day_data.get("day", "?")
        theme     = day_data.get("theme", "")
        daily_tot = day_data.get("daily_total_usd", 0)
        slots     = day_data.get("slots", [])

        st.markdown(f"""
        <div style="background:linear-gradient(90deg,#0D9488,#0f766e);
                    border-radius:10px; padding:0.75rem 1.2rem; margin:1rem 0 0.5rem;
                    display:flex; justify-content:space-between; align-items:center; color:white;">
            <span style="font-size:1.1rem; font-weight:700;">📅 Day {day_num} — {theme}</span>
            <span style="font-weight:600; font-size:0.95rem;">Daily est. 💰 ${daily_tot} USD</span>
        </div>
        """, unsafe_allow_html=True)

        running = 0
        for slot in slots:
            ts       = slot.get("time_slot", "")
            activity = slot.get("activity", "")
            location = slot.get("location", "")
            dur      = slot.get("duration_hrs", 0)
            cost     = slot.get("cost_usd", 0)
            category = slot.get("category", "")
            tip      = slot.get("tip", "")
            running += cost
            emoji    = TIME_EMOJI.get(ts, "•")
            cat_col  = CATEGORY_COLORS.get(category, DEFAULT_CAT_COLOR)

            tip_html = f'<div style="background:#f0fdf4; border-left:3px solid #22c55e; padding:0.35rem 0.6rem; margin-top:0.4rem; border-radius:4px; font-size:0.82rem; color:#166534;">💡 {tip}</div>' if tip else ""

            st.markdown(f"""
            <div style="background:#f8fafc; border:1px solid #e2e8f0;
                        border-left:4px solid {cat_col};
                        border-radius:8px; padding:0.75rem 1rem; margin:0.25rem 0;">
                <div style="font-size:0.78rem; color:#64748b; font-weight:600; margin-bottom:0.2rem;">
                    {emoji}&nbsp; {ts}
                    &nbsp;&nbsp;
                    <span style="background:{cat_col}; color:white; font-size:0.68rem;
                                 padding:1px 8px; border-radius:999px; font-weight:600;">{category}</span>
                </div>
                <div style="font-size:1rem; font-weight:700; color:#0f172a; margin-bottom:0.2rem;">{activity}</div>
                <div style="font-size:0.85rem; color:#475569;">
                    📍 {location} &nbsp;|&nbsp; ⏱ {dur}h &nbsp;|&nbsp; 💰 ${cost} USD
                    &nbsp;&nbsp;
                    <span style="font-size:0.78rem; color:#94a3b8;">(running: ${running} USD)</span>
                </div>
                {tip_html}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

    # Packing & Emergency info
    packing   = itinerary.get("packing_tips", [])
    emergency = itinerary.get("emergency_contacts", {})

    if packing or emergency:
        st.markdown("---")
        info_col1, info_col2 = st.columns(2)

        if packing:
            with info_col1:
                st.markdown("#### 🎒 Packing Checklist")
                for tip in packing:
                    st.markdown(f"- {tip}")

        if emergency:
            with info_col2:
                st.markdown("#### 🚨 Emergency Contacts")
                for k, v in emergency.items():
                    st.markdown(f"**{k.replace('_',' ').title()}:** {v}")

    st.markdown("---")
    st.info("👉 Head to **Tab 3 — Activity Swap** to customise individual slots, or **Tab 4 — Trip Manager** to save and export this itinerary.")
