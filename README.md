# Premier League Predictor

An AI-powered Premier League prediction website that forecasts match outcomes, season standings, and team performance using machine learning models.

## Features

- **Match Predictions**: Predict individual match outcomes (Win/Draw/Loss) and scores
- **Season Predictions**: Forecast final league table standings
- **Head-to-Head Analysis**: Predict outcomes based on team history
- **Team Performance**: Analyze team statistics and form

## Tech Stack

- **Backend**: FastAPI (Python)
- **ML Models**: scikit-learn, XGBoost
- **Frontend**: React with TypeScript
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **Data Source**: Football-Data.org API (free tier available)

## Setup

### Backend Setup

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Add your Football-Data.org API key to .env
```

4. Run the backend:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

## API Endpoints

- `GET /api/predict/match/{home_team}/{away_team}` - Predict a specific match
- `GET /api/predict/season` - Predict entire season standings
- `GET /api/teams` - Get all teams
- `GET /api/matches` - Get upcoming matches
- `GET /api/stats/{team}` - Get team statistics

## Data Collection

The system fetches data from Football-Data.org API. You'll need to:
1. Sign up at https://www.football-data.org/
2. Get your free API key
3. Add it to `.env` file

## Model Training

Run the training script to update models:
```bash
cd backend
python scripts/train_models.py
```

