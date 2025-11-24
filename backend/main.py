from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, List
import uvicorn
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from models.predictor import MatchPredictor, SeasonPredictor
from data.data_fetcher import DataFetcher
from database.db import Database
from schemas import MatchPrediction, SeasonPrediction, Team, Match, Player


def get_mock_teams():
    """Return mock Premier League teams when API is unavailable"""
    return [
        {"id": 1, "name": "Arsenal", "short_name": "ARS", "crest": None, "founded": 1886},
        {"id": 2, "name": "Aston Villa", "short_name": "AVL", "crest": None, "founded": 1874},
        {"id": 3, "name": "Bournemouth", "short_name": "BOU", "crest": None, "founded": 1899},
        {"id": 4, "name": "Brentford", "short_name": "BRE", "crest": None, "founded": 1889},
        {"id": 5, "name": "Brighton", "short_name": "BHA", "crest": None, "founded": 1901},
        {"id": 6, "name": "Chelsea", "short_name": "CHE", "crest": None, "founded": 1905},
        {"id": 7, "name": "Crystal Palace", "short_name": "CRY", "crest": None, "founded": 1905},
        {"id": 8, "name": "Everton", "short_name": "EVE", "crest": None, "founded": 1878},
        {"id": 9, "name": "Fulham", "short_name": "FUL", "crest": None, "founded": 1879},
        {"id": 10, "name": "Liverpool", "short_name": "LIV", "crest": None, "founded": 1892},
        {"id": 11, "name": "Luton Town", "short_name": "LUT", "crest": None, "founded": 1885},
        {"id": 12, "name": "Manchester City", "short_name": "MCI", "crest": None, "founded": 1880},
        {"id": 13, "name": "Manchester United", "short_name": "MUN", "crest": None, "founded": 1878},
        {"id": 14, "name": "Newcastle United", "short_name": "NEW", "crest": None, "founded": 1892},
        {"id": 15, "name": "Nottingham Forest", "short_name": "NFO", "crest": None, "founded": 1865},
        {"id": 16, "name": "Sheffield United", "short_name": "SHU", "crest": None, "founded": 1889},
        {"id": 17, "name": "Tottenham", "short_name": "TOT", "crest": None, "founded": 1882},
        {"id": 18, "name": "West Ham", "short_name": "WHU", "crest": None, "founded": 1895},
        {"id": 19, "name": "Wolves", "short_name": "WOL", "crest": None, "founded": 1877},
        {"id": 20, "name": "Burnley", "short_name": "BUR", "crest": None, "founded": 1882},
    ]


def get_mock_team_stats(team_name: str):
    """Return mock team stats when API is unavailable"""
    # Generate realistic mock stats based on team name
    import random
    random.seed(hash(team_name) % 1000)  # Consistent stats per team
    
    matches = random.randint(15, 25)
    wins = random.randint(5, matches - 5)
    draws = random.randint(2, matches - wins - 2)
    losses = matches - wins - draws
    goals_for = random.randint(20, 50)
    goals_against = random.randint(15, 45)
    
    return {
        "team": team_name,
        "matches_played": matches,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "goals_for": goals_for,
        "goals_against": goals_against,
        "goal_diff": goals_for - goals_against,
        "points": wins * 3 + draws,
        "position": random.randint(1, 20),
        "form": "".join(random.choices(["W", "D", "L"], k=5))
    }

app = FastAPI(
    title="Premier League Predictor API",
    description="AI-powered predictions for Premier League matches and seasons",
    version="1.0.0"
)

# CORS middleware
# Allow origins from environment variable or default to localhost
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]
print(f"CORS allowed origins: {allowed_origins}")  # Debug log
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db = Database()
data_fetcher = DataFetcher()
match_predictor = MatchPredictor()
season_predictor = SeasonPredictor()

@app.on_event("startup")
async def startup_event():
    """Initialize models and database on startup"""
    try:
        # Ensure database is initialized
        db.init_db()
        # Load trained models
        match_predictor.load_model()
        season_predictor.load_model()
        print("Models loaded successfully")
    except Exception as e:
        print(f"Warning: Could not load models: {e}")
        print("Run training script first: python scripts/train_models.py")


@app.get("/")
async def root():
    return {
        "message": "Premier League Predictor API",
        "version": "1.0.0",
        "endpoints": {
            "predict_match": "/api/predict/match/{home_team}/{away_team}",
            "predict_season": "/api/predict/season",
            "teams": "/api/teams",
            "matches": "/api/matches",
            "team_stats": "/api/stats/{team}"
        }
    }


@app.get("/api/teams", response_model=List[Team])
async def get_teams():
    """Get all Premier League teams"""
    try:
        teams = db.get_teams()
        if not teams:
            # Fetch from API if not in database
            teams_data = await data_fetcher.fetch_teams()
            if not teams_data:
                # Use mock data if API unavailable
                print("API unavailable, using mock teams data")
                teams_data = get_mock_teams()
            db.save_teams(teams_data)
            teams = db.get_teams()
        return teams
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/matches", response_model=List[Match])
async def get_matches():
    """Get upcoming Premier League matches"""
    try:
        matches = await data_fetcher.fetch_upcoming_matches()
        # If no matches from API, return empty list (frontend handles this gracefully)
        if not matches:
            print("No matches available from API")
            return []  # Return empty list instead of None
        return matches
    except Exception as e:
        print(f"Error fetching matches: {e}")
        return []  # Return empty list on error instead of raising exception


@app.get("/api/predict/match/{home_team}/{away_team}", response_model=MatchPrediction)
async def predict_match(home_team: str, away_team: str):
    """
    Predict the outcome of a specific match
    
    - **home_team**: Name of the home team
    - **away_team**: Name of the away team
    """
    try:
        # Normalize team names
        home_team = home_team.replace("_", " ").replace("-", " ")
        away_team = away_team.replace("_", " ").replace("-", " ")
        
        prediction = await match_predictor.predict(home_team, away_team)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/predict/season", response_model=SeasonPrediction)
async def predict_season():
    """Predict the entire season standings"""
    try:
        prediction = await season_predictor.predict_season()
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats/{team}")
async def get_team_stats(team: str, refresh: bool = False):
    """Get statistics for a specific team
    
    Args:
        team: Team name
        refresh: If True, force refresh from API (default: False, but will refresh if data is old)
    """
    try:
        team = team.replace("_", " ").replace("-", " ")
        
        # Always fetch fresh data from API to ensure accuracy
        # The API provides the most up-to-date standings
        stats = await data_fetcher.fetch_team_stats(team)
        
        if not stats:
            # Try database as fallback
            stats = db.get_team_stats(team)
            if not stats:
                # Use mock data if API unavailable
                print(f"API unavailable, using mock stats for {team}")
                stats = get_mock_team_stats(team)
        else:
            # Save fresh data to database
            db.save_team_stats(team, stats)
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/players/{team}", response_model=List[Player])
async def get_team_players(team: str):
    """Get squad/players for a specific team"""
    try:
        team = team.replace("_", " ").replace("-", " ")
        players = await data_fetcher.fetch_team_squad(team)
        return players
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": match_predictor.model_loaded
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

