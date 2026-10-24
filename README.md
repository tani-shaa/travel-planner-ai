# ✈️ Personalized Travel Itinerary Planner
### Skill Wallet Capstone Project 4 — Generative AI · Intelligent SaaS Platform

> A full-stack, AI-powered Streamlit application that generates optimized day-by-day vacation itineraries, clusters attractions to eliminate travel fatigue, offers vibe-based destination recommendations, and produces exportable PDF travel guides.

---

## 🚀 Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

> **Demo Mode** — The app runs fully without an API key using pre-built Lisbon sample data.  
> Add your Gemini API key to unlock live AI-generated itineraries.

---

## 📸 Features

| Tab | Feature |
|-----|---------|
| ⚙️ Settings | Trip preferences, API key config, vibe/budget/pace/interests |
| 🌍 Destinations | AI recommends Top 3 cities matching your profile |
| 🗓️ Itinerary | Day-by-day plan with geographic clustering & running cost tracker |
| 🔄 Activity Swap | Replace any slot without regenerating the whole trip |
| 💾 Trip Manager | Save/load trips from SQLite, 1-click PDF export |

---

## 🛠️ Tech Stack

- **Frontend/Backend:** Python 3.10+ · Streamlit
- **AI:** Google Gemini 1.5 Flash (`google-generativeai`)
- **PDF:** ReportLab
- **Database:** SQLite (built-in — zero external DB dependencies)
- **Deployment:** Streamlit Community Cloud

---

## ⚡ Quick Start (Local)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/travel-planner-ai.git
cd travel-planner-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key (optional)
```bash
cp .env.example .env
# Edit .env and add: GEMINI_API_KEY=your_key_here
```
Get a free key at: https://aistudio.google.com/app/apikey

### 4. Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## ☁️ Deploy to Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo, branch `main`, and set **Main file path** to `app.py`
4. Under **Advanced settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```
5. Click **Deploy** — done!

---

## 📁 Project Structure

```
travel_planner/
├── app.py                      # Main Streamlit entry point
├── requirements.txt
├── .env.example
├── .streamlit/
│   └── config.toml             # Theme + server config
├── assets/
│   └── styles.css              # Wanderlust-inspired SaaS CSS
├── pages/
│   ├── tab1_preferences.py     # ⚙️  Settings & preferences
│   ├── tab2_destinations.py    # 🌍  AI Destination Recommender
│   ├── tab3_itinerary.py       # 🗓️  Day-by-Day Itinerary Generator
│   ├── tab4_swap.py            # 🔄  Activity Swap & Customization
│   └── tab5_trips.py           # 💾  Trip Manager & PDF Export
└── utils/
    ├── config.py               # API key + preference constants
    ├── gemini_client.py        # All Gemini AI prompts
    ├── demo_data.py            # Full demo data (Lisbon 3-day trip)
    ├── database.py             # SQLite persistence layer
    └── pdf_export.py           # ReportLab PDF generator
```

---

## 🔑 Gemini API Key

- Free tier available at [Google AI Studio](https://aistudio.google.com/app/apikey)
- The app works **fully in demo mode** without any key
- Key is stored locally in `.env` or Streamlit secrets — never transmitted anywhere

---

## 📄 License

Built for the Skill Wallet Capstone Program · Project 4 — Generative AI SaaS Platform
