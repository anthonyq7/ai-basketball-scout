from fastapi.responses import PlainTextResponse
import pandas as pd
import scraper
from fastapi import FastAPI, HTTPException
import database
import json
import gemini

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)
merged = scraper.process_and_merge_data()

@app.get("/")
async def root():
    return {"message": "AI Basketball Scout"}

   
@app.post("/players")
async def post_players():
    db = database.SessionLocal()
    try:
        players = await scraper.create_player_models(merged)
        added_count = 0
        for player in players:
            entry = db.query(database.Player).filter(database.Player.player_name == player.get("player_name") and database.Player.year == player.get("year")).first()
            if not entry:
                new_entry = database.Player(
                    player_name=player.get("player_name"),
                    age=player.get("age"),
                    position=player.get("position"),
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
        raise HTTPException(status_code=500, detail=f"Error adding players: {str(e)}")
    finally:
        db.close()


@app.get("/players")
async def get_players():
    try:
        players = await scraper.create_player_models(merged)
        return {"players": players}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting players: {str(e)}")

@app.get("/player/{year}/{player_name}")
async def get_player(year: int, player_name: str):
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

@app.get("/scrape/players")
async def scrape_players():
    try:
        await scraper.scrape_all_stats()
        return {"message": "data successfully scraped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@app.get("/generate_report/{year}/{player_name}")
async def get_player_report(year: int, player_name: str):
    year = float(year)
    db = database.SessionLocal()
    try:
        query = db.query(database.Player).filter(database.Player.player_name == player_name and database.Player.year == year).first()
        if not query:
            return {"Error": "Player not found"}
        
        player_dict = vars(query)
        player_dict.pop('_sa_instance_state', None)
        report = gemini.generate_report(player_dict)
        return PlainTextResponse(content=report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

        






    
    


