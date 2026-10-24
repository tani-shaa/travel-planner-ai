"""
Tab 0 — Configuration & User Preferences
Collects API key + trip preferences and stores them in session state.
"""

import streamlit as st
from utils.config import (
    VIBES, TRAVEL_STYLES, PACES, INTERESTS,
    BUDGET_LEVELS, CURRENCIES, DURATIONS, SEASONS,
    is_demo_mode, get_gemini_api_key,
)


def render():
    st.markdown("## ⚙️ Trip Preferences")
    st.markdown("Fill in your travel profile below. Your preferences are used across all tabs.")

    # ── API key ───────────────────────────────────────────────────────────────
    with st.expander("🔑 Gemini API Key", expanded=is_demo_mode()):
        api_input = st.text_input(
            "Paste your Gemini API key here (optional — demo mode works without it)",
            value=st.session_state.get("api_key_input", ""),
            type="password",
            key="api_key_input",
        )
        if api_input:
            import os
            os.environ["GEMINI_API_KEY"] = api_input
            st.success("✅ API key set for this session.")
        else:
            if is_demo_mode():
                st.info("🎮 **Demo Mode** — running with pre-built sample data. Add your Gemini API key above to get live AI-generated results.", icon="ℹ️")
            else:
                st.success("✅ API key loaded from environment.")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✈️ Destination & Vibe")
        vibe = st.selectbox(
            "Trip Vibe / Destination Type",
            VIBES,
            index=VIBES.index(st.session_state.get("vibe", VIBES[0])),
            key="vibe",
        )
        travel_style = st.selectbox(
            "Who are you travelling with?",
            TRAVEL_STYLES,
            index=TRAVEL_STYLES.index(st.session_state.get("travel_style", TRAVEL_STYLES[0])),
            key="travel_style",
        )
        duration = st.select_slider(
            "Trip Duration (days)",
            options=DURATIONS,
            value=st.session_state.get("duration", 5),
            key="duration",
        )
        season = st.selectbox(
            "Travel Season",
            SEASONS,
            index=SEASONS.index(st.session_state.get("season", SEASONS[0])),
            key="season",
        )

    with col2:
        st.markdown("### 💰 Budget & Pace")
        budget = st.radio(
            "Budget Level",
            BUDGET_LEVELS,
            index=BUDGET_LEVELS.index(st.session_state.get("budget", BUDGET_LEVELS[1])),
            horizontal=True,
            key="budget",
        )
        pace = st.radio(
            "Trip Pace",
            PACES,
            index=PACES.index(st.session_state.get("pace", PACES[1])),
            horizontal=True,
            key="pace",
        )
        currency = st.selectbox(
            "Display Currency",
            CURRENCIES,
            index=CURRENCIES.index(st.session_state.get("currency", CURRENCIES[0])),
            key="currency",
        )
        interests = st.multiselect(
            "Your Interests",
            INTERESTS,
            default=st.session_state.get("interests", ["Food", "History"]),
            key="interests",
        )

    st.divider()

    # ── Optional: fixed destination override ──────────────────────────────────
    st.markdown("### 🗺️ Already have a destination in mind?")
    st.caption("Leave blank to get AI recommendations in Tab 1.")
    fixed_dest = st.text_input(
        "Fixed destination (city, country)",
        value=st.session_state.get("fixed_destination", ""),
        placeholder="e.g. Tokyo, Japan",
        key="fixed_destination",
    )

    st.divider()
    st.success("✅ Preferences saved! Head to **Tab 1** to get destination recommendations, or jump straight to **Tab 2** if you already have a destination.")

    # Summary card
    if interests:
        st.markdown("#### 📋 Your Profile Summary")
        cols = st.columns(4)
        cols[0].metric("Vibe", vibe)
        cols[1].metric("Duration", f"{duration} days")
        cols[2].metric("Budget", budget)
        cols[3].metric("Pace", pace)
        st.markdown(f"**Interests:** {', '.join(interests)}")
        st.markdown(f"**Travel style:** {travel_style}  |  **Season:** {season}")
