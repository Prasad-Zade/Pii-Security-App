# Quick Deployment Fix

## Issue
PyTorch version 2.1.0 not available on Python 3.13.4

## Solution
1. Updated requirements.txt with compatible versions
2. Created minimal requirements for faster deployment
3. Simplified app.py to remove heavy dependencies

## Deploy Steps
```bash
git add .
git commit -m "Fix deployment requirements"
git push origin main
```

## Render Configuration
- Use `requirements_minimal.txt` for build command
- Faster deployment without ML dependencies
- Core API functionality maintained

## Test After Deployment
```bash
curl https://your-app.onrender.com/api/health
```