# Premier League Predictor - Project Overview

## Architecture

### Backend (FastAPI)
- **API Layer**: FastAPI with automatic OpenAPI documentation
- **ML Models**: XGBoost/Random Forest for predictions
- **Data Layer**: SQLite database for caching
- **Data Fetching**: Football-Data.org API integration
- **Feature Engineering**: Extracts 25+ features from team statistics

### Frontend (React + TypeScript)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development
- **State Management**: TanStack Query (React Query)
- **Styling**: CSS with modern gradient designs
- **Routing**: React Router for navigation

## Key Components

### 1. Match Predictor
- Predicts match outcomes (Home Win/Draw/Away Win)
- Provides win probabilities for each outcome
- Predicts scores (home and away)
- Confidence scores for predictions

### 2. Season Predictor
- Forecasts entire season standings
- Predicts champion and relegated teams
- Shows position changes from current standings

### 3. Team Statistics
- Current team performance metrics
- Recent form (last 5 matches)
- Goals for/against statistics
- Win rates and points per game

## Machine Learning Approach

### Features Used (25 features)
1. Team points (home, away, difference)
2. Goals for/against
3. Goal difference
4. Win/Draw/Loss records
5. Matches played
6. Goals per game
7. Win rates
8. Recent form (last 5 matches)
9. League position difference
10. Home advantage factor

### Models
- **Outcome Prediction**: XGBoost Classifier (3 classes: Home Win, Draw, Away Win)
- **Score Prediction**: XGBoost Regressor (predicts home and away scores)
- **Fallback**: Simple rule-based predictions if models not available

### Training Data
- Fetches historical match data from Football-Data.org API
- Uses 200+ recent completed matches for training
- Creates mock data if API unavailable (for demonstration)

## Data Flow

1. **Data Collection**: 
   - Fetches teams, matches, and statistics from Football-Data.org API
   - Stores in SQLite database for caching

2. **Feature Engineering**:
   - Extracts features from team statistics
   - Normalizes and prepares data for ML models

3. **Prediction**:
   - Loads trained models
   - Generates predictions based on features
   - Returns probabilities and scores

4. **Frontend Display**:
   - Fetches predictions via API
   - Displays results with visualizations
   - Shows probabilities and confidence scores

## API Endpoints

- `GET /` - API information
- `GET /api/teams` - List all teams
- `GET /api/matches` - Upcoming matches
- `GET /api/predict/match/{home_team}/{away_team}` - Match prediction
- `GET /api/predict/season` - Season prediction
- `GET /api/stats/{team}` - Team statistics
- `GET /api/health` - Health check

## Future Enhancements

1. **Better ML Models**:
   - Deep learning models (LSTM, Transformers)
   - Player statistics integration
   - Head-to-head history analysis
   - Weather and injury data

2. **More Features**:
   - Player performance predictions
   - Goal scorer predictions
   - Betting odds integration
   - Historical prediction accuracy tracking

3. **Performance**:
   - Real-time data updates
   - Caching improvements
   - Database optimization
   - API rate limit handling

4. **UI/UX**:
   - Interactive charts and graphs
   - Prediction history
   - Comparison tools
   - Mobile app version

## Technology Choices Rationale

- **FastAPI**: Fast, modern, auto-documentation, async support
- **XGBoost**: State-of-the-art gradient boosting, good for structured data
- **React**: Popular, component-based, great ecosystem
- **SQLite**: Simple, no setup required, good for development
- **Vite**: Fast development server, modern build tool

## Getting Started

See `SETUP.md` for detailed setup instructions, or `README.md` for quick start.

