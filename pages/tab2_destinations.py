"""
Tab 1 — Smart Destination Recommender
Recommends top 3 destinations based on the traveler's profile.
"""

import streamlit as st
from utils.gemini_client import recommend_destinations
from utils.config import is_demo_mode


def render():
    st.markdown("## 🌍 Smart Destination Recommender")
    st.markdown("Based on your travel profile, our AI suggests the best matching destinations.")

    # Check if a fixed destination was already provided
    fixed = st.session_state.get("fixed_destination", "").strip()
    if fixed:
        st.info(f"📌 You already have a fixed destination: **{fixed}**. Head to Tab 2 to build your itinerary, or clear it in Settings to use the recommender.")
        if st.button("🗑️ Clear fixed destination"):
            st.session_state["fixed_destination"] = ""
            st.rerun()
        return

    if is_demo_mode():
        st.warning("🎮 **Demo Mode** — showing sample recommendations. Add a Gemini API key in Settings for live AI results.", icon="ℹ️")

    # Show profile summary
    vibe         = st.session_state.get("vibe", "Beach")
    travel_style = st.session_state.get("travel_style", "Solo")
    budget       = st.session_state.get("budget", "Mid-Range")
    duration     = st.session_state.get("duration", 5)
    interests    = st.session_state.get("interests", ["Food", "History"])
    season       = st.session_state.get("season", "Spring (Mar–May)")

    with st.expander("📋 Current Travel Profile", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Vibe", vibe)
        c2.metric("Duration", f"{duration}d")
        c3.metric("Budget", budget)
        c4.metric("Pace", st.session_state.get("pace", "Moderate"))
        st.markdown(f"**Interests:** {', '.join(interests) if interests else 'None selected'}  |  **Season:** {season}")

    st.divider()

    if st.button("🔍 Get AI Destination Recommendations", type="primary", use_container_width=True):
        if not interests:
            st.warning("Please select at least one interest in the Settings tab.")
            return
        with st.spinner("✨ Finding your perfect destinations..."):
            recs = recommend_destinations(
                vibe=vibe,
                budget=budget,
                duration=duration,
                travel_style=travel_style,
                interests=interests,
                season=season,
            )
            st.session_state["recommendations"] = recs

    recs = st.session_state.get("recommendations", [])
    if not recs:
        st.markdown("""
        <div style="text-align:center; padding: 3rem 0; color: #94a3b8;">
            <div style="font-size: 3rem;">🗺️</div>
            <p>Click the button above to discover your ideal destinations.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("### 🏆 Top 3 Recommended Destinations")

    for i, dest in enumerate(recs):
        city    = dest.get("city", "Unknown")
        country = dest.get("country", "")
        highlight = dest.get("highlight", "")
        why     = dest.get("why", "")
        best    = dest.get("best_for", "")
        cost    = dest.get("avg_daily_cost_usd", 0)

        medal = ["🥇", "🥈", "🥉"][i] if i < 3 else "📍"

        with st.container():
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f0fdfa, #ecfdf5);
                        border: 1px solid #a7f3d0; border-radius: 12px;
                        padding: 1.2rem 1.5rem; margin-bottom: 1rem;">
                <h3 style="margin:0; color:#0f766e;">{medal} {city}, {country}</h3>
                <p style="margin: 0.4rem 0 0.2rem; font-style: italic; color: #475569;">
                    ✨ {highlight}
                </p>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns([3, 2, 1])
            with c1:
                st.markdown(f"**Why it matches you:** {why}")
                st.markdown(f"🏷️ **Best for:** {best}")
            with c2:
                st.metric("Est. Daily Cost", f"${cost} USD")
                st.metric("Recommended Duration", f"{duration} days")
            with c3:
                full_dest = f"{city}, {country}"
                if st.button(f"🗓️ Plan this trip", key=f"plan_{i}", use_container_width=True):
                    st.session_state["selected_destination"] = full_dest
                    st.session_state["fixed_destination"] = full_dest
                    st.success(f"✅ Selected **{full_dest}**! Go to Tab 2 to build your itinerary.")

        st.divider()
