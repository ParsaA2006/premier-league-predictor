import asyncio
from typing import Optional, List
import numpy as np
from database.db import Database

class FeatureEngineer:
    """Creates features for ML models from match and team data"""
    
    def __init__(self):
        self.db = Database()
    
    async def get_match_features(self, home_team: str, away_team: str) -> Optional[List[float]]:
        """Extract features for a match prediction"""
        home_stats = self.db.get_team_stats(home_team)
        away_stats = self.db.get_team_stats(away_team)
        
        if not home_stats or not away_stats:
            return None
        
        features = []
        
        # Points features
        features.append(home_stats.get('points', 0))
        features.append(away_stats.get('points', 0))
        features.append(home_stats.get('points', 0) - away_stats.get('points', 0))
        
        # Goal statistics
        features.append(home_stats.get('goals_for', 0))
        features.append(away_stats.get('goals_for', 0))
        features.append(home_stats.get('goals_against', 0))
        features.append(away_stats.get('goals_against', 0))
        features.append(home_stats.get('goal_diff', 0))
        features.append(away_stats.get('goal_diff', 0))
        
        # Win/Draw/Loss records
        features.append(home_stats.get('wins', 0))
        features.append(away_stats.get('wins', 0))
        features.append(home_stats.get('draws', 0))
        features.append(away_stats.get('draws', 0))
        features.append(home_stats.get('losses', 0))
        features.append(away_stats.get('losses', 0))
        
        # Matches played
        home_matches = home_stats.get('matches_played', 1)
        away_matches = away_stats.get('matches_played', 1)
        features.append(home_matches)
        features.append(away_matches)
        
        # Goals per game
        features.append(home_stats.get('goals_for', 0) / max(home_matches, 1))
        features.append(away_stats.get('goals_for', 0) / max(away_matches, 1))
        features.append(home_stats.get('goals_against', 0) / max(home_matches, 1))
        features.append(away_stats.get('goals_against', 0) / max(away_matches, 1))
        
        # Win rate
        features.append(home_stats.get('wins', 0) / max(home_matches, 1))
        features.append(away_stats.get('wins', 0) / max(away_matches, 1))
        
        # Form (last 5 matches) - convert to numeric
        home_form = self._form_to_numeric(home_stats.get('form', ''))
        away_form = self._form_to_numeric(away_stats.get('form', ''))
        features.append(home_form)
        features.append(away_form)
        
        # Position difference
        features.append(home_stats.get('position', 20) - away_stats.get('position', 20))
        
        # Home advantage (always 1 for home team)
        features.append(1.0)
        
        return features
    
    def _form_to_numeric(self, form_string: str) -> float:
        """Convert form string (e.g., 'WWDLW') to numeric value"""
        if not form_string:
            return 0.5
        
        form_points = {'W': 3, 'D': 1, 'L': 0}
        total_points = sum(form_points.get(char, 0) for char in form_string[:5])
        return total_points / (len(form_string[:5]) * 3) if form_string else 0.5
    
    def extract_features_from_match(self, match: dict, home_stats: dict, away_stats: dict) -> List[float]:
        """Extract features from a historical match for training"""
        features = []
        
        # Points features
        features.append(home_stats.get('points', 0))
        features.append(away_stats.get('points', 0))
        features.append(home_stats.get('points', 0) - away_stats.get('points', 0))
        
        # Goal statistics
        features.append(home_stats.get('goals_for', 0))
        features.append(away_stats.get('goals_for', 0))
        features.append(home_stats.get('goals_against', 0))
        features.append(away_stats.get('goals_against', 0))
        features.append(home_stats.get('goal_diff', 0))
        features.append(away_stats.get('goal_diff', 0))
        
        # Win/Draw/Loss records
        features.append(home_stats.get('wins', 0))
        features.append(away_stats.get('wins', 0))
        features.append(home_stats.get('draws', 0))
        features.append(away_stats.get('draws', 0))
        features.append(home_stats.get('losses', 0))
        features.append(away_stats.get('losses', 0))
        
        # Matches played
        home_matches = home_stats.get('matches_played', 1)
        away_matches = away_stats.get('matches_played', 1)
        features.append(home_matches)
        features.append(away_matches)
        
        # Goals per game
        features.append(home_stats.get('goals_for', 0) / max(home_matches, 1))
        features.append(away_stats.get('goals_for', 0) / max(away_matches, 1))
        features.append(home_stats.get('goals_against', 0) / max(home_matches, 1))
        features.append(away_stats.get('goals_against', 0) / max(away_matches, 1))
        
        # Win rate
        features.append(home_stats.get('wins', 0) / max(home_matches, 1))
        features.append(away_stats.get('wins', 0) / max(away_matches, 1))
        
        # Form
        home_form = self._form_to_numeric(home_stats.get('form', ''))
        away_form = self._form_to_numeric(away_stats.get('form', ''))
        features.append(home_form)
        features.append(away_form)
        
        # Position difference
        features.append(home_stats.get('position', 20) - away_stats.get('position', 20))
        
        # Home advantage
        features.append(1.0)
        
        return features

