# 🚀 Deployment Guide - Tokyo Trip Assistant

## Overview
This project uses **Railway** for production deployment with **GitHub Actions** for CI/CD automation.

## Architecture
- **Single Container**: FastAPI backend (port 8000) + Streamlit frontend (port 8501)
- **Public Access**: Streamlit UI only (Railway exposes port 8501)
- **Backend**: Internal API, not publicly accessible (security by design)

## Deployment Process

### 1. Setup Railway Project
1. Go to [Railway.app](https://railway.app)
2. Create new project from GitHub repository
3. Railway will auto-detect Dockerfile and deploy

### 2. Environment Variables (Set in Railway Dashboard)
```bash
# Required API Keys
OPENAI_API_KEY=your_openai_key_here
PINECONE_API_KEY=your_pinecone_key_here
OPENWEATHER_API_KEY=your_weather_key_here

# Environment
ENVIRONMENT=production
PORT=8501
```

### 3. GitHub Actions CI/CD Setup

**Required GitHub Secrets:**
- `RAILWAY_TOKEN`: Get from Railway dashboard → Account Settings → Tokens

**Workflow Triggers:**
- **Push to main**: Runs tests + deploys to production
- **Pull Request**: Runs tests only (no deployment)

### 4. Manual Deployment Commands

```bash
# Install Railway CLI
curl -fsSL https://railway.app/install.sh | sh

# Login to Railway
railway login

# Link to your project (first time only)
railway link

# Deploy manually
railway up

# View logs
railway logs

# Open deployed app
railway open
```

## Health Checks

### Local Testing
```bash
# Start with Docker
docker-compose up --build

# Check health
curl http://localhost:8000/health  # Backend health
curl http://localhost:8501/_stcore/health  # Frontend health
```

### Production Monitoring
- **Railway Health Check**: Automatic via `/_stcore/health`
- **Backend Health**: Internal only (not publicly accessible)
- **Uptime**: Railway provides built-in monitoring

## CI/CD Pipeline Status

[![Deploy to Railway](https://github.com/yourusername/tokyo-trip-assistant/actions/workflows/deploy.yml/badge.svg)](https://github.com/yourusername/tokyo-trip-assistant/actions/workflows/deploy.yml)

## Troubleshooting

### Common Issues:
1. **Build Fails**: Check environment variables are set
2. **Health Check Fails**: Ensure start.sh is executable
3. **API Keys**: Verify all required keys are configured

### Debug Commands:
```bash
# View Railway logs
railway logs --tail

# Check service status
railway status

# Restart service
railway up --detach
```

## Production URLs
- **Live Demo**: `https://your-app-name.railway.app`
- **API Health**: Not publicly accessible (internal only)
- **Uptime Status**: Available in Railway dashboard

---

**Note**: Backend API (port 8000) is intentionally not exposed publicly for security. All user interaction happens through the Streamlit interface.