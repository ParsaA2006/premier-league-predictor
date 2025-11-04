# Setup Guide

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Step 1: Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env` (if you have an API key)
   - Or create a `.env` file manually:
```
FOOTBALL_DATA_API_KEY=your_api_key_here
```
   - Get a free API key at: https://www.football-data.org/
   - Note: The system works without an API key but will use mock data

5. Train the ML models (optional but recommended):
```bash
python scripts/train_models.py
```
This will create trained models in `models/trained/`. If you skip this, the system will use simple rule-based predictions.

6. Start the backend server:
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`

### Step 2: Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```
The frontend will be available at `http://localhost:3000`

## API Documentation

Once the backend is running, visit:
- API Docs: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

## Features

### 1. Match Predictor
- Select two teams to predict match outcome
- View win probabilities for home, draw, and away
- Get predicted scores

### 2. Season Predictor
- See predicted final league standings
- View predicted champion and relegated teams
- Compare current vs predicted positions

### 3. Team Stats
- View detailed team statistics
- See recent form
- Analyze team performance metrics

## Troubleshooting

### Models not loading
- Run `python scripts/train_models.py` to train models
- Ensure `models/trained/` directory exists

### API errors
- Check if Football-Data.org API key is valid
- The system will work with mock data if API is unavailable
- Check rate limits (free tier has limits)

### Frontend not connecting to backend
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify proxy settings in `frontend/vite.config.ts`

## Production Deployment

### Backend
- Use a production ASGI server like Gunicorn with Uvicorn workers
- Set up proper environment variables
- Use a production database (PostgreSQL recommended)
- Enable HTTPS

### Frontend
- Build the frontend: `npm run build`
- Serve the `dist` folder with a web server
- Configure API URL in environment variables

## Next Steps

1. Get a Football-Data.org API key for real data
2. Train models with more historical data
3. Fine-tune ML models for better accuracy
4. Add more features (player stats, head-to-head history, etc.)
5. Deploy to a cloud platform

