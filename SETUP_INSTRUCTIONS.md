# Setup Instructions - Premier League Predictor

## ✅ What I Fixed

1. **Model Paths**: Fixed relative path issues - models now work regardless of where you run the server
2. **Directory Creation**: Models directory is automatically created if it doesn't exist
3. **Training Script**: Updated to use absolute paths

## 📋 Step-by-Step Setup

### Prerequisites
- **Python 3.8+** (check with `python3 --version`)
- **Node.js 16+** (check with `node --version`)
- **npm** (comes with Node.js)

---

## 🔧 Backend Setup

### Step 1: Navigate to backend directory
```bash
cd backend
```

### Step 2: Create virtual environment
```bash
python3 -m venv venv
```

### Step 3: Activate virtual environment

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run setup script (creates necessary directories)
```bash
python scripts/setup.py
```

### Step 6: (Optional) Set up API key

Create a `.env` file in the `backend` directory:
```bash
# Copy this template
echo "FOOTBALL_DATA_API_KEY=your_api_key_here" > .env
```

**Note:** The app works without an API key but will use mock data. To get real data:
1. Sign up at https://www.football-data.org/
2. Get your free API key
3. Add it to `.env` file

### Step 7: (Optional) Train ML models
```bash
python scripts/train_models.py
```

**Note:** This is optional. The app will work with simple predictions if models aren't trained yet.

### Step 8: Start the backend server
```bash
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Keep this terminal window open!**

---

## 🎨 Frontend Setup

### Step 1: Open a NEW terminal window
*(Keep the backend terminal running)*

### Step 2: Navigate to frontend directory
```bash
cd frontend
```

### Step 3: Install dependencies
```bash
npm install
```

This may take a few minutes the first time.

### Step 4: Start the frontend development server
```bash
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
```

---

## 🌐 Access the Application

1. **Frontend**: Open your browser and go to `http://localhost:3000`
2. **Backend API Docs**: Open `http://localhost:8000/docs` to see the API documentation

---

## ✅ Verification Checklist

- [ ] Backend server is running on port 8000
- [ ] Frontend server is running on port 3000
- [ ] Can access frontend at http://localhost:3000
- [ ] Can access API docs at http://localhost:8000/docs
- [ ] No errors in terminal windows

---

## 🐛 Troubleshooting

### Backend Issues

**"python3 is not recognized"**
- Make sure Python is installed
- Try `python` instead of `python3`

**"Module not found" errors**
- Make sure virtual environment is activated (you should see `(venv)`)
- Run `pip install -r requirements.txt` again

**Port 8000 already in use**
- Close the program using port 8000, or change the port:
```bash
uvicorn main:app --reload --port 8001
```
(Then update frontend `vite.config.ts` to point to port 8001)

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
- Check browser console for CORS errors

---

## 🎯 What You'll See

Once both are running:
- **Home Page**: Overview and upcoming matches
- **Match Predictor**: Select two teams to predict match outcome
- **Season Predictor**: See predicted final league standings
- **Team Stats**: View detailed team statistics

---

## 📝 Quick Command Reference

**Backend:**
```bash
cd backend
source venv/bin/activate  # Mac/Linux
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

---

Enjoy predicting! 🎯⚽

