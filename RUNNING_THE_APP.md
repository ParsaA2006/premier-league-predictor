# Running the App - Quick Answers

## ✅ SQL/Database Setup

**YES, SQL is fully set up!** 

- Uses **SQLite** (file-based database, no server needed)
- Database file (`premier_league.db`) is **automatically created** in the `backend` directory when you first run the app
- Tables are created automatically on startup
- **You don't need to do anything** - it just works!

The database will be created at: `backend/premier_league.db`

---

## 🔑 API Key - Do You Need It?

### Short Answer: **NO, you don't need it to run the app!**

The app will work without an API key using **mock data**:
- ✅ 20 Premier League teams (Arsenal, Liverpool, Man City, etc.)
- ✅ Mock team statistics
- ✅ Predictions will work
- ✅ Frontend will display data

### But... For Real Data:

**YES, get an API key if you want:**
- Real-time match data
- Current team standings
- Actual upcoming matches
- Live statistics

### How to Get API Key (Free):

1. Go to https://www.football-data.org/
2. Sign up (free tier available)
3. Get your API key
4. Create `backend/.env` file:
   ```
   FOOTBALL_DATA_API_KEY=your_key_here
   ```

**The app works perfectly fine without it!** Mock data is included.

---

## 🚀 Quick Start (No API Key Needed)

### Terminal 1 - Backend:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python scripts/setup.py
uvicorn main:app --reload
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm install
npm run dev
```

Then open: **http://localhost:3000**

---

## 📊 What You'll See

**Without API Key:**
- 20 Premier League teams (mock data)
- Predictions work (using mock stats)
- Season predictions work
- Match predictions work

**With API Key:**
- Real current teams
- Real upcoming matches
- Real team statistics
- More accurate predictions

---

## ✅ Summary

| Item | Status | Action Needed |
|------|--------|---------------|
| SQL Database | ✅ Ready | None - auto-creates |
| API Key | ⚠️ Optional | Only if you want real data |
| Mock Data | ✅ Included | Works without API key |
| App Functionality | ✅ Full | Works either way |

**Bottom line:** You can run it right now without an API key! 🎉

