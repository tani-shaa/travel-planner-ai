"""
Configuration and API key management.
Supports both .env file and Streamlit secrets for cloud deployment.
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_gemini_api_key() -> str:
    """Retrieve Gemini API key from env or Streamlit secrets."""
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        pass
    return os.getenv("GEMINI_API_KEY", "")


def is_demo_mode() -> bool:
    """Return True if no API key is configured — demo/stub mode."""
    return get_gemini_api_key() == ""


# ── Trip preference constants ──────────────────────────────────────────────────

VIBES = ["Beach", "Mountains", "Cultural", "Urban", "Adventure", "Wellness"]
TRAVEL_STYLES = ["Solo", "Couple", "Family", "Friends", "Group"]
PACES = ["Relaxed", "Moderate", "Fast-Paced"]
INTERESTS = ["Food", "Adventure", "History", "Nightlife", "Nature", "Art & Museums", "Shopping"]
BUDGET_LEVELS = ["Budget", "Mid-Range", "Luxury"]
CURRENCIES = ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD", "SGD"]
DURATIONS = list(range(2, 15))
SEASONS = ["Spring (Mar–May)", "Summer (Jun–Aug)", "Autumn (Sep–Nov)", "Winter (Dec–Feb)"]
