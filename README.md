AI Basketball Scout
===================

A two-part application that generates NBA scouting reports and visualizes player performance across seasons.

Features
--------
- Search and select players; fetch headshots
- Generate structured scouting reports with sections: Overview, Strengths, Weaknesses, Playstyle and Tendencies, Scheme Fit
- Combined performance chart (PPG, APG, RPG, SPG, BPG) with readable dark theme
- FastAPI backend serving player data and report generation endpoints
- Streamlit frontend for an interactive UI

Tech Stack
---------
- Backend: FastAPI, Uvicorn, Python
- Frontend: Streamlit
- Database: PostgreSQL
- Cache: Redis
- Data: CSVs from Basketball Reference (2020–2025)
- Visualization: Matplotlib
- HTTP/Utils: requests, python-dotenv
- Media: Pillow (for headshots)
- LLM Integration: Google Gemini (via `app/gemini.py`)
- Data Processing: Pandas
- Scraping: Beautiful Soup (bs4)

Project Structure
-----------------
- `app/`: FastAPI backend (API, models, scraping, Gemini integration)
- `frontend/streamlit_app.py`: Streamlit UI
- `data/`: CSVs sourced from Basketball Reference (2020–2025)

Prerequisites
-------------
- Python 3.10+
- Virtual environment recommended

Environment Variables
---------------------
Create a `.env` in both project root and `frontend/` if needed.

Required variables:
- Backend
  - `GEMINI_API_KEY` (if using Gemini for report generation)
  - `DATABASE_URL` (e.g., `postgresql+psycopg2://user:pass@localhost:5432/ai_basketball_scout`)
  - `REDIS_URL` (e.g., `redis://localhost:6379/0`)
- Frontend
  - `BACKEND_URL` (e.g., `http://localhost:8000`)

Install
-------
From the project root:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt  # If present
```

Run
---
Backend (FastAPI):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend (Streamlit):
```bash
cd frontend
streamlit run streamlit_app.py
```

Key Endpoints (Backend)
-----------------------
- `GET /players/names` — List of players with `player_name` and `birth_year`
- `GET /player/{player_name}?birth_year=YYYY` — Season stats for a player
- `GET /player-headshot/{player_name}/{birth_year}` — Player headshot URL
- `GET /generate_report/{player_name}/{birth_year}` — Scouting report text

Notes
-----
- Data comes from Basketball Reference (2020–2025) CSVs in `data/`.
- Ensure `BACKEND_URL` points to the running FastAPI instance before starting Streamlit.

License
-------
See `LICENSE`.
