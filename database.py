from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal=sessionmaker(bind=engine)

class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    year = Column(Float, nullable=True)
    player_name = Column(String, nullable=False)
    age = Column(Float, nullable=False)
    position = Column(String, nullable=False)
    games_played = Column(Float)
    minutes_played_per_game = Column(Float)
    field_goals_made_per_game = Column(Float)
    field_goal_attempts_per_game = Column(Float)
    field_goal_percentage = Column(Float)
    three_pointers_made_per_game = Column(Float)
    three_point_attempts_per_game = Column(Float)
    three_point_percentage = Column(Float)
    two_pointers_made_per_game = Column(Float)
    two_point_attempts_per_game = Column(Float)
    two_point_percentage = Column(Float)
    free_throws_made_per_game = Column(Float)
    free_throw_attempts_per_game = Column(Float)
    free_throw_percentage = Column(Float)
    offensive_rebounds_per_game = Column(Float)
    defensive_rebounds_per_game = Column(Float)
    total_rebounds_per_game = Column(Float)
    assists_per_game = Column(Float)
    steals_per_game = Column(Float)
    blocks_per_game = Column(Float)
    turnovers_per_game = Column(Float)
    personal_fouls_per_game = Column(Float)
    points_per_game = Column(Float)
    
    # Per 100 possessions stats
    offensive_rating = Column(Float)
    defensive_rating = Column(Float)
    
    # Advanced stats
    player_efficiency_rating = Column(Float)
    true_shooting_percentage = Column(Float)
    total_rebound_percentage = Column(Float)
    assist_percentage = Column(Float)
    steal_percentage = Column(Float)
    block_percentage = Column(Float)
    turnover_percentage = Column(Float)
    usage_percentage = Column(Float)
    win_shares = Column(Float)
    win_shares_per_48 = Column(Float)
    box_plus_minus = Column(Float)
    value_over_replacement_player = Column(Float)
    
    # Shooting distance attempt percentages
    two_point_attempt_percentage = Column(Float)
    layup_dunk_attempt_percentage = Column(Float)
    short_midrange_attempt_percentage = Column(Float)
    midrange_attempt_percentage = Column(Float)
    long_midrange_attempt_percentage = Column(Float)
    three_point_attempt_percentage = Column(Float)
    
    # Shooting distance made percentages
    layup_dunk_made_percentage = Column(Float)
    short_midrange_made_percentage = Column(Float)
    midrange_made_percentage = Column(Float)
    long_midrange_made_percentage = Column(Float)
    
    # Assisted field goal percentages
    two_point_assisted_percentage = Column(Float)
    three_point_assisted_percentage = Column(Float)
    
    # Corner three statistics
    corner_three_attempt_percentage = Column(Float)
    corner_three_made_percentage = Column(Float)
    