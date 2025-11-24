# Deployment Guide - Premier League Predictor

## 🚀 Railway Deployment

This guide will help you deploy the Premier League Predictor to Railway.

### Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app) (free tier available)
2. **GitHub Account**: Your code should be in a GitHub repository
3. **API Key**: Your Football-Data.org API key

---

## Step 1: Prepare Your Repository

Make sure your code is pushed to GitHub:
```bash
git add .
git commit -m "Add Docker and Railway deployment configuration"
git push origin main
```

---

## Step 2: Deploy Backend to Railway

### Option A: Using Railway Dashboard (Recommended)

1. **Go to Railway**: https://railway.app
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your repository**
5. **Railway will detect the Dockerfile automatically**

### Option B: Using Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to existing project or create new
railway link

# Deploy
railway up
```

### Configure Backend Service

1. **Set Root Directory**: 
   - In Railway dashboard, go to Settings
   - Set "Root Directory" to `backend`

2. **Set Environment Variables**:
   - Go to Variables tab
   - Add: `FOOTBALL_DATA_API_KEY=your_api_key_here`
   - Add: `ALLOWED_ORIGINS=https://your-frontend-url.railway.app,http://localhost:3000`
   - Add: `PORT=8000` (Railway sets this automatically, but good to have)

3. **Deploy**:
   - Railway will automatically build and deploy
   - Note the generated URL (e.g., `https://premier-league-backend.railway.app`)

---

## Step 3: Deploy Frontend to Railway

### Create Second Service

1. **In Railway project, click "+ New"**
2. **Select "GitHub Repo"** (same repo)
3. **Configure**:
   - Root Directory: `frontend`
   - Build Command: `npm run build` (handled by Dockerfile)
   - Start Command: (handled by Dockerfile)

### Configure Frontend Service

1. **Set Environment Variables**:
   - `VITE_API_URL=https://your-backend-url.railway.app`
   - Or update `vite.config.ts` to use environment variable

2. **Update Frontend API URL**:
   - The frontend needs to know where the backend is
   - Update `frontend/src/api/client.ts` or use environment variable

---

## Step 4: Update Frontend for Production

The frontend needs to know the backend URL. Update the API client:

```typescript
// frontend/src/api/client.ts
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.PROD 
    ? 'https://your-backend-url.railway.app' 
    : 'http://localhost:8000')
```

---

## Step 5: Test Deployment

1. **Backend Health Check**:
   - Visit: `https://your-backend-url.railway.app/api/health`
   - Should return: `{"status":"healthy",...}`

2. **Frontend**:
   - Visit your frontend URL
   - Should load the app
   - Try making a prediction

---

## Environment Variables Reference

### Backend:
- `FOOTBALL_DATA_API_KEY` - Your Football-Data.org API key (required)
- `ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins
- `PORT` - Port to run on (Railway sets this automatically)

### Frontend:
- `VITE_API_URL` - Backend API URL

---

## Local Testing with Docker

Before deploying, test locally:

```bash
# Build and run with docker-compose
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

---

## Troubleshooting

### Backend Issues:
- **Port binding**: Railway sets PORT automatically, make sure your code uses `os.getenv("PORT")`
- **CORS errors**: Add your frontend URL to `ALLOWED_ORIGINS`
- **Database**: SQLite works, but consider Railway Postgres for production

### Frontend Issues:
- **API connection**: Check `VITE_API_URL` is set correctly
- **Build errors**: Check Dockerfile build stage
- **404 on routes**: Make sure nginx.conf has SPA routing configured

### General:
- **Logs**: Check Railway logs in dashboard
- **Build logs**: Check build output for errors
- **Environment variables**: Verify all are set correctly

---

## Production Considerations

1. **Database**: Consider upgrading to PostgreSQL (Railway Postgres addon)
2. **Caching**: Add Redis for API response caching
3. **Monitoring**: Set up Railway monitoring/alerts
4. **Backups**: Configure database backups
5. **SSL**: Railway provides SSL automatically

---

## Cost Estimate

**Railway Free Tier**:
- $5 free credit per month
- Should be enough for this project
- Pay-as-you-go after that

**Typical Usage**:
- Backend: ~$5-10/month
- Frontend: ~$2-5/month
- Total: ~$7-15/month (or free if under limits)

---

## Next Steps

1. ✅ Deploy backend
2. ✅ Deploy frontend
3. ✅ Test everything works
4. ✅ Update resume with live URL!
5. 🎉 Share your deployed app!

---

## Useful Commands

```bash
# View logs
railway logs

# Open shell in container
railway shell

# View variables
railway variables

# Redeploy
railway up
```

---

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Your project README for local setup

