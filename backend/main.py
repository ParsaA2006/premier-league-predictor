from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, List
import uvicorn
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from models.predictor import MatchPredictor, SeasonPredictor
from data.data_fetcher import DataFetcher
from database.db import Database
from schemas import MatchPrediction, SeasonPrediction, Team, Match

app = FastAPI(
    title="Premier League Predictor API",
    description="AI-powered predictions for Premier League matches and seasons",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
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
        return matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
async def get_team_stats(team: str):
    """Get statistics for a specific team"""
    try:
        team = team.replace("_", " ").replace("-", " ")
        stats = db.get_team_stats(team)
        if not stats:
            # Fetch from API
            stats = await data_fetcher.fetch_team_stats(team)
            db.save_team_stats(team, stats)
        return stats
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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

