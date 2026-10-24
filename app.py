"""
Personalized Travel Itinerary Planner
Full-stack Streamlit SaaS — Skill Wallet Capstone Project 4
Powered by Google Gemini AI
"""

import streamlit as st
import os
from pathlib import Path

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Travel Planner AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load custom CSS ────────────────────────────────────────────────────────────
css_path = Path(__file__).parent / "assets" / "styles.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Import page renderers ──────────────────────────────────────────────────────
from pages.tab1_preferences import render as render_preferences
from pages.tab2_destinations import render as render_destinations
from pages.tab3_itinerary    import render as render_itinerary
from pages.tab4_swap         import render as render_swap
from pages.tab5_trips        import render as render_trips

# ── Initialise session state defaults ─────────────────────────────────────────
DEFAULTS = {
    "vibe":                "Beach",
    "travel_style":        "Solo",
    "duration":            5,
    "season":              "Spring (Mar–May)",
    "budget":              "Mid-Range",
    "pace":                "Moderate",
    "currency":            "USD",
    "interests":           ["Food", "History"],
    "fixed_destination":   "",
    "selected_destination":"",
    "recommendations":     [],
    "itinerary":           None,
    "swap_suggestion":     None,
}
for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 1rem;">
        <div style="font-size: 2.8rem;">✈️</div>
        <h2 style="margin:0; font-size:1.2rem; font-weight:700; color:#CCFBF1;">
            Travel Planner AI
        </h2>
        <p style="font-size:0.75rem; color:#94a3b8; margin:0.2rem 0 0;">
            Powered by Gemini · Capstone Project 4
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Quick-glance current trip info
    dest = (st.session_state.get("fixed_destination") or
            st.session_state.get("selected_destination") or "Not set")
    dur  = st.session_state.get("duration", 5)
    bdg  = st.session_state.get("budget", "Mid-Range")
    pac  = st.session_state.get("pace", "Moderate")

    st.markdown("**📍 Current Trip**")
    st.markdown(f"- **Destination:** {dest}")
    st.markdown(f"- **Duration:** {dur} days")
    st.markdown(f"- **Budget:** {bdg}  |  **Pace:** {pac}")

    itinerary = st.session_state.get("itinerary")
    if itinerary and itinerary.get("days"):
        total = itinerary.get("total_estimated_cost_usd", 0)
        days  = len(itinerary["days"])
        st.markdown(f"- **Itinerary:** {days} days loaded")
        st.markdown(f"- **Est. Cost:** ${total:,} USD")
    else:
        st.markdown("- *No itinerary generated yet*")

    st.divider()

    # Demo mode indicator
    from utils.config import is_demo_mode
    if is_demo_mode():
        st.markdown("""
        <div style="background:#1e3a5f; border:1px solid #3b82f6; border-radius:8px;
                    padding:0.6rem 0.8rem; font-size:0.8rem; color:#93c5fd;">
            🎮 <b>Demo Mode</b><br>
            Add your Gemini API key in Settings for live AI results.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#14532d; border:1px solid #22c55e; border-radius:8px;
                    padding:0.6rem 0.8rem; font-size:0.8rem; color:#86efac;">
            ✅ <b>Live Mode</b><br>Gemini API key active.
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style="font-size:0.72rem; color:#64748b; text-align:center;">
        🔒 Your API key stays local.<br>
        No data sent to third parties.<br><br>
        Built with Streamlit + Gemini AI<br>
        © 2026 Skill Wallet Capstone
    </div>
    """, unsafe_allow_html=True)

# ── Hero header ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg, #0F172A 0%, #134e4a 50%, #0D9488 100%);
            border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 1.5rem;
            position: relative; overflow: hidden;">
    <div style="position:absolute; top:-20px; right:-20px; font-size:8rem;
                opacity:0.06; pointer-events:none;">✈️</div>
    <h1 style="margin:0; font-size:2rem; font-weight:800; color:white;
               font-family:'Playfair Display', serif; letter-spacing:-0.01em;">
        ✈️ Personalized Travel Itinerary Planner
    </h1>
    <p style="margin:0.5rem 0 0; color:#99f6e4; font-size:1rem; font-weight:400;">
        AI-powered day-by-day itineraries · Smart destination matching · 
        Vibe-based recommendations · 1-click PDF export
    </p>
</div>
""", unsafe_allow_html=True)

# ── Tab layout ─────────────────────────────────────────────────────────────────
tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "⚙️ Settings",
    "🌍 Destinations",
    "🗓️ Itinerary",
    "🔄 Activity Swap",
    "💾 Trip Manager",
])

with tab0:
    render_preferences()

with tab1:
    render_destinations()

with tab2:
    render_itinerary()

with tab3:
    render_swap()

with tab4:
    render_trips()
