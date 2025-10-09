# 🚀 Google Cloud Platform Deployment Guide

## ⚡ Cloud Run Deployment (RECOMMENDED)

**Total Time**: 5-10 minutes
**Cost**: FREE (2M requests/month free tier)

---

## 📋 Prerequisites (3 minutes)

### 1. Install Google Cloud CLI
Download from: https://cloud.google.com/sdk/docs/install

**Windows Quick Install**:
```powershell
# Download and run the installer
# OR use Chocolatey:
choco install gcloudsdk
```

### 2. Login to GCP
```powershell
gcloud auth login
```

### 3. Create/Select Project
```powershell
# Create new project (replace PROJECT_ID with your choice)
gcloud projects create finance-chatbot-demo --name="Finance ChatBot"

# Set as active project
gcloud config set project finance-chatbot-demo

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

---

## 🚀 Deploy to Cloud Run (5 minutes)

### Option A: Direct Deploy (Easiest)

```powershell
# Navigate to project
cd "C:\Users\Ayush Kumar\Downloads\ChatBot-Finance\ChatBot-Finance"

# Deploy directly from source
gcloud run deploy finance-chatbot `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars "FLASK_ENV=production,GEMINI_API_KEY=AIzaSyDOzogpt08zzEDyeQuozXasjXkymljwA0M,SECRET_KEY=your-secret-key-here,JWT_SECRET_KEY=your-jwt-secret-here"
```

**That's it!** Cloud Run will:
1. Build your Docker container (2-3 min)
2. Deploy it (1-2 min)
3. Give you a public URL

### Option B: Build Then Deploy (More Control)

```powershell
# Build container
gcloud builds submit --tag gcr.io/finance-chatbot-demo/finance-chatbot

# Deploy container
gcloud run deploy finance-chatbot `
  --image gcr.io/finance-chatbot-demo/finance-chatbot `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars "FLASK_ENV=production,GEMINI_API_KEY=AIzaSyDOzogpt08zzEDyeQuozXasjXkymljwA0M,SECRET_KEY=your-secret-key,JWT_SECRET_KEY=your-jwt-secret"
```

---

## 🎯 After Deployment

### 1. Get Your URL
Cloud Run will output: `Service URL: https://finance-chatbot-xxxxx-uc.a.run.app`

### 2. Test It
Open the URL in browser or:
```powershell
gcloud run services describe finance-chatbot --region us-central1 --format "value(status.url)"
```

### 3. Create Demo Data
Your app auto-creates demo data on first run, but if needed:
```powershell
# Get service URL
$URL = gcloud run services describe finance-chatbot --region us-central1 --format "value(status.url)"

# Trigger demo data creation
Invoke-WebRequest -Uri "$URL/api/create-demo-data" -Method POST
```

### 4. Login
- URL: Your Cloud Run URL
- Username: `demo`
- Password: `demo123`

---

## 🔧 Managing Your Deployment

### View Logs
```powershell
gcloud run services logs read finance-chatbot --region us-central1
```

### Update Environment Variables
```powershell
gcloud run services update finance-chatbot `
  --region us-central1 `
  --update-env-vars "NEW_VAR=value"
```

### Redeploy After Code Changes
```powershell
gcloud run deploy finance-chatbot --source . --region us-central1
```

### Delete Service (Clean Up)
```powershell
gcloud run services delete finance-chatbot --region us-central1
```

---

## 💡 Advantages of Cloud Run

✅ **Fast deployment** (5-10 minutes)
✅ **Auto-scaling** (0 to 1000+ instances)
✅ **Pay per use** (free tier: 2M requests/month)
✅ **No server management**
✅ **HTTPS automatically**
✅ **Google infrastructure**
✅ **Perfect for demos**

---

## 🐛 Troubleshooting

### Issue: "gcloud: command not found"
**Solution**: Restart terminal after installing Cloud SDK

### Issue: Build fails
**Solution**: Check Dockerfile syntax, ensure requirements.txt is valid

### Issue: Database errors
**Solution**: Database auto-creates in /tmp (Cloud Run supports this)

### Issue: Cold starts
**Solution**: Normal for free tier (first request may take 2-3 seconds)

### Issue: Port binding errors
**Solution**: Cloud Run sets $PORT automatically, our Dockerfile uses it

---

## 📊 Comparison with Other Platforms

| Platform | Deploy Time | Free Tier | Difficulty |
|----------|-------------|-----------|------------|
| **Cloud Run** | 5-10 min | 2M requests | ⭐⭐⭐⭐⭐ |
| App Engine | 10-15 min | Limited | ⭐⭐⭐⭐ |
| Render | 3-5 min | 750 hrs | ⭐⭐⭐⭐⭐ |
| PythonAnywhere | 15 min | 1 app | ⭐⭐⭐⭐ |

---

## 🎤 For Your Hackathon

**Why mention GCP**:
- "Deployed on Google Cloud Run for enterprise-grade scalability"
- "Using Google's Gemini AI API for intelligent responses"
- "Auto-scales from 0 to thousands of users instantly"
- "Production-ready cloud infrastructure"

**Impressive factors**:
- Google Cloud Platform (recognized brand)
- Containerized deployment (Docker)
- Auto-scaling architecture
- Cloud-native design

---

## ✅ Quick Command Summary

```powershell
# One-command deployment
gcloud run deploy finance-chatbot --source . --region us-central1 --allow-unauthenticated

# View URL
gcloud run services describe finance-chatbot --region us-central1 --format "value(status.url)"

# View logs
gcloud run services logs read finance-chatbot --region us-central1 --limit 50
```

---

**Your app will be live at**: `https://finance-chatbot-xxxxx-uc.a.run.app`

**Total setup time**: ~10 minutes from zero to deployed! 🚀
