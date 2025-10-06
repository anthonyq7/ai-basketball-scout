from fastapi.responses import PlainTextResponse
from models import Player
import scraper
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
import database
import gemini
from typing import List
from dotenv import load_dotenv
import os
import redis
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import json
import asyncio

load_dotenv()

app = FastAPI()
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.getenv("REDIS_URL")
    )
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.on_event("startup")
async def startup_event():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print(f"Data directory ensured: {data_dir.absolute()}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_URL", "http://localhost:8501"),  
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"], 
    allow_headers=[
        "Accept",                    
        "Content-Type"                      
    ],
    max_age=600  
)


database.Base.metadata.create_all(bind=database.engine)
redis_client = redis.from_url(os.getenv("REDIS_URL"))
years = [2025, 2024, 2023, 2022, 2021, 2020]

@app.get("/")
async def root():
    return {"message": "AI Basketball Scout"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/players")
async def post_players():
    db = database.SessionLocal()
    try:
        players = []
        for year in years:
            year_players = await scraper.create_player_models(scraper.process_and_merge_data(float(year)))
            players = players + year_players

        added_count = 0
        for player in players:
            entry = db.query(database.Player).filter(database.Player.player_name == player.get("player_name"), database.Player.year == player.get("year"), database.Player.birth_year == player.get("birth_year")).first()
            if not entry:
                new_entry = database.Player(
                    player_name=player.get("player_name"),
                    age=player.get("age"),
                    birth_year=player.get("birth_year"),
                    position=player.get("position"),
                    headshot_url=player.get("headshot_url"),
                    games_played=player.get("games_played"),
                    minutes_played_per_game=player.get("minutes_played_per_game"),
                    field_goals_made_per_game=player.get("field_goals_made_per_game"),
                    field_goal_attempts_per_game=player.get("field_goal_attempts_per_game"),
                    field_goal_percentage=player.get("field_goal_percentage"),
                    three_pointers_made_per_game=player.get("three_pointers_made_per_game"),
                    three_point_attempts_per_game=player.get("three_point_attempts_per_game"),
                    three_point_percentage=player.get("three_point_percentage"),
                    two_pointers_made_per_game=player.get("two_pointers_made_per_game"),
                    two_point_attempts_per_game=player.get("two_point_attempts_per_game"),
                    two_point_percentage=player.get("two_point_percentage"),
                    free_throws_made_per_game=player.get("free_throws_made_per_game"),
                    free_throw_attempts_per_game=player.get("free_throw_attempts_per_game"),
                    free_throw_percentage=player.get("free_throw_percentage"),
                    offensive_rebounds_per_game=player.get("offensive_rebounds_per_game"),
                    defensive_rebounds_per_game=player.get("defensive_rebounds_per_game"),
                    total_rebounds_per_game=player.get("total_rebounds_per_game"),
                    assists_per_game=player.get("assists_per_game"),
                    steals_per_game=player.get("steals_per_game"),
                    blocks_per_game=player.get("blocks_per_game"),
                    turnovers_per_game=player.get("turnovers_per_game"),
                    personal_fouls_per_game=player.get("personal_fouls_per_game"),
                    points_per_game=player.get("points_per_game"),
                    offensive_rating=player.get("offensive_rating"),
                    defensive_rating=player.get("defensive_rating"),
                    player_efficiency_rating=player.get("player_efficiency_rating"),
                    true_shooting_percentage=player.get("true_shooting_percentage"),
                    total_rebound_percentage=player.get("total_rebound_percentage"),
                    assist_percentage=player.get("assist_percentage"),
                    steal_percentage=player.get("steal_percentage"),
                    block_percentage=player.get("block_percentage"),
                    turnover_percentage=player.get("turnover_percentage"),
                    usage_percentage=player.get("usage_percentage"),
                    win_shares=player.get("win_shares"),
                    win_shares_per_48=player.get("win_shares_per_48"),
                    box_plus_minus=player.get("box_plus_minus"),
                    value_over_replacement_player=player.get("value_over_replacement_player"),
                    two_point_attempt_percentage=player.get("two_point_attempt_percentage"),
                    layup_dunk_attempt_percentage=player.get("layup_dunk_attempt_percentage"),
                    short_midrange_attempt_percentage=player.get("short_midrange_attempt_percentage"),
                    midrange_attempt_percentage=player.get("midrange_attempt_percentage"),
                    long_midrange_attempt_percentage=player.get("long_midrange_attempt_percentage"),
                    three_point_attempt_percentage=player.get("three_point_attempt_percentage"),
                    layup_dunk_made_percentage=player.get("layup_dunk_made_percentage"),
                    short_midrange_made_percentage=player.get("short_midrange_made_percentage"),
                    midrange_made_percentage=player.get("midrange_made_percentage"),
                    long_midrange_made_percentage=player.get("long_midrange_made_percentage"),
                    two_point_assisted_percentage=player.get("two_point_assisted_percentage"),
                    three_point_assisted_percentage=player.get("three_point_assisted_percentage"),
                    corner_three_attempt_percentage=player.get("corner_three_attempt_percentage"),
                    corner_three_made_percentage=player.get("corner_three_made_percentage"),
                    year=player.get("year")
                )
                db.add(new_entry)
                added_count += 1
        
        db.commit()
        return {"message": f"Successfully added {added_count} players to database"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to add players")
    finally:
        db.close()


@app.get("/players", response_model=List[Player])
async def get_players():
    db = database.SessionLocal()
    try:
        players = db.query(database.Player).all()
        return players
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get players")
    finally:
        db.close()

@app.get("/player/{player_name}", response_model=List[Player])
async def get_player(player_name: str, birth_year: int):
    db = database.SessionLocal()
    try:
        player = db.query(database.Player).filter(database.Player.player_name == player_name, database.Player.birth_year == birth_year).all()
        return player #FASTAPI + PYNDANTIC converts this SQLALchemy model to JSON
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to get player")
    finally:
        db.close()
    """
    OLD CODE:
    players = await scraper.create_player_models(merged)
    year = float(year)
    player_name.strip()
    low = 0 
    high = len(players) - 1

    #AYYYYYY O(log n)
    while low <= high:
        mid = (low + high) // 2
        mid_player = players[mid]

        if mid_player.get("player_name") == player_name and mid_player.get("year") == year:
            return {"player": mid_player}
        elif mid_player.get("player_name") < player_name:
            low = mid + 1
        else:
            high = mid - 1
    return {"Error": "Player not found"} 
    """

@app.get("/scrape/players")
async def scrape_players():
    try:
        await scraper.scrape_all_stats()
        return {"message": "data successfully scraped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to scrape players")

# Helpers to structure JSON as {year: {stats}}
def players_to_year_map(players: List[Player]) -> dict:
    out = {}
    for p in players: #Iterates season by season
        d = p.model_dump(mode="json") #Converts a Player object to dict
        y = d.get("year")
        key = str(int(y)) if isinstance(y, (int, float)) else str(y) #Makes the "year" key stored as a string
        stats = {k: v for k, v in d.items() if k != "year"} #Copy everything except year into a dictionary
        out[key] = stats #Using the year as a key, puts all of stats as a value
    return out 

def rows_to_year_map(rows) -> dict:
    pyd = [Player.model_validate(r, from_attributes=True) for r in rows] #Brackets create a list, converts each row into a validated Player object
    #from_attributes tells Pydantic to look at attributes from the SQLAlchemy row, r.
    #Normally, Pyndantic expects a dict 
    return players_to_year_map(pyd)

@app.get("/generate_report/{player_name}/{birth_year}")
@limiter.limit("10/minute")
async def get_player_report(request: Request, player_name: str, birth_year: int):
    cache_key=f"player:{player_name}:birth-year:{birth_year}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        data = cached_data.decode('utf-8') #converts from bytes to string
        return PlainTextResponse(content=data)

    db = database.SessionLocal()
    try:
        rows = db.query(database.Player).filter(database.Player.player_name == player_name, database.Player.birth_year == birth_year).all()
        if not rows:
            return {"Error": "Player not found"}
        year_map = rows_to_year_map(rows)
        report = gemini.generate_report({"player_name": player_name, "seasons": year_map})
        redis_client.setex(cache_key, 3600, report)
        return PlainTextResponse(content=report)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate report")
    finally:
        db.close()

@app.get("/players/names")
async def get_player_names_all():
    db = database.SessionLocal()
    try:
        rows = db.query(database.Player).all()
        unique_players = []
        if not rows:
            return {"Error": "No players found"}

        for r in rows: #Loops through all players
            player_exists = any(
                existing["player_name"] == r.player_name and existing["birth_year"] == r.birth_year for existing in unique_players
            ) #Checks to see if ANY are in unique_players
            
            if not player_exists:
                unique_players.append({ #Appends to list if not exists
                    "player_name": r.player_name,
                    "birth_year": r.birth_year
                })
        #unique_names = [player.get("player_name") for player in unique_players] >>> This gets only names
        return unique_players
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get player names")
    finally:
        db.close()

@app.get("/player-headshot/{player_name}/{birth_year}")
async def get_player_headshot(player_name: str, birth_year: int):
    db = database.SessionLocal()
    try:
        query = db.query(database.Player).filter(database.Player.player_name == player_name, database.Player.birth_year == birth_year).first()
        if not query:
            return {"Error": "Player not found"}
        headshot_url = query.headshot_url
        return {"headshot_url": headshot_url} #returns a JSON object with URL
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get headshot")
    finally:
        db.close()

@app.websocket("/ws/generate_report/{player_name}/{birth_year}")
async def websocket_generate_report(websocket: WebSocket, player_name: str, birth_year: int):
    await websocket.accept()
    
    try:
        cache_key = f"player:{player_name}:birth-year:{birth_year}"
        cached_data = redis_client.get(cache_key)
        
        if cached_data:
            #Send cached data as a single message
            cached_report = cached_data.decode('utf-8')
            await websocket.send_text(json.dumps({
                "type": "complete",
                "content": cached_report,
                "cached": True
            }))
            return
        
        db = database.SessionLocal()
        try:
            rows = db.query(database.Player).filter(
                database.Player.player_name == player_name, 
                database.Player.birth_year == birth_year
            ).all()
            
            if not rows:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "content": "Player not found"
                }))
                return
            
            year_map = rows_to_year_map(rows)
            player_data = {"player_name": player_name, "seasons": year_map}
            
        finally:
            db.close()
        
        #Send initial message
        await websocket.send_text(json.dumps({
            "type": "start",
            "content": f"Generating report for {player_name}"
        }))
        
        # Stream the report token by token
        full_report = ""
        async for token in gemini.generate_report_stream(player_data):
            if token:
                full_report += token
                await websocket.send_text(json.dumps({
                    "type": "token",
                    "content": token
                }))
                # Small delay to make streaming visible
                await asyncio.sleep(0.05)
        
        #Cache the complete report
        redis_client.setex(cache_key, 3600, full_report)
        
        #Send completion message
        await websocket.send_text(json.dumps({
            "type": "complete",
            "content": "Report generation completed.",
            "cached": False
        }))
        
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for {player_name}")
    except Exception as e:
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "content": "Error generating report"
            }))
        except:
            pass  #Connection might be closed

