# Personalized Travel Itinerary Planner

**Skill Wallet Capstone Project 4 — Generative AI | Intelligent SaaS Platform**

A full-stack, AI-powered Streamlit application that generates optimized day-by-day vacation itineraries, clusters attractions to eliminate travel fatigue, offers vibe-based destination recommendations, and produces exportable PDF travel guides.

---

## Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

The application runs fully in demo mode without an API key, using pre-built sample data.  
Add a Gemini API key to enable live AI-generated itineraries.

---

## Features

| Tab | Description |
|-----|-------------|
| Settings | Configure trip preferences — vibe, budget, pace, interests, travel style, and API key |
| Destinations | AI recommends the top 3 cities matching the traveler's profile |
| Itinerary | Day-by-day plan with geographic clustering and a running cost tracker |
| Activity Swap | Replace any individual slot without regenerating the full itinerary |
| Trip Manager | Save and load trips from a local SQLite database; export to PDF |

---

## Tech Stack

- **Framework:** Python 3.10+ / Streamlit
- **AI Model:** Google Gemini 1.5 Flash via `google-generativeai`
- **PDF Generation:** ReportLab
- **Database:** SQLite (built-in — no external database required)
- **Deployment:** Streamlit Community Cloud

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A Gemini API key (optional — app works without one in demo mode)

### Installation

```bash
git clone https://github.com/tani-shaa/travel-planner-ai.git
cd travel-planner-ai
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
```

Open `.env` and set your API key:

```
GEMINI_API_KEY=your_key_here
```

Get a free key at: https://aistudio.google.com/app/apikey

### Running the App

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Deployment — Streamlit Community Cloud

1. Push the repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select the repository, set branch to `main` or `master`, and set the main file path to `app.py`.
4. Under **Advanced settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   ```
5. Click **Deploy**.

---

## Project Structure

```
travel_planner/
├── app.py                      # Main Streamlit entry point
├── requirements.txt
├── .env.example
├── .streamlit/
│   └── config.toml             # Theme and server configuration
├── assets/
│   └── styles.css              # Custom CSS styling
├── pages/
│   ├── tab1_preferences.py     # Settings and user preferences
│   ├── tab2_destinations.py    # AI destination recommender
│   ├── tab3_itinerary.py       # Day-by-day itinerary generator
│   ├── tab4_swap.py            # Activity swap and customization
│   └── tab5_trips.py           # Trip manager and PDF export
└── utils/
    ├── config.py               # API key management and constants
    ├── gemini_client.py        # Gemini AI prompt layer
    ├── demo_data.py            # Structured demo data
    ├── database.py             # SQLite persistence layer
    └── pdf_export.py           # ReportLab PDF generator
```

---

## Notes

- The `.env` file is excluded from version control via `.gitignore`. Your API key is never committed.
- The SQLite database (`data/trips.db`) is also excluded — it is created locally on first run.
- For Streamlit Cloud deployment, add the API key through the Secrets interface rather than a `.env` file.

---

## License

Built for the Skill Wallet Capstone Program — Project 4: Generative AI SaaS Platform.
