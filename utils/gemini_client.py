"""
Gemini AI client wrapper.
All prompts and API calls live here.
Falls back to structured demo data when no API key is present.
"""

import json
import re
import google.generativeai as genai
from utils.config import get_gemini_api_key, is_demo_mode
from utils.demo_data import DEMO_DESTINATIONS, DEMO_ITINERARY, DEMO_ACTIVITY_SWAP


def _get_model():
    api_key = get_gemini_api_key()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def _safe_json(text: str):
    """Strip markdown fences and parse JSON from Gemini response."""
    cleaned = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
    # Sometimes Gemini adds trailing commas — remove them
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
    return json.loads(cleaned)


# ── Destination Recommender ────────────────────────────────────────────────────

def recommend_destinations(
    vibe: str,
    budget: str,
    duration: int,
    travel_style: str,
    interests: list,
    season: str,
) -> list:
    if is_demo_mode():
        return DEMO_DESTINATIONS

    model = _get_model()
    prompt = f"""
You are an expert travel consultant. Recommend the TOP 3 travel destinations for this traveler profile.

Traveler Profile:
- Vibe / Destination type: {vibe}
- Travel style: {travel_style}
- Budget level: {budget}
- Trip duration: {duration} days
- Interests: {", ".join(interests)}
- Travel season: {season}

Respond ONLY with a valid JSON array containing exactly 3 objects, each with:
- "city" (string)
- "country" (string)
- "highlight" (string — one iconic thing about the destination)
- "why" (string — 2-sentence reason it matches this traveler)
- "best_for" (string — comma-separated tags)
- "avg_daily_cost_usd" (integer)

No markdown, no extra text. JSON array only:
"""
    try:
        response = model.generate_content(prompt)
        return _safe_json(response.text)
    except Exception as e:
        return [{"city": "API Error", "country": "", "highlight": str(e),
                 "why": "Please check your API key.", "best_for": "", "avg_daily_cost_usd": 0}]


# ── Day-by-Day Itinerary Generator ────────────────────────────────────────────

def generate_itinerary(
    destination: str,
    duration: int,
    budget: str,
    pace: str,
    travel_style: str,
    interests: list,
    currency: str,
) -> dict:
    if is_demo_mode():
        demo = dict(DEMO_ITINERARY)
        demo["destination"] = destination
        return demo

    model = _get_model()
    slots_per_day = {"Relaxed": 4, "Moderate": 5, "Fast-Paced": 6}.get(pace, 5)

    prompt = f"""
You are a senior travel planner creating a detailed trip itinerary.

Trip Details:
- Destination: {destination}
- Duration: {duration} days
- Budget: {budget}
- Pace: {pace} ({slots_per_day} activities per day)
- Travel style: {travel_style}
- Interests: {", ".join(interests)}
- Currency for costs: {currency}

Rules:
1. Apply geographic clustering — group nearby attractions on the same day to minimise backtracking.
2. Time slots should be from: Morning, Lunch, Afternoon, Evening, Dinner (add Night for Fast-Paced).
3. Provide itemised costs and daily totals.
4. Avoid repeating the same area on consecutive days.

Respond ONLY with a valid JSON object (no markdown) with this exact structure:
{{
  "destination": "{destination}",
  "days": [
    {{
      "day": 1,
      "theme": "Arrival & Old Town",
      "slots": [
        {{
          "time_slot": "Morning",
          "activity": "activity name",
          "location": "specific place",
          "duration_hrs": 2.0,
          "cost_local": 0,
          "cost_usd": 0,
          "category": "Sightseeing",
          "tip": "practical tip"
        }}
      ],
      "daily_total_usd": 80
    }}
  ],
  "total_estimated_cost_usd": 400,
  "currency": "{currency}",
  "packing_tips": ["tip1", "tip2", "tip3", "tip4"],
  "emergency_contacts": {{
    "police": "number",
    "ambulance": "number",
    "tourist_helpline": "number or website"
  }}
}}
"""
    try:
        response = model.generate_content(prompt)
        return _safe_json(response.text)
    except Exception as e:
        return {"error": str(e), "destination": destination, "days": [],
                "total_estimated_cost_usd": 0, "currency": currency,
                "packing_tips": [], "emergency_contacts": {}}


# ── Activity Swap ─────────────────────────────────────────────────────────────

def swap_activity(
    destination: str,
    day: int,
    time_slot: str,
    current_activity: str,
    swap_reason: str,
    budget: str,
    interests: list,
) -> dict:
    if is_demo_mode():
        return DEMO_ACTIVITY_SWAP

    model = _get_model()
    prompt = f"""
A traveler wants to swap one activity from their itinerary.

Context:
- Destination: {destination}
- Day {day}, Time slot: {time_slot}
- Current activity: {current_activity}
- Reason for swap: {swap_reason}
- Budget: {budget}
- Interests: {", ".join(interests)}

Suggest ONE alternative activity. Respond ONLY with a valid JSON object (no markdown):
{{
  "activity": "name",
  "location": "specific place",
  "duration_hrs": 2.0,
  "cost_usd": 15,
  "category": "Food",
  "tip": "practical tip",
  "reason": "why this is a great swap"
}}
"""
    try:
        response = model.generate_content(prompt)
        return _safe_json(response.text)
    except Exception as e:
        return {"activity": "Error", "location": "", "duration_hrs": 0,
                "cost_usd": 0, "category": "", "tip": str(e), "reason": ""}
