from pydantic import BaseModel
from typing import Optional

class Player(BaseModel):
    year: float
    player_name: str
    age: float
    position: str
    headshot_url: Optional[str] = None
    games_played: Optional[float] = None
    minutes_played_per_game: Optional[float] = None
    field_goals_made_per_game: Optional[float] = None
    field_goal_attempts_per_game: Optional[float] = None
    field_goal_percentage: Optional[float] = None
    three_pointers_made_per_game: Optional[float] = None
    three_point_attempts_per_game: Optional[float] = None
    three_point_percentage: Optional[float] = None
    two_pointers_made_per_game: Optional[float] = None
    two_point_attempts_per_game: Optional[float] = None
    two_point_percentage: Optional[float] = None
    free_throws_made_per_game: Optional[float] = None
    free_throw_attempts_per_game: Optional[float] = None
    free_throw_percentage: Optional[float] = None
    offensive_rebounds_per_game: Optional[float] = None
    defensive_rebounds_per_game: Optional[float] = None
    total_rebounds_per_game: Optional[float] = None
    assists_per_game: Optional[float] = None
    steals_per_game: Optional[float] = None
    blocks_per_game: Optional[float] = None
    turnovers_per_game: Optional[float] = None
    personal_fouls_per_game: Optional[float] = None
    points_per_game: Optional[float] = None
    
    # Per 100 possessions stats
    offensive_rating: Optional[float] = None
    defensive_rating: Optional[float] = None
    
    # Advanced stats
    player_efficiency_rating: Optional[float] = None
    true_shooting_percentage: Optional[float] = None
    total_rebound_percentage: Optional[float] = None
    assist_percentage: Optional[float] = None
    steal_percentage: Optional[float] = None
    block_percentage: Optional[float] = None
    turnover_percentage: Optional[float] = None
    usage_percentage: Optional[float] = None
    win_shares: Optional[float] = None
    win_shares_per_48: Optional[float] = None
    box_plus_minus: Optional[float] = None
    value_over_replacement_player: Optional[float] = None
    
    # Shooting distance attempt percentages
    two_point_attempt_percentage: Optional[float] = None
    layup_dunk_attempt_percentage: Optional[float] = None
    short_midrange_attempt_percentage: Optional[float] = None
    midrange_attempt_percentage: Optional[float] = None
    long_midrange_attempt_percentage: Optional[float] = None
    three_point_attempt_percentage: Optional[float] = None
    
    # Shooting distance made percentages
    layup_dunk_made_percentage: Optional[float] = None
    short_midrange_made_percentage: Optional[float] = None
    midrange_made_percentage: Optional[float] = None
    long_midrange_made_percentage: Optional[float] = None
    
    # Assisted field goal percentages
    two_point_assisted_percentage: Optional[float] = None
    three_point_assisted_percentage: Optional[float] = None
    
    # Corner three statistics
    corner_three_attempt_percentage: Optional[float] = None
    corner_three_made_percentage: Optional[float] = None

    class Config:
        from_attributes = True #Lets Pyndantic accept SQLAlchemy models
        #SQLAlchemy models cannot be serialized into JSON