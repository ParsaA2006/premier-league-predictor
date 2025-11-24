# Docker Setup Guide

## 🐳 What is Docker?

Docker packages your application and all its dependencies into a container that runs the same way everywhere.

## Local Development with Docker

### Prerequisites
- Docker Desktop installed (https://www.docker.com/products/docker-desktop)
- Docker Compose (comes with Docker Desktop)

### Quick Start

1. **Build and run everything**:
   ```bash
   docker-compose up --build
   ```

2. **Access the app**:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

3. **Stop everything**:
   ```bash
   docker-compose down
   ```

### Individual Services

**Run just backend**:
```bash
cd backend
docker build -t premier-league-backend .
docker run -p 8000:8000 -e FOOTBALL_DATA_API_KEY=your_key premier-league-backend
```

**Run just frontend**:
```bash
cd frontend
docker build -t premier-league-frontend .
docker run -p 3000:80 premier-league-frontend
```

## Docker Commands Reference

```bash
# Build images
docker-compose build

# Start services
docker-compose up

# Start in background (detached)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build

# View running containers
docker ps

# Execute command in container
docker-compose exec backend python scripts/train_models.py
```

## What Each Dockerfile Does

### Backend Dockerfile:
1. Uses Python 3.9 base image
2. Installs system dependencies
3. Installs Python packages from requirements.txt
4. Copies your code
5. Exposes port 8000
6. Runs uvicorn server

### Frontend Dockerfile:
1. **Build stage**: Uses Node to build React app
2. **Production stage**: Uses nginx to serve built files
3. Optimized for production (small image size)

## Environment Variables

Create a `.env` file in project root:
```env
FOOTBALL_DATA_API_KEY=your_api_key_here
```

Or set in docker-compose.yml directly.

## Troubleshooting

**Port already in use**:
```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Use port 8001 instead
```

**Container won't start**:
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend
```

**Rebuild from scratch**:
```bash
docker-compose down -v  # Remove volumes too
docker-compose build --no-cache
docker-compose up
```

**Database issues**:
- SQLite database is stored in a Docker volume
- Data persists between container restarts
- To reset: `docker-compose down -v`

## Production vs Development

**Development** (docker-compose.yml):
- Hot reload enabled
- Volume mounts for live code updates
- Development dependencies included

**Production** (Railway/Heroku):
- Optimized builds
- No volume mounts
- Production-only dependencies
- Smaller image sizes

## Next Steps

1. Test locally with `docker-compose up`
2. Push to GitHub
3. Deploy to Railway (see DEPLOYMENT.md)
4. 🎉 Your app is live!

