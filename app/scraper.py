import os
import pandas as pd
import httpx
from io import StringIO  
from bs4 import BeautifulSoup, Comment
from app.models import Player
from nba_api.stats.static import players as nba_players
from fastapi import HTTPException
from typing import Optional


def get_bref_stats_v1(url, csv_name): #Legacy code right here, for learning and review purposes
    html_content = httpx.get(url).text #Downloads page's HTML as a string
    html = StringIO(html_content) #Turns that string into a file-like object
    dfs = pd.read_html(html) #Parses tables: scans the HTML and finds every <table> and returns them as a list of dataframes (dfs)
    df = dfs[0] #Picks the first table
    # .head() shows the first 5 rows
    df.to_csv(f"data/{csv_name}.csv", index=False) #Turns df into .csv file


def get_bref_stats(url, csv_name): #This version accounts for tables hidden inside HTML comments
    
    html_content = httpx.get(url).text
    soup = BeautifulSoup(html_content, "lxml")

    comment = soup.find(string=lambda text: isinstance(text, Comment) and "<table" in text)
    if comment:
        df = pd.read_html(str(BeautifulSoup(comment, "lxml")))[0]
        df.to_csv(f"data/{csv_name}.csv", index=False)
        return
    
    df = pd.read_html(StringIO(html_content))[0]
    df.to_csv(f"data/{csv_name}.csv", index=False)


async def scrape_all_stats():
    """Scrape all basketball statistics from Basketball Reference"""
    url_dict = {}
    url_dict["per_game_2025"] = "https://www.basketball-reference.com/leagues/NBA_2025_per_game.html"
    url_dict["per_100_poss_2025"] = "https://www.basketball-reference.com/leagues/NBA_2025_per_poss.html"
    url_dict["advanced_2025"] = "https://www.basketball-reference.com/leagues/NBA_2025_advanced.html"
    url_dict["shooting_2025"] = "https://www.basketball-reference.com/leagues/NBA_2025_shooting.html"
    url_dict["per_game_2024"] = "https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"
    url_dict["per_100_poss_2024"] = "https://www.basketball-reference.com/leagues/NBA_2024_per_poss.html"
    url_dict["advanced_2024"] = "https://www.basketball-reference.com/leagues/NBA_2024_advanced.html"
    url_dict["shooting_2024"] = "https://www.basketball-reference.com/leagues/NBA_2024_shooting.html"
    url_dict["per_game_2023"] = "https://www.basketball-reference.com/leagues/NBA_2023_per_game.html"
    url_dict["per_100_poss_2023"] = "https://www.basketball-reference.com/leagues/NBA_2023_per_poss.html"
    url_dict["advanced_2023"] = "https://www.basketball-reference.com/leagues/NBA_2023_advanced.html"
    url_dict["shooting_2023"] = "https://www.basketball-reference.com/leagues/NBA_2023_shooting.html"
    url_dict["per_game_2022"] = "https://www.basketball-reference.com/leagues/NBA_2022_per_game.html"
    url_dict["per_100_poss_2022"] = "https://www.basketball-reference.com/leagues/NBA_2022_per_poss.html"
    url_dict["advanced_2022"] = "https://www.basketball-reference.com/leagues/NBA_2022_advanced.html"
    url_dict["shooting_2022"] = "https://www.basketball-reference.com/leagues/NBA_2022_shooting.html"
    url_dict["per_game_2021"] = "https://www.basketball-reference.com/leagues/NBA_2021_per_game.html"
    url_dict["per_100_poss_2021"] = "https://www.basketball-reference.com/leagues/NBA_2021_per_poss.html"
    url_dict["advanced_2021"] = "https://www.basketball-reference.com/leagues/NBA_2021_advanced.html"
    url_dict["shooting_2021"] = "https://www.basketball-reference.com/leagues/NBA_2021_shooting.html"
    url_dict["per_game_2020"] = "https://www.basketball-reference.com/leagues/NBA_2020_per_game.html"
    url_dict["per_100_poss_2020"] = "https://www.basketball-reference.com/leagues/NBA_2020_per_poss.html"
    url_dict["advanced_2020"] = "https://www.basketball-reference.com/leagues/NBA_2020_advanced.html"
    url_dict["shooting_2020"] = "https://www.basketball-reference.com/leagues/NBA_2020_shooting.html"
    
    for key, value in url_dict.items():
        get_bref_stats(value, key)


def process_and_merge_data(year: int):
    """Process and merge all scraped data into a single dataframe for a given year"""
    year = int(year)
    file_map = {
        "per_game": f"data/per_game_{year}.csv",
        "per_100": f"data/per_100_poss_{year}.csv",
        "advanced": f"data/advanced_{year}.csv",
        "shooting": f"data/shooting_{year}.csv",
    }
    missing = [path for path in file_map.values() if not os.path.exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing CSV files for year {year}: {', '.join(missing)}")

    # Load all CSV files
    df_per_game = pd.read_csv(file_map["per_game"])
    df_per_100_poss = pd.read_csv(file_map["per_100"])
    df_advanced = pd.read_csv(file_map["advanced"])
    df_shooting = pd.read_csv(file_map["shooting"], header=[0, 1])

    # PICK THE COLUMNS I WANT + RENAMING THEM
    per_game_sel = (
        df_per_game
            .loc[:, ["Player", "Age", "Team", "Pos", "G", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "2P", "2PA", "2P%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]]
            .rename(columns={
                "Player": "player_name", 
                "Age": "age", 
                "Team": "team", 
                "Pos": "position", 
                "G": "games_played", 
                "MP": "minutes_played_per_game", 
                "FG": "field_goals_made_per_game", 
                "FGA": "field_goal_attempts_per_game", 
                "FG%": "field_goal_percentage", 
                "3P": "three_pointers_made_per_game", 
                "3PA": "three_point_attempts_per_game", 
                "3P%": "three_point_percentage", 
                "2P": "two_pointers_made_per_game", 
                "2PA": "two_point_attempts_per_game", 
                "2P%": "two_point_percentage", 
                "FT": "free_throws_made_per_game", 
                "FTA": "free_throw_attempts_per_game", 
                "FT%": "free_throw_percentage", 
                "ORB": "offensive_rebounds_per_game", 
                "DRB": "defensive_rebounds_per_game", 
                "TRB": "total_rebounds_per_game", 
                "AST": "assists_per_game", 
                "STL": "steals_per_game", 
                "BLK": "blocks_per_game", 
                "TOV": "turnovers_per_game", 
                "PF": "personal_fouls_per_game", 
                "PTS": "points_per_game"
            })
    )

    per_100_poss_sel = (
        df_per_100_poss
            .loc[:, ["Player", "Age", "Team", "ORtg", "DRtg"]]
            .rename(columns={
                "Player": "player_name", 
                "Age": "age", 
                "Team": "team", 
                "ORtg": "offensive_rating", 
                "DRtg": "defensive_rating"
            })
    )

    advanced_sel = (
        df_advanced
            .loc[:, ["Player", "Age", "Team", "PER", "TS%", "TRB%", "AST%", "STL%", "BLK%", "TOV%", "USG%", "WS", "WS/48", "BPM", "VORP"]]
            .rename(columns={
                "Player": "player_name", 
                "Age": "age", 
                "Team": "team", 
                "PER": "player_efficiency_rating", 
                "TS%": "true_shooting_percentage", 
                "TRB%": "total_rebound_percentage", 
                "AST%": "assist_percentage", 
                "STL%": "steal_percentage", 
                "BLK%": "block_percentage", 
                "TOV%": "turnover_percentage", 
                "USG%": "usage_percentage", 
                "WS": "win_shares", 
                "WS/48": "win_shares_per_48", 
                "BPM": "box_plus_minus", 
                "VORP": "value_over_replacement_player"
            })
    )

    df_shooting_pct_FG_distance = df_shooting["% of FGA by Distance"]
    df_shooting_FG_pct_distance = df_shooting["FG% by Distance"]
    df_shooting_pct_assisted = df_shooting["% of FG Ast'd"]
    df_shooting_corner_3 = df_shooting["Corner 3s"]

    shooting_pct_FG_distance_sel = (
        df_shooting_pct_FG_distance
        .loc[:, ["2P", "0-3", "3-10", "10-16", "16-3P", "3P"]]
        .rename(columns={
            "2P": "two_point_attempt_percentage", 
            "0-3": "layup_dunk_attempt_percentage", 
            "3-10": "short_midrange_attempt_percentage", 
            "10-16": "midrange_attempt_percentage", 
            "16-3P": "long_midrange_attempt_percentage", 
            "3P": "three_point_attempt_percentage"
        })
    )

    shooting_FG_pct_distance_sel = (
        df_shooting_FG_pct_distance
        .loc[:, [ "0-3", "3-10", "10-16", "16-3P"]]
        .rename(columns={
            "0-3": "layup_dunk_made_percentage", 
            "3-10": "short_midrange_made_percentage", 
            "10-16": "midrange_made_percentage", 
            "16-3P": "long_midrange_made_percentage"
        })
    )

    shooting_pct_assisted_sel = (
        df_shooting_pct_assisted
        .rename(columns={
            "2P": "two_point_assisted_percentage", 
            "3P": "three_point_assisted_percentage"
        })
    )

    shooting_corner_3_sel = (
        df_shooting_corner_3
        .rename(columns={
            "%3PA": "corner_three_attempt_percentage", 
            "3P%": "corner_three_made_percentage"
        })
    )
    
    df_shooting_player_age_team = pd.concat([df_shooting["Unnamed: 1_level_0"], df_shooting["Unnamed: 2_level_0"], df_shooting["Unnamed: 3_level_0"]], axis=1)

    shooting_player_age_team_sel = (
        df_shooting_player_age_team.
        rename(columns={
            "Player": "player_name", 
            "Age": "age", 
            "Team": "team"
        })
    )

    shooting_sel = pd.concat([shooting_player_age_team_sel, shooting_pct_FG_distance_sel, shooting_FG_pct_distance_sel, shooting_pct_assisted_sel, shooting_corner_3_sel], axis=1)

    def keep_tot_or_first(df):
        def pick_group(g):
            has_multi = g["team"].isin(["2TM", "3TM", "4TM", "5TM", "6TM"]).any()
            if has_multi:
                return g[g["team"].isin(["2TM", "3TM", "4TM", "5TM", "6TM"])].head(1)
            return g.head(1)

        out = (
            df.sort_values(["player_name", "age", "team"])
              .groupby("player_name", as_index=False, group_keys=False)
              .apply(pick_group)
              .reset_index(drop=True)
        )
        return out

    per_game_sel = keep_tot_or_first(per_game_sel)
    per_100_poss_sel = keep_tot_or_first(per_100_poss_sel)
    advanced_sel = keep_tot_or_first(advanced_sel)
    shooting_sel = keep_tot_or_first(shooting_sel)

    for df in (per_game_sel, per_100_poss_sel, advanced_sel, shooting_sel):
        df.drop(columns="team", inplace=True)

    merged = per_game_sel.merge(per_100_poss_sel, on=["player_name", "age"], how="inner", validate="one_to_one")
    merged = merged.merge(advanced_sel, on=["player_name", "age"], how="inner", validate="one_to_one")
    merged = merged.merge(shooting_sel, on=["player_name", "age"], how="inner", validate="one_to_one")

    merged["year"] = float(year)
    merged['age'] = pd.to_numeric(merged['age'], errors='coerce')
    merged = merged[merged['player_name'].ne('League Average')]
    merged = merged.dropna(subset=['player_name', 'age', 'position'])
    return merged


def get_player_data(player_name: str, merged: pd.DataFrame) -> dict:
    mask = merged["player_name"].str.casefold().eq(player_name.casefold())
    row = merged.loc[mask].head(1)
    if row.empty:
        raise ValueError("Player/season not found")

    return row.iloc[0].to_dict()


async def create_player_models(merged: pd.DataFrame):
    player_models = []
    
    for index, row in merged.iterrows():
        player_dict = row.to_dict()
        player_dict['year'] = float(row['year'])
        hs_url = get_player_headshot(player_dict.get("player_name"))
        player_dict["headshot_url"] = hs_url
        player_dict["birth_year"] = player_dict.get("year") - player_dict.get("age") - 1
        
        # Handle NaN values by converting them to None (null)
        for key, value in player_dict.items():
            if pd.isna(value):
                player_dict[key] = None
        
        
        try:
            player_model = Player(**player_dict)
            player_models.append(player_model.model_dump())
        except Exception as e:
            print(f"Error creating model for {player_dict.get('player_name', 'Unknown')}: {e}")
    
    return player_models


def get_player_headshot(player_name: str) -> Optional[str]:
    player_name = player_name.strip() if player_name else player_name
    try:
        matches = nba_players.find_players_by_full_name(player_name)
        if not matches:
            return None
        player = matches[0]
        url = nba_cdn_headshot(int(player["id"]))
        return url
    except Exception:
        return None


def nba_cdn_headshot(nba_player_id: int, size="1040x760") -> str:
    return f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/{size}/{nba_player_id}.png"





        

