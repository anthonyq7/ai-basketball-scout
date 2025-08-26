AI Basketball Scout
===================

A comprehensive NBA scouting application that generates detailed player reports and visualizes performance across multiple seasons. **Now deployed on Render for easy access!**

Features
--------
- Search and select players across 6 NBA seasons (2020-2025)
- Generate AI-powered scouting reports with detailed analysis
- Comprehensive performance visualization with 50+ statistical metrics
- FastAPI backend with Redis caching for optimal performance
- Streamlit frontend for an intuitive, interactive user experience

Data Coverage
-------------
- **6 Complete Seasons**: 2019-2020 through 2024-2025
- **50+ Statistical Metrics** including:
  - Traditional stats (PPG, APG, RPG, SPG, BPG)
  - Advanced metrics (PER, TS%, Win Shares, VORP)
  - Shooting analytics (3P%, Mid-range %, Corner 3s)
  - Efficiency ratings (Offensive/Defensive Rating)
  - Possession-based stats (Per 100 possessions)
- **Data Source**: Basketball Reference - the most comprehensive basketball statistics database
- **Real-time Updates**: Automated scraping ensures data freshness

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

Live Demo
---------
**Access the application directly on Render:**
- No local installation required
- Always up-to-date with the latest data
- Optimized for production use

Key Endpoints (Backend)
-----------------------
- `GET /players/names` — List of players with `player_name` and `birth_year`
- `GET /player/{player_name}?birth_year=YYYY` — Season stats for a player
- `GET /player-headshot/{player_name}/{birth_year}` — Player headshot URL
- `GET /generate_report/{player_name}/{birth_year}` — AI-generated scouting report
- `GET /rate-limit/status` — Check API rate limit usage

Data Sources
------------
All player statistics are sourced from Basketball Reference, combining:
- **Per Game Statistics**: Traditional box score metrics
- **Per 100 Possessions**: Pace-adjusted performance data
- **Advanced Metrics**: Efficiency and impact measurements
- **Shooting Analytics**: Distance-based and assisted shot data

This comprehensive dataset enables detailed player analysis across multiple dimensions, providing insights that go beyond basic statistics.

License
-------
See `LICENSE`.
