"""
Training script for Premier League prediction models
Run this script to train/retrain the ML models
"""
import os
import sys
import pickle
import asyncio
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data_fetcher import DataFetcher
from data.feature_engineering import FeatureEngineer
from database.db import Database

async def collect_training_data():
    """Collect historical match data for training"""
    print("Collecting training data...")
    
    data_fetcher = DataFetcher()
    db = Database()
    feature_engineer = FeatureEngineer()
    
    # Fetch recent matches
    matches = await data_fetcher.fetch_recent_matches(limit=200)
    
    if not matches:
        print("Warning: No matches found. Using mock data for demonstration.")
        return create_mock_training_data()
    
    # Fetch teams and their stats
    teams = await data_fetcher.fetch_teams()
    db.save_teams(teams)
    
    # Fetch stats for each team
    for team in teams:
        stats = await data_fetcher.fetch_team_stats(team['name'])
        if stats:
            db.save_team_stats(team['name'], stats)
    
    # Build training dataset
    X = []
    y = []
    X_scores = []
    y_scores = []
    
    for match in matches:
        if match.get('home_score') is None or match.get('away_score') is None:
            continue
        
        home_team = match['home_team']
        away_team = match['away_team']
        
        # Get team stats at the time (simplified - using current stats)
        home_stats = db.get_team_stats(home_team)
        away_stats = db.get_team_stats(away_team)
        
        if not home_stats or not away_stats:
            continue
        
        # Extract features
        features = feature_engineer.extract_features_from_match(match, home_stats, away_stats)
        X.append(features)
        
        # Determine outcome label (0: HOME_WIN, 1: DRAW, 2: AWAY_WIN)
        home_score = match['home_score']
        away_score = match['away_score']
        
        if home_score > away_score:
            y.append(0)
        elif home_score == away_score:
            y.append(1)
        else:
            y.append(2)
        
        # Score prediction targets
        X_scores.append(features)
        y_scores.append([home_score, away_score])
    
    if len(X) < 10:
        print("Not enough training data. Using mock data.")
        return create_mock_training_data()
    
    return np.array(X), np.array(y), np.array(X_scores), np.array(y_scores)


def create_mock_training_data():
    """Create mock training data for demonstration when API is unavailable"""
    print("Creating mock training data...")
    np.random.seed(42)
    
    n_samples = 500
    n_features = 25
    
    X = np.random.rand(n_samples, n_features)
    
    # Add some logic to make predictions more realistic
    X[:, 0] = np.random.uniform(0, 100, n_samples)  # Home points
    X[:, 1] = np.random.uniform(0, 100, n_samples)  # Away points
    X[:, 2] = X[:, 0] - X[:, 1]  # Point difference
    
    # Generate outcomes based on point difference
    y = []
    y_scores = []
    X_scores = []
    
    for i in range(n_samples):
        point_diff = X[i, 2]
        if point_diff > 10:
            y.append(0)  # Home win
            home_score = np.random.randint(2, 4)
            away_score = np.random.randint(0, 2)
        elif point_diff < -10:
            y.append(2)  # Away win
            home_score = np.random.randint(0, 2)
            away_score = np.random.randint(2, 4)
        else:
            y.append(1)  # Draw
            score = np.random.randint(0, 3)
            home_score = score
            away_score = score
        
        y_scores.append([home_score, away_score])
        X_scores.append(X[i])
    
    return X, np.array(y), np.array(X_scores), np.array(y_scores)


async def train_models():
    """Train the prediction models"""
    print("Starting model training...")
    
    # Collect data
    X, y, X_scores, y_scores = await collect_training_data()
    
    print(f"Training with {len(X)} samples")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    X_train_scores, X_test_scores, y_train_scores, y_test_scores = train_test_split(
        X_scores, y_scores, test_size=0.2, random_state=42
    )
    
    # Train outcome prediction model
    print("Training outcome prediction model...")
    try:
        # Try XGBoost first, fallback to Random Forest
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
    except:
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Outcome prediction accuracy: {accuracy:.2%}")
    print(classification_report(y_test, y_pred, 
          target_names=['HOME_WIN', 'DRAW', 'AWAY_WIN']))
    
    # Save outcome model
    os.makedirs("models/trained", exist_ok=True)
    with open("models/trained/match_predictor.pkl", "wb") as f:
        pickle.dump(model, f)
    print("Saved outcome prediction model")
    
    # Train score prediction model
    print("Training score prediction model...")
    try:
        score_model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
    except:
        score_model = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            random_state=42
        )
    
    score_model.fit(X_train_scores, y_train_scores)
    
    # Evaluate score prediction
    y_pred_scores = score_model.predict(X_test_scores)
    mae = np.mean(np.abs(y_pred_scores - y_test_scores))
    print(f"Score prediction MAE: {mae:.2f} goals")
    
    # Save score model
    with open("models/trained/score_predictor.pkl", "wb") as f:
        pickle.dump(score_model, f)
    print("Saved score prediction model")
    
    print("\nTraining completed successfully!")
    print("Models saved to models/trained/")


if __name__ == "__main__":
    asyncio.run(train_models())

