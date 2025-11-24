from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Team(BaseModel):
    id: int
    name: str
    short_name: Optional[str] = None
    crest: Optional[str] = None
    founded: Optional[int] = None


class Match(BaseModel):
    id: int
    home_team: str
    away_team: str
    date: datetime
    status: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None


class MatchPrediction(BaseModel):
    home_team: str
    away_team: str
    predicted_result: str  # "HOME_WIN", "DRAW", "AWAY_WIN"
    home_win_probability: float
    draw_probability: float
    away_win_probability: float
    predicted_home_score: Optional[int] = None
    predicted_away_score: Optional[int] = None
    confidence: float


class SeasonPrediction(BaseModel):
    season: str
    predicted_standings: List[dict]  # List of teams with predicted points, position, etc.
    predicted_champion: str
    predicted_relegated: List[str]
    updated_at: datetime


class TeamStats(BaseModel):
    team: str
    matches_played: int
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int
    points: int
    form: str  # Last 5 matches form (e.g., "WWDLW")
    home_record: dict
    away_record: dict


class Player(BaseModel):
    id: int
    name: str
    position: Optional[str] = None
    dateOfBirth: Optional[str] = None
    nationality: Optional[str] = None
    role: Optional[str] = None
    shirtNumber: Optional[int] = None
    photo: Optional[str] = None

