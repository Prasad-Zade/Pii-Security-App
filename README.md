# PII Privacy Protection System

## Final Year Project - Functional Dependency-Based Privacy Masking

### 🚀 Quick Deploy

```bash
git add .
git commit -m "Clean deployment with functional model"
git push origin main
```

### 📱 Flutter App
- Location: `flutter_application_1/`
- API URL: `https://pii-security-app.onrender.com/api`

### 🧠 Features
- Trained functional dependency model in `functional_model/`
- Smart PII masking based on query context
- Flutter mobile app with chat interface
- Real-time privacy scoring

### 🔧 API Endpoints
- `POST /api/process` - Process text
- `GET /api/sessions` - Get chat sessions
- `POST /api/sessions/{id}/process` - Process in session

### 📊 Model Performance
- Uses your trained DistilBERT model
- Fallback to rule-based logic if model unavailable
- Context-aware entity masking decisions