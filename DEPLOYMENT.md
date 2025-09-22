# Deployment Guide - PII Privacy Protection System

## 🚀 Render Deployment

### Prerequisites
- GitHub account
- Render account (free tier available)
- Project pushed to GitHub repository

### Step 1: Prepare Repository
```bash
# Ensure all files are committed
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Deploy to Render

1. **Login to Render Dashboard**
   - Go to https://render.com
   - Sign in with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the PII Privacy Protection repository

3. **Configure Service**
   - **Name:** `pii-security-app`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Instance Type:** Free (or paid for better performance)

4. **Environment Variables**
   - `PYTHON_VERSION`: `3.11.0`
   - `PORT`: `5000` (auto-configured by Render)

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be available at: `https://pii-security-app.onrender.com`

### Step 3: Verify Deployment

Test the API endpoints:
```bash
# Health check
curl https://pii-security-app.onrender.com/api/health

# Process text
curl -X POST https://pii-security-app.onrender.com/api/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Customer John Smith, what is AI?"}'
```

## 📱 Flutter App Integration

### Update API Base URL
The Flutter app is already configured to use the Render URL:
```dart
static const String baseUrl = 'https://pii-security-app.onrender.com/api';
```

### Build Flutter App
```bash
cd flutter_application_1

# For Android
flutter build apk --release

# For iOS
flutter build ios --release

# For Web
flutter build web
```

### Test Integration
1. Run Flutter app
2. Test chat functionality
3. Verify API calls to Render backend

## 🔧 API Endpoints

### Core Endpoints
- `GET /api/health` - Health check
- `POST /api/process` - Process text with PII masking

### Flutter-Specific Endpoints
- `GET /api/sessions` - Get chat sessions
- `POST /api/sessions` - Create new session
- `GET /api/sessions/{id}/messages` - Get session messages
- `POST /api/sessions/{id}/process` - Process text in session
- `DELETE /api/sessions/{id}` - Delete session

### Web Interface
- `GET /` - Homepage
- `GET /demo` - Interactive demo
- `GET /about` - Project information

## 🔍 Monitoring & Debugging

### Render Dashboard
- View logs in real-time
- Monitor resource usage
- Check deployment status

### Common Issues
1. **Cold Start Delay:** First request may take 30+ seconds
2. **Memory Limits:** Free tier has 512MB RAM limit
3. **Build Timeouts:** Large dependencies may cause timeouts

### Solutions
- Use lighter ML models for production
- Implement caching for frequent requests
- Upgrade to paid tier for better performance

## 📊 Performance Optimization

### Backend Optimizations
```python
# Cache model loading
@lru_cache(maxsize=1)
def load_model():
    return AutoModelForSequenceClassification.from_pretrained(model_path)

# Implement request caching
from functools import lru_cache

@lru_cache(maxsize=100)
def process_cached_text(text_hash):
    return pii_system.process_text(text)
```

### Flutter Optimizations
```dart
// Implement request caching
class ApiCache {
  static final Map<String, dynamic> _cache = {};
  
  static Future<dynamic> getCached(String key, Future<dynamic> Function() request) async {
    if (_cache.containsKey(key)) {
      return _cache[key];
    }
    final result = await request();
    _cache[key] = result;
    return result;
  }
}
```

## 🔐 Security Considerations

### Production Security
- Enable HTTPS (automatic on Render)
- Implement rate limiting
- Add API authentication
- Validate all inputs
- Log security events

### Environment Variables
```bash
# Add to Render dashboard
SECRET_KEY=your-secret-key-here
API_RATE_LIMIT=100
MAX_TEXT_LENGTH=10000
```

## 📈 Scaling

### Horizontal Scaling
- Render auto-scales based on traffic
- Consider Redis for session storage
- Implement load balancing

### Database Integration
```python
# Add PostgreSQL for persistent storage
import psycopg2
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)
```

## 🚀 Production Checklist

- [ ] Repository pushed to GitHub
- [ ] Render service configured
- [ ] Environment variables set
- [ ] Health check endpoint working
- [ ] API endpoints tested
- [ ] Flutter app updated with production URL
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Performance monitoring setup
- [ ] Security measures in place

## 📞 Support

For deployment issues:
1. Check Render logs
2. Verify environment variables
3. Test API endpoints manually
4. Check Flutter network permissions
5. Review CORS configuration

## 🔄 Continuous Deployment

### Auto-Deploy Setup
1. Enable auto-deploy in Render dashboard
2. Connect to main branch
3. Automatic deployments on git push

### CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy to Render
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: echo "Auto-deploy configured in Render"
```