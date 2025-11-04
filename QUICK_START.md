# Quick Start Guide - Running the Application

## Prerequisites
- Python 3.8 or higher (download from https://www.python.org/)
- Node.js 16 or higher (download from https://nodejs.org/)
- npm (comes with Node.js)

## Backend Setup & Run

### Step 1: Navigate to backend folder
```bash
cd backend
```

### Step 2: Create virtual environment
```bash
python -m venv venv
```

### Step 3: Activate virtual environment
**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Create necessary directories
```bash
python scripts/setup.py
```

### Step 6: (Optional) Train ML models
```bash
python scripts/train_models.py
```
*Note: This step is optional. The app will work with simple predictions if models aren't trained yet.*

### Step 7: (Optional) Set up API key
Create a file named `.env` in the `backend` folder:
```
FOOTBALL_DATA_API_KEY=your_api_key_here
```
*Note: You can skip this step - the app works without an API key but will use mock data.*

### Step 8: Start the backend server
```bash
uvicorn main:app --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Keep this terminal window open!**

---

## Frontend Setup & Run

### Step 1: Open a NEW terminal window
*(Keep the backend terminal running)*

### Step 2: Navigate to frontend folder
```bash
cd frontend
```

### Step 3: Install dependencies
```bash
npm install
```
*This may take a few minutes the first time*

### Step 4: Start the frontend development server
```bash
npm run dev
```

You should see output like:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

---

## Access the Application

1. **Frontend**: Open your browser and go to `http://localhost:3000`
2. **Backend API Docs**: Open `http://localhost:8000/docs` to see the API documentation

---

## Troubleshooting

### Backend Issues

**"python is not recognized"**
- Make sure Python is installed and added to PATH
- Try `python3` instead of `python`

**"Module not found" errors**
- Make sure virtual environment is activated (you should see `(venv)` in your terminal)
- Run `pip install -r requirements.txt` again

**Port 8000 already in use**
- Close the program using port 8000, or change the port:
```bash
uvicorn main:app --reload --port 8001
```

### Frontend Issues

**"npm is not recognized"**
- Make sure Node.js is installed
- Restart your terminal after installing Node.js

**"npm install" fails**
- Try deleting `node_modules` folder and `package-lock.json`, then run `npm install` again

**Port 3000 already in use**
- Vite will automatically use the next available port (like 3001)

**Frontend can't connect to backend**
- Make sure backend is running on port 8000
- Check that you see `Uvicorn running on http://127.0.0.1:8000` in backend terminal

---

## What You'll See

Once both are running:
- **Home Page**: Overview and upcoming matches
- **Match Predictor**: Select two teams to predict match outcome
- **Season Predictor**: See predicted final league standings
- **Team Stats**: View detailed team statistics

Enjoy predicting! 🎯⚽

