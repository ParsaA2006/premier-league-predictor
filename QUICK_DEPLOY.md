# Quick Deploy to Railway 🚀

## Prerequisites
- GitHub account
- Railway account (free at railway.app)
- Your Football-Data.org API key

## Steps (5 minutes)

### 1. Push to GitHub
```bash
git add .
git commit -m "Add Docker and Railway deployment"
git push origin main
```

### 2. Deploy Backend
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. **Important**: In Settings → Root Directory, set to `backend`
5. Go to Variables tab, add:
   - `FOOTBALL_DATA_API_KEY` = your API key
   - `ALLOWED_ORIGINS` = `*` (or your frontend URL later)
6. Railway will auto-deploy! Note the URL (e.g., `https://premier-league-backend.railway.app`)

### 3. Deploy Frontend
1. In same Railway project, click "+ New" → "GitHub Repo" (same repo)
2. In Settings → Root Directory, set to `frontend`
3. Go to Variables tab, add:
   - `VITE_API_URL` = your backend URL from step 2
4. Railway will auto-deploy! Note the URL

### 4. Update Frontend API URL
Edit `frontend/src/api/client.ts` and replace:
```typescript
'https://your-backend-url.railway.app'  // Replace with your actual backend URL
```

Then push again:
```bash
git add frontend/src/api/client.ts
git commit -m "Update API URL for production"
git push
```

### 5. Done! 🎉
- Backend: `https://your-backend.railway.app`
- Frontend: `https://your-frontend.railway.app`
- API Docs: `https://your-backend.railway.app/docs`

## Test Locally First (Optional)

```bash
# Test with Docker locally
docker-compose up --build

# Should work at:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
```

## Troubleshooting

**Backend won't start?**
- Check Railway logs
- Verify `FOOTBALL_DATA_API_KEY` is set
- Check Root Directory is `backend`

**Frontend can't connect?**
- Verify `VITE_API_URL` matches backend URL
- Check CORS settings in backend
- Check browser console for errors

**Need help?**
- Check `DEPLOYMENT.md` for detailed guide
- Railway logs show all errors
- Railway Discord for support

## Cost
- Free tier: $5 credit/month
- Should be enough for this project
- Pay-as-you-go after

---

**That's it! Your app is now live on the internet! 🌐**

