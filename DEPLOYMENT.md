# Deploy PII Security App

## Quick Deploy to Render

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Connect GitHub repository
   - Choose "Web Service"
   - Build Command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - Start Command: `gunicorn api_server:app`

## Alternative: Deploy to Heroku

1. **Install Heroku CLI**
2. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku run python -m spacy download en_core_web_sm
   ```

## Environment Variables

Set these on your hosting platform:
- `GEMINI_API_KEY` (optional - for LLM features)
- `PORT` (auto-set by most platforms)

## Files for Deployment

✅ `requirements.txt` - Python dependencies
✅ `Procfile` - Start command
✅ `runtime.txt` - Python version
✅ Updated `api_server.py` - Production ready

## Flutter App Connection

The app is now configured to connect to:
`https://pii-security-app.onrender.com/api`

Update the URL in `network_service.dart` if using different hosting.