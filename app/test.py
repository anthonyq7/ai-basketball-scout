import time
from dotenv import load_dotenv
from streamlit.commands.page_config import REPORT_A_BUG_KEY
from models import Player
import database
from statistics import median, quantiles, mean
from gemini import generate_report
from fastapi import HTTPException
from typing import List
import asyncio
import redis
import os

load_dotenv()
redis_client = redis.from_url(os.getenv("REDIS_URL"))

ITERATIONS = 100

def players_to_year_map(players: List[Player]) -> dict:
    out = {}
    for p in players:
        d = p.model_dump(mode="json")
        y = d.get("year")
        key = str(int(y)) if isinstance(y, (int, float)) else str(y)
        stats = {k: v for k, v in d.items() if k != "year"}
        out[key] = stats
    return out

def rows_to_year_map(rows) -> dict:
    pyd = [Player.model_validate(r, from_attributes=True) for r in rows]
    return players_to_year_map(pyd)

async def timeGeneration(player_name: str, birth_year: int):
    t0 = time.perf_counter()
    db = database.SessionLocal()
    try:
        rows = db.query(database.Player).filter(database.Player.player_name == player_name, database.Player.birth_year == birth_year).all()
        if not rows:
            return {"Error": "Player not found"}
        year_map = rows_to_year_map(rows)
        report = generate_report({"player_name": player_name, "seasons": year_map})
        return report, time.perf_counter() - t0
    finally:
        db.close()

async def timeCache(player_name: str, birth_year: int):
    t0 = time.perf_counter()
    cache_key=f"player:{player_name}:birth-year:{birth_year}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        data = cached_data.decode('utf-8')
        return data, time.perf_counter() - t0

def print_stats(label, timings):
    p90 = quantiles(timings, n=10)[-1]
    p95 = quantiles(timings, n=20)[-1]
    print(f"\n{label} (n={len(timings)})")
    print(f"  min= {min(timings)*1000:6.2f} ms")
    print(f"  p50= {median(timings)*1000:6.2f} ms")
    print(f"  mean= {mean(timings)*1000:6.2f} ms")
    print(f"  p90= {p90*1000:6.2f} ms")
    print(f"  p95= {p95*1000:6.2f} ms")
    print(f"  max= {max(timings)*1000:6.2f} ms")

async def main():
    print("Warming up cache...")
    report, gen_time = await timeGeneration("Draymond Green", 1990)
    print(report)
    redis_client.setex(f"player:{"Draymond Green"}:birth-year:{1990}", 60, report)
    print(f"  (Report generation time: {gen_time*1000:.2f} ms)\n") #Doing it once so that my tokens aren't cooked

    cache_times = []
    for x in range(ITERATIONS):
        x, t = await timeCache("Draymond Green", 1990)
        cache_times.append(t)
    
    print_stats("Redis Cache Latency", cache_times)


if __name__ == "__main__":
    asyncio.run(main())




    
    








