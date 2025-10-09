# 🚀 FinanceAI - Deployment Guide

## 📋 Table of Contents
1. [Quick Comparison](#quick-comparison)
2. [Option 1: Render (Recommended)](#option-1-render-recommended)
3. [Option 2: PythonAnywhere](#option-2-pythonanywhere)
4. [Option 3: Railway](#option-3-railway)
5. [Option 4: Heroku](#option-4-heroku)
6. [Option 5: Vercel (Frontend) + Railway (Backend)](#option-5-vercel--railway)
7. [Pre-Deployment Checklist](#pre-deployment-checklist)

---

## ⚡ Quick Comparison

| Platform | Free Tier | Ease | Speed | Database | Best For |
|----------|-----------|------|-------|----------|----------|
| **Render** ✅ | Yes (750hrs) | ⭐⭐⭐⭐⭐ | Fast | Persistent | **RECOMMENDED** |
| **PythonAnywhere** | Yes (Limited) | ⭐⭐⭐⭐ | Medium | Persistent | Beginners |
| **Railway** | $5 credit | ⭐⭐⭐⭐⭐ | Fast | Persistent | Production |
| **Heroku** | No (Paid) | ⭐⭐⭐⭐ | Fast | Persistent | Enterprise |
| **Vercel** | Yes | ⭐⭐⭐ | Very Fast | Need external | Hybrid |

**My Recommendation: Use Render** (100% free, easy, fast, production-ready)

---

## 🎯 Option 1: Render (RECOMMENDED) ⭐

### Why Render?
- ✅ **Completely FREE** (750 hours/month)
- ✅ **Auto-deploy** from GitHub on every push
- ✅ **Persistent database** (SQLite works)
- ✅ **HTTPS** included
- ✅ **Custom domain** support
- ✅ **Zero configuration** needed
- ✅ **Great for hackathons**

### Step-by-Step Deployment:

#### 1. **Prepare Your Repository**
```powershell
cd "c:\Users\Ayush Kumar\Downloads\ChatBot-Finance\ChatBot-Finance"

# Create Procfile for Render
New-Item -Path "Procfile" -ItemType File -Force
Add-Content -Path "Procfile" -Value "web: gunicorn app:app"

# Add gunicorn to requirements
Add-Content -Path "requirements.txt" -Value "gunicorn==21.2.0"

# Commit changes
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

#### 2. **Deploy on Render**

1. Go to https://render.com
2. Sign up with GitHub (free account)
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository: `INSVikrant54/Finance_ChatBot`
5. Configure:
   - **Name**: `financeai-chatbot` (or any name)
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Root Directory**: Leave blank
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

6. Click **"Advanced"** and add Environment Variables:
   ```
   FLASK_ENV=production
   GEMINI_API_KEY=AIzaSyDOzogpt08zzEDyeQuozXasjXkymljwA0M
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-here
   DATABASE_URL=sqlite:///instance/finance_chatbot.db
   ```

7. Click **"Create Web Service"**

8. Wait 5-10 minutes for deployment

9. Your app will be live at: `https://financeai-chatbot.onrender.com`

#### 3. **Initialize Demo Data** (IMPORTANT - Do This After First Deploy)

**What is Demo Data?**
The `create_demo_data.py` script creates:
- ✅ Demo user account (username: `demo`, password: `demo123`)
- ✅ Sample transactions (income, expenses, savings)
- ✅ Sample budgets (Food, Transport, Entertainment, etc.)
- ✅ Sample savings goals (Emergency Fund, Vacation)
- ✅ Pre-populated database so judges can see features immediately

**How to Create Demo Data on Render:**

1. **Go to your Render Dashboard**
2. **Click on your deployed service** (`financeai-chatbot`)
3. **Click "Shell"** tab (top menu)
4. **Run this command** in the Render Shell:
   ```bash
   python create_demo_data.py
   ```
5. **You'll see output like:**
   ```
   ✅ Created demo user
      Username: demo
      Password: demo123
   ✅ Created 15 sample transactions
   ✅ Created 5 budgets
   ✅ Created 2 savings goals
   🎉 Demo data created successfully!
   ```

**Now you can login with:**
- Username: `demo`
- Password: `demo123`

### ✅ Done! Your app is now live with demo data and ready for judges!

---

## 🐍 Option 2: PythonAnywhere

### Why PythonAnywhere?
- ✅ **FREE tier** available
- ✅ **Python-focused** hosting
- ✅ **Easy setup** for Flask apps
- ✅ **Good for beginners**
- ⚠️ Limited to 512MB storage
- ⚠️ Slower performance

### Step-by-Step:

1. **Sign up**: https://www.pythonanywhere.com (Free account)

2. **Upload Code**:
   - Go to **"Files"** tab
   - Upload your project files or clone from GitHub:
     ```bash
     git clone https://github.com/INSVikrant54/Finance_ChatBot.git
     ```

3. **Create Virtual Environment**:
   ```bash
   cd Finance_ChatBot
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Web App**:
   - Go to **"Web"** tab
   - Click **"Add a new web app"**
   - Choose **"Manual configuration"** → **Python 3.10**
   - Set **Source code**: `/home/yourusername/Finance_ChatBot`
   - Set **Working directory**: `/home/yourusername/Finance_ChatBot`

5. **Edit WSGI Configuration**:
   ```python
   import sys
   path = '/home/yourusername/Finance_ChatBot'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

6. **Reload Web App** and visit: `https://yourusername.pythonanywhere.com`

---

## 🚂 Option 3: Railway

### Why Railway?
- ✅ **$5 FREE credit** (lasts 1-2 months)
- ✅ **Fastest deployment** (under 2 minutes)
- ✅ **Auto-deploy** from GitHub
- ✅ **Best performance**
- ⚠️ Requires credit card after free credit

### Step-by-Step:

1. **Prepare Files**:
```powershell
# Create railway.json
@"
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
"@ | Out-File -FilePath railway.json -Encoding utf8

# Add to git
git add railway.json
git commit -m "Add Railway config"
git push
```

2. **Deploy**:
   - Go to https://railway.app
   - Click **"Start a New Project"**
   - Choose **"Deploy from GitHub repo"**
   - Select `Finance_ChatBot`
   - Add environment variables (same as Render)
   - Click **"Deploy"**

3. **Generate Domain**:
   - Go to **Settings** → **Generate Domain**
   - Your app: `https://financeai.railway.app`

---

## 🔷 Option 4: Heroku

### Why Heroku?
- ✅ **Most popular** (enterprise-grade)
- ✅ **Excellent documentation**
- ✅ **Add-ons ecosystem**
- ⚠️ **No free tier** (starts at $7/month)

### Quick Setup:

```powershell
# Install Heroku CLI
winget install Heroku.HerokuCLI

# Login
heroku login

# Create app
heroku create financeai-chatbot

# Add buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Open app
heroku open
```

---

## 🎨 Option 5: Vercel (Frontend) + Railway (Backend)

### Why Hybrid?
- ✅ **Blazing fast frontend** (Vercel's edge network)
- ✅ **Separate backend** for better scaling
- ✅ **Professional architecture**
- ⚠️ Requires splitting your app

### Architecture:
```
Vercel (Frontend) → API Calls → Railway (Flask Backend)
   ├── home.html
   ├── index.html
   └── static files
```

**Note**: This requires refactoring your app to separate frontend/backend. Not recommended for hackathons.

---

## ✅ Pre-Deployment Checklist

### 1. **Update config.py for Production**
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/finance_chatbot.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or os.urandom(24)
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    # Production settings
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
```

### 2. **Create .env File** (Don't commit!)
```env
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
GEMINI_API_KEY=AIzaSyDOzogpt08zzEDyeQuozXasjXkymljwA0M
FLASK_ENV=production
DATABASE_URL=sqlite:///instance/finance_chatbot.db
```

### 3. **Update .gitignore**
```
instance/
*.db
.env
__pycache__/
```

### 4. **Test Locally First**
```powershell
# Set production mode
$env:FLASK_ENV="production"

# Run app
python app.py

# Test at http://localhost:8080
```

### 5. **Create Procfile** (for Render/Heroku/Railway)
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

### 6. **Update requirements.txt**
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-CORS==4.0.0
google-generativeai==0.3.1
bcrypt==4.1.1
PyJWT==2.8.0
gunicorn==21.2.0
python-dotenv==1.0.0
```

---

## 🎯 My Final Recommendation

### **For Hackathon Demo: Use Render**

**Why?**
1. ✅ **100% Free forever**
2. ✅ **No credit card required**
3. ✅ **Auto-deploy from GitHub** (push = deploy)
4. ✅ **Persistent storage** (your database won't reset)
5. ✅ **Professional URL** (financeai.onrender.com)
6. ✅ **HTTPS included**
7. ✅ **Easy to demo** to judges
8. ✅ **5-minute setup**

### Quick Render Setup (Copy-Paste):

```powershell
# 1. Add gunicorn
cd "c:\Users\Ayush Kumar\Downloads\ChatBot-Finance\ChatBot-Finance"
Add-Content requirements.txt "`ngunicorn==21.2.0"

# 2. Create Procfile
"web: gunicorn app:app" | Out-File -FilePath Procfile -Encoding utf8

# 3. Push to GitHub
git add .
git commit -m "Deploy to Render"
git push origin main

# 4. Go to render.com → New Web Service → Connect GitHub repo
# 5. Click Deploy (takes 5 minutes)
# 6. Done! 🎉
```

---

## 🆘 Troubleshooting

### Issue: "Demo login not working" / "Invalid credentials"
**Cause**: You haven't run `create_demo_data.py` yet
**Solution**: 
1. Go to Render Dashboard → Your Service → Shell tab
2. Run: `python create_demo_data.py`
3. Wait for "✅ Demo data created successfully!" message
4. Now try logging in with username: `demo`, password: `demo123`

### Issue: "No transactions showing" / "Empty dashboard"
**Cause**: Database is empty, demo data not created
**Solution**: Same as above - run `create_demo_data.py` in Render Shell

### Issue: Database doesn't persist
**Solution**: Ensure you're using persistent storage:
```python
# In config.py
SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/finance_chatbot.db'
```

### Issue: Environment variables not working
**Solution**: Add them in platform dashboard, not in code

### Issue: Demo data missing after deploy
**Solution**: Run create_demo_data.py after first deployment:
```bash
# In platform's shell/terminal
python create_demo_data.py
```

### Issue: App sleeps on free tier
**Solution**: Normal behavior. First request takes 30 seconds to wake up.

---

## 📱 Share Your Deployed App

After deployment, share with judges:

```
🌟 FinanceAI - Live Demo
🔗 URL: https://financeai-chatbot.onrender.com
👤 Demo Login:
   Username: demo
   Password: demo123

📊 Features:
✅ AI-Powered Chatbot (Google Gemini 2.0)
✅ Smart Notifications
✅ Budget Management
✅ Savings Goals
✅ EMI Calculator
✅ ML Predictions

🔧 Tech Stack:
Backend: Python Flask
Frontend: HTML/CSS/JS
AI: Google Gemini 2.0 Flash
Database: SQLite
```

---

## 🎓 Learning Resources

- **Render Docs**: https://render.com/docs
- **Flask Deployment**: https://flask.palletsprojects.com/en/3.0.x/deploying/
- **Gunicorn Guide**: https://docs.gunicorn.org/

---

## ✨ Pro Tips

1. **Test Locally First**: Always test in production mode locally before deploying
2. **Use Environment Variables**: Never hardcode API keys
3. **Monitor Logs**: Check platform logs if something breaks
4. **Keep It Simple**: For hackathons, simpler deployment = less stress
5. **Have Backup**: Keep local version running during demo (just in case)

---

## 🏆 Ready to Deploy!

**Recommended Steps:**
1. ✅ Push latest code to GitHub
2. ✅ Sign up on Render.com
3. ✅ Connect GitHub repo
4. ✅ Click Deploy
5. ✅ Wait 5 minutes
6. ✅ Run create_demo_data.py in Render shell
7. ✅ Test your live app
8. ✅ Share URL with judges

**Good luck with your hackathon presentation! 🚀**

---

## 📋 Quick Reference: After Deployment Checklist

**After you deploy on Render, follow these steps in order:**

### Step 1: Wait for Deployment to Complete ⏳
- Check Render Dashboard until you see "Live" status (green)
- Usually takes 5-10 minutes

### Step 2: Create Demo Data 🎯
1. Go to Render Dashboard
2. Click your service name
3. Click **"Shell"** tab
4. Type: `python create_demo_data.py`
5. Press Enter
6. Wait for success message

### Step 3: Test Your App 🧪
1. Click **"Open URL"** in Render Dashboard
2. Your app opens in browser
3. Click **"Login"** on homepage
4. Enter:
   - Username: `demo`
   - Password: `demo123`
5. Click Login

### Step 4: Verify Demo Data ✅
After login, you should see:
- ✅ Dashboard with charts and graphs
- ✅ Recent transactions (15+ entries)
- ✅ Budgets (Food, Transport, Entertainment, etc.)
- ✅ Savings goals (Emergency Fund, Vacation)
- ✅ AI Chatbot ready to answer questions

### Step 5: Share with Judges 📱
Copy your Render URL and share:
```
🌟 FinanceAI - Live Demo
🔗 URL: https://your-app-name.onrender.com
👤 Demo Login:
   Username: demo
   Password: demo123
```

---

## ⚠️ Common Mistakes to Avoid

❌ **DON'T**: Try to login before running `create_demo_data.py`
✅ **DO**: Run the script first, then login

❌ **DON'T**: Forget to run `create_demo_data.py` in Render Shell
✅ **DO**: Use Render's built-in Shell feature (not your local terminal)

❌ **DON'T**: Create new user manually for demo
✅ **DO**: Use the pre-configured demo account (username: demo, password: demo123)

❌ **DON'T**: Skip testing before presenting
✅ **DO**: Test login and all features before your hackathon presentation

---

**Remember**: `create_demo_data.py` is a ONE-TIME setup. After running it once, your demo account and data persist forever! 🎉
