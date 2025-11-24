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
        # Get the backend directory (parent of models directory)
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(backend_dir, "models", "trained", "match_predictor.pkl")
        self.score_model_path = os.path.join(backend_dir, "models", "trained", "score_predictor.pkl")
    
    def load_model(self):
        """Load trained models from disk"""
        try:
            # Ensure models directory exists
            models_dir = os.path.dirname(self.model_path)
            os.makedirs(models_dir, exist_ok=True)
            
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
        # Try to fetch stats if not in database
        from data.data_fetcher import DataFetcher
        data_fetcher = DataFetcher()
        
        home_stats = self.db.get_team_stats(home_team)
        if not home_stats:
            # Try to fetch from API
            stats = await data_fetcher.fetch_team_stats(home_team)
            if stats:
                self.db.save_team_stats(home_team, stats)
                home_stats = self.db.get_team_stats(home_team)
        
        away_stats = self.db.get_team_stats(away_team)
        if not away_stats:
            # Try to fetch from API
            stats = await data_fetcher.fetch_team_stats(away_team)
            if stats:
                self.db.save_team_stats(away_team, stats)
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
        
        # Calculate goals per game for both teams
        home_matches = max(home_stats.get('matches_played', 1), 1)
        away_matches = max(away_stats.get('matches_played', 1), 1)
        home_goals_per_game = home_stats.get('goals_for', 0) / home_matches
        away_goals_per_game = away_stats.get('goals_for', 0) / away_matches
        home_conceded_per_game = home_stats.get('goals_against', 0) / home_matches
        away_conceded_per_game = away_stats.get('goals_against', 0) / away_matches
        
        # Predict scores based on attack and defense
        # Home score = home team's attack * away team's defense weakness + home advantage
        predicted_home_score = max(0, round(
            (home_goals_per_game * 0.7 + away_conceded_per_game * 0.3) * 1.1
        ))
        
        # Away score = away team's attack * home team's defense
        predicted_away_score = max(0, round(
            (away_goals_per_game * 0.7 + home_conceded_per_game * 0.3) * 0.9
        ))
        
        # Ensure at least 0 goals
        predicted_home_score = max(0, min(predicted_home_score, 5))  # Cap at 5
        predicted_away_score = max(0, min(predicted_away_score, 5))  # Cap at 5
        
        if home_strength > away_strength + 10:
            result = "HOME_WIN"
            home_prob = 0.6
            draw_prob = 0.25
            away_prob = 0.15
            # Adjust scores for home win
            if predicted_home_score <= predicted_away_score:
                predicted_home_score = predicted_away_score + 1
        elif away_strength > home_strength + 10:
            result = "AWAY_WIN"
            home_prob = 0.15
            draw_prob = 0.25
            away_prob = 0.6
            # Adjust scores for away win
            if predicted_away_score <= predicted_home_score:
                predicted_away_score = predicted_home_score + 1
        else:
            result = "DRAW"
            home_prob = 0.35
            draw_prob = 0.35
            away_prob = 0.30
            # Make scores closer for draw
            avg_score = (predicted_home_score + predicted_away_score) / 2
            predicted_home_score = max(0, round(avg_score))
            predicted_away_score = max(0, round(avg_score))
        
        return {
            "home_team": home_team,
            "away_team": away_team,
            "predicted_result": result,
            "home_win_probability": home_prob,
            "draw_probability": draw_prob,
            "away_win_probability": away_prob,
            "predicted_home_score": predicted_home_score,
            "predicted_away_score": predicted_away_score,
            "confidence": max(home_prob, draw_prob, away_prob)
        }


class SeasonPredictor:
    """Predicts entire season standings"""
    
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.db = Database()
        # Get the backend directory (parent of models directory)
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(backend_dir, "models", "trained", "season_predictor.pkl")
    
    def load_model(self):
        """Load trained season prediction model"""
        try:
            # Ensure models directory exists
            models_dir = os.path.dirname(self.model_path)
            os.makedirs(models_dir, exist_ok=True)
            
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                self.model_loaded = True
        except Exception as e:
            print(f"Error loading season model: {e}")
    
    async def predict_season(self):
        """Predict season standings"""
        from datetime import datetime
        from data.data_fetcher import DataFetcher
        
        data_fetcher = DataFetcher()
        
        # Get teams from database, or fetch from API if not available
        teams = self.db.get_teams()
        if not teams or len(teams) < 20:
            # Fetch all teams from API to ensure we have all 20
            teams_data = await data_fetcher.fetch_teams()
            if teams_data:
                self.db.save_teams(teams_data)
                teams = self.db.get_teams()
        
        if not teams:
            return {
                "season": "2024/25",
                "predicted_standings": [],
                "predicted_champion": "Unknown",
                "predicted_relegated": [],
                "updated_at": datetime.now()
            }
        
        # Get current season data for ALL teams
        # Use database stats first (faster), only fetch from API if missing
        standings = []
        for team in teams:
            # Try database first (much faster)
            stats = self.db.get_team_stats(team['name'])
            
            # If no stats in database, try to fetch from API
            if not stats:
                stats = await data_fetcher.fetch_team_stats(team['name'])
                if stats:
                    self.db.save_team_stats(team['name'], stats)
            
            # Simple prediction: extrapolate current form
            matches_played = stats.get('matches_played', 0) if stats else 0
            current_points = stats.get('points', 0) if stats else 0
            current_position = stats.get('position', 0) if stats else 0
            
            if matches_played > 0:
                points_per_game = current_points / matches_played
                predicted_points = points_per_game * 38  # 38 games in a season
            else:
                # Default prediction for teams without matches played yet
                predicted_points = 50  # Average points
            
            standings.append({
                "team": team['name'],
                "predicted_points": round(predicted_points, 1),
                "current_points": current_points,
                "current_position": current_position if current_position > 0 else 20  # Default to bottom if no position
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

