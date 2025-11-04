import pickle
import os
import numpy as np
from typing import Optional
import asyncio

from database.db import Database
from data.feature_engineering import FeatureEngineer


class MatchPredictor:
    """Predicts match outcomes using trained ML models"""
    
    def __init__(self):
        self.model = None
        self.score_model = None
        self.model_loaded = False
        self.db = Database()
        self.feature_engineer = FeatureEngineer()
        self.model_path = "models/trained/match_predictor.pkl"
        self.score_model_path = "models/trained/score_predictor.pkl"
    
    def load_model(self):
        """Load trained models from disk"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                self.model_loaded = True
            
            if os.path.exists(self.score_model_path):
                with open(self.score_model_path, 'rb') as f:
                    self.score_model = pickle.load(f)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model_loaded = False
    
    async def predict(self, home_team: str, away_team: str):
        """Predict match outcome"""
        if not self.model_loaded:
            # Fallback to simple prediction based on stats
            return await self._simple_predict(home_team, away_team)
        
        # Get team features
        features = await self.feature_engineer.get_match_features(home_team, away_team)
        
        if features is None:
            return await self._simple_predict(home_team, away_team)
        
        # Predict outcome
        outcome_probs = self.model.predict_proba([features])[0]
        outcome_pred = self.model.predict([features])[0]
        
        # Map prediction to result
        result_map = {0: "HOME_WIN", 1: "DRAW", 2: "AWAY_WIN"}
        predicted_result = result_map[outcome_pred]
        
        # Predict scores if model available
        home_score, away_score = None, None
        if self.score_model:
            try:
                scores = self.score_model.predict([features])[0]
                home_score = max(0, int(round(scores[0])))
                away_score = max(0, int(round(scores[1])))
            except:
                pass
        
        return {
            "home_team": home_team,
            "away_team": away_team,
            "predicted_result": predicted_result,
            "home_win_probability": float(outcome_probs[0]),
            "draw_probability": float(outcome_probs[1]),
            "away_win_probability": float(outcome_probs[2]),
            "predicted_home_score": home_score,
            "predicted_away_score": away_score,
            "confidence": float(max(outcome_probs))
        }
    
    async def _simple_predict(self, home_team: str, away_team: str):
        """Simple prediction based on team stats when model not available"""
        home_stats = self.db.get_team_stats(home_team)
        away_stats = self.db.get_team_stats(away_team)
        
        if not home_stats or not away_stats:
            # Default prediction
            return {
                "home_team": home_team,
                "away_team": away_team,
                "predicted_result": "DRAW",
                "home_win_probability": 0.33,
                "draw_probability": 0.34,
                "away_win_probability": 0.33,
                "predicted_home_score": 1,
                "predicted_away_score": 1,
                "confidence": 0.5
            }
        
        # Simple logic based on points and form
        home_strength = home_stats.get('points', 0) + home_stats.get('goal_diff', 0) * 0.1
        away_strength = away_stats.get('points', 0)
        
        # Home advantage factor
        home_strength *= 1.15
        
        if home_strength > away_strength + 10:
            result = "HOME_WIN"
            home_prob = 0.6
            draw_prob = 0.25
            away_prob = 0.15
        elif away_strength > home_strength + 10:
            result = "AWAY_WIN"
            home_prob = 0.15
            draw_prob = 0.25
            away_prob = 0.6
        else:
            result = "DRAW"
            home_prob = 0.35
            draw_prob = 0.35
            away_prob = 0.30
        
        return {
            "home_team": home_team,
            "away_team": away_team,
            "predicted_result": result,
            "home_win_probability": home_prob,
            "draw_probability": draw_prob,
            "away_win_probability": away_prob,
            "predicted_home_score": 1,
            "predicted_away_score": 1,
            "confidence": max(home_prob, draw_prob, away_prob)
        }


class SeasonPredictor:
    """Predicts entire season standings"""
    
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.db = Database()
        self.model_path = "models/trained/season_predictor.pkl"
    
    def load_model(self):
        """Load trained season prediction model"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                self.model_loaded = True
        except Exception as e:
            print(f"Error loading season model: {e}")
    
    async def predict_season(self):
        """Predict season standings"""
        from datetime import datetime
        
        teams = self.db.get_teams()
        if not teams:
            return {
                "season": "2024/25",
                "predicted_standings": [],
                "predicted_champion": "Unknown",
                "predicted_relegated": [],
                "updated_at": datetime.now()
            }
        
        # Get current season data
        standings = []
        for team in teams:
            stats = self.db.get_team_stats(team['name'])
            if stats:
                # Simple prediction: extrapolate current form
                matches_played = stats.get('matches_played', 0)
                current_points = stats.get('points', 0)
                
                if matches_played > 0:
                    points_per_game = current_points / matches_played
                    predicted_points = points_per_game * 38  # 38 games in a season
                else:
                    predicted_points = 50  # Default
                
                standings.append({
                    "team": team['name'],
                    "predicted_points": round(predicted_points, 1),
                    "current_points": current_points,
                    "current_position": stats.get('position', 0)
                })
        
        # Sort by predicted points
        standings.sort(key=lambda x: x['predicted_points'], reverse=True)
        
        # Add position
        for i, team in enumerate(standings):
            team['predicted_position'] = i + 1
        
        predicted_champion = standings[0]['team'] if standings else "Unknown"
        predicted_relegated = [t['team'] for t in standings[-3:]] if len(standings) >= 3 else []
        
        return {
            "season": "2024/25",
            "predicted_standings": standings,
            "predicted_champion": predicted_champion,
            "predicted_relegated": predicted_relegated,
            "updated_at": datetime.now()
        }

