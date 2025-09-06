# Deploy to Render - Step by Step

## 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

## 2. Deploy on Render
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Fill in these settings:
   - **Name**: `pii-privacy-server`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python api_server.py`
   - **Plan**: Free

## 3. Add Environment Variable
- In Render dashboard → Environment
- Add: `GEMINI_API_KEY` = `AIzaSyCkc83znIV2wqNeV53llqdQU5slPcvCu9U`

## 4. Deploy
- Click "Create Web Service"
- Wait 2-3 minutes for deployment

## 5. Get Your URL
- Copy the URL: `https://your-app-name.onrender.com`

## 6. Update Flutter App
Replace in `lib/services/api_service.dart`:
```dart
static const String baseUrl = 'https://your-app-name.onrender.com/api';
```