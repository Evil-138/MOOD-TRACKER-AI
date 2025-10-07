# 🚀 Deployment Guide - MoodFlow

Complete deployment instructions for various platforms.

---

## 🎯 Pre-Deployment Checklist

- [ ] App runs locally without errors
- [ ] Database initialized correctly
- [ ] All dependencies in requirements.txt
- [ ] Static files loading properly
- [ ] AI model downloads successfully
- [ ] Change SECRET_KEY in app.py
- [ ] Test on multiple browsers
- [ ] Mobile responsive verified

---

## 🌐 Platform 1: Render (Recommended)

**Best for:** Free tier, easy deployment, automatic HTTPS

### Step-by-Step

1. **Prepare Your Code**

```powershell
# Ensure you have these files:
# - app.py
# - requirements.txt (with gunicorn)
# - Procfile (optional for Render)
```

2. **Create GitHub Repository**

```powershell
git init
git add .
git commit -m "Initial commit - MoodFlow app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/moodflow.git
git push -u origin main
```

3. **Deploy to Render**

- Go to [render.com](https://render.com)
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Configure:
  - **Name**: moodflow
  - **Environment**: Python 3
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `gunicorn app:app`
  - **Instance Type**: Free

4. **Environment Variables** (Optional)

Add in Render dashboard:
- `PYTHON_VERSION`: `3.11.0`
- `FLASK_ENV`: `production`

5. **Deploy!**

Click "Create Web Service" - Wait 5-10 minutes for first deploy.

**Your app will be live at:** `https://moodflow-XXXX.onrender.com`

### Render Tips

- Free tier sleeps after inactivity (wakes in 30-60s)
- Automatic deploys on git push
- Built-in HTTPS certificates
- Check logs in dashboard for errors

---

## 🐳 Platform 2: Railway

**Best for:** Simple deployment, generous free tier

### Step-by-Step

1. **Create Account** at [railway.app](https://railway.app)

2. **Deploy from GitHub**

- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your repository
- Railway auto-detects Flask!

3. **Configuration** (Auto-detected)

Railway automatically:
- Installs requirements.txt
- Runs gunicorn app:app
- Assigns PORT environment variable

4. **Custom Domain** (Optional)

- Settings → Domains
- Add custom domain or use railway.app subdomain

**Your app will be live at:** `https://moodflow-production-XXXX.up.railway.app`

---

## 🤗 Platform 3: Hugging Face Spaces

**Best for:** AI/ML apps, good for portfolio, free GPU (if needed)

### Step-by-Step

1. **Create Space**

- Go to [huggingface.co/spaces](https://huggingface.co/spaces)
- Click "Create new Space"
- Choose:
  - **Space name**: moodflow
  - **License**: MIT
  - **SDK**: Docker (or Gradio)
  - **Visibility**: Public

2. **Modify app.py**

Change the last line to:

```python
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=7860)
```

3. **Create README.md for HF**

Create file: `README.md` (in root, HF uses this):

```yaml
---
title: MoodFlow - AI Mood Tracker
emoji: 🧠
colorFrom: cyan
colorTo: magenta
sdk: docker
pinned: false
---

# MoodFlow - AI Mood Tracker

Check it out!
```

4. **Use Dockerfile**

The Dockerfile in the project is already configured for HF Spaces!

5. **Upload Files**

Either:
- Use Git (recommended)
- Use web interface to upload files

**Git Method:**
```powershell
git clone https://huggingface.co/spaces/YOUR_USERNAME/moodflow
cd moodflow
# Copy all your files here
git add .
git commit -m "Initial deployment"
git push
```

**Your app will be live at:** `https://huggingface.co/spaces/YOUR_USERNAME/moodflow`

---

## ☁️ Platform 4: Google Cloud Run

**Best for:** Scalability, pay-per-use

### Step-by-Step

1. **Install Google Cloud SDK**

Download from: https://cloud.google.com/sdk/docs/install

2. **Initialize**

```powershell
gcloud init
gcloud auth login
```

3. **Deploy**

```powershell
# Build and deploy
gcloud run deploy moodflow `
    --source . `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated
```

4. **Configuration**

The Dockerfile is used automatically.

**Your app will be live at:** `https://moodflow-XXXX.run.app`

---

## 🔵 Platform 5: Azure App Service

**Best for:** Microsoft ecosystem, enterprise

### Step-by-Step

1. **Install Azure CLI**

```powershell
# Download from: https://aka.ms/installazurecliwindows
```

2. **Login**

```powershell
az login
```

3. **Create Resources**

```powershell
# Create resource group
az group create --name moodflow-rg --location eastus

# Create app service plan
az appservice plan create `
    --name moodflow-plan `
    --resource-group moodflow-rg `
    --sku B1 `
    --is-linux

# Create web app
az webapp create `
    --resource-group moodflow-rg `
    --plan moodflow-plan `
    --name moodflow-app `
    --runtime "PYTHON:3.11"
```

4. **Deploy Code**

```powershell
# Deploy from local git
az webapp up `
    --name moodflow-app `
    --resource-group moodflow-rg `
    --runtime "PYTHON:3.11"
```

**Your app will be live at:** `https://moodflow-app.azurewebsites.net`

---

## 🟢 Platform 6: Heroku

**Best for:** Classic PaaS (Note: No longer free tier)

### Step-by-Step

1. **Install Heroku CLI**

Download from: https://devcenter.heroku.com/articles/heroku-cli

2. **Login and Create App**

```powershell
heroku login
heroku create moodflow-app
```

3. **Add Procfile** (already created)

Ensure `Procfile` exists:
```
web: gunicorn app:app
```

4. **Deploy**

```powershell
git push heroku main
```

5. **Open App**

```powershell
heroku open
```

**Your app will be live at:** `https://moodflow-app.herokuapp.com`

---

## 📦 Platform 7: Docker Deployment

**Best for:** Self-hosting, any VPS

### Build and Run

```powershell
# Build image
docker build -t moodflow:latest .

# Run container
docker run -d `
    -p 80:7860 `
    --name moodflow `
    moodflow:latest

# Access at http://localhost
```

### Deploy to VPS

```bash
# On your server (Linux)
git clone YOUR_REPO
cd moodflow
docker build -t moodflow .
docker run -d -p 80:7860 --restart always moodflow
```

---

## 🔧 Post-Deployment Configuration

### 1. Update Secret Key

**IMPORTANT:** Change in `app.py`:

```python
app.config['SECRET_KEY'] = 'your-random-secret-key-here'
```

Generate random key:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Environment Variables

Set these in your platform:

```
FLASK_ENV=production
SECRET_KEY=your-generated-secret-key
DATABASE_URL=sqlite:///mood_tracker.db  # or cloud DB
```

### 3. Database Persistence

**Render/Railway/Heroku:**
- Use persistent volumes
- Or migrate to PostgreSQL

**Example PostgreSQL setup:**
```powershell
pip install psycopg2-binary
# Update app.py to use PostgreSQL connection
```

---

## 🔍 Monitoring & Maintenance

### Check App Health

```powershell
# Test endpoints
curl https://your-app.com/
curl https://your-app.com/api/entries
```

### Monitor Logs

**Render:**
- Dashboard → Logs tab

**Railway:**
- Dashboard → Deployments → View Logs

**Heroku:**
```powershell
heroku logs --tail
```

**Google Cloud:**
```powershell
gcloud run logs read
```

### Performance Optimization

1. **Enable Caching**
   - Use Flask-Caching
   - Cache AI model in memory

2. **Use CDN**
   - Serve static files from CDN
   - Cloudflare free tier

3. **Database Indexing**
   - Add indexes to date column
   - Regular vacuum/optimize

---

## 🚨 Troubleshooting

### Issue: AI Model Download Timeout

**Solution:**
```python
# In app.py, increase timeout or pre-download model
# Add to Dockerfile:
RUN python -c "from transformers import pipeline; pipeline('sentiment-analysis')"
```

### Issue: Database Not Persisting

**Solution:**
- Check platform persistent storage
- Use environment variable for DB path
- Consider cloud database (PostgreSQL/MongoDB)

### Issue: Out of Memory

**Solution:**
- Upgrade plan (more RAM)
- Optimize model loading (lazy load)
- Clear unused dependencies

### Issue: Slow Cold Starts

**Solution:**
- Keep app "warm" with uptime monitor (uptimerobot.com)
- Use paid tier (no sleep)
- Optimize startup time

---

## 📊 Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Render** | ✅ 750hrs/mo | $7/mo | Beginners |
| **Railway** | ✅ $5 credit | $5/mo+ | Simple apps |
| **HF Spaces** | ✅ Unlimited | Free | AI/ML demos |
| **Google Cloud** | ❌ (credit) | Pay-per-use | Scale |
| **Azure** | ❌ | $13/mo+ | Enterprise |
| **Heroku** | ❌ | $5-7/mo | Legacy |

---

## ✅ Deployment Success Checklist

After deployment, verify:

- [ ] Home page loads
- [ ] Can create new entry
- [ ] AI analysis works
- [ ] Dashboard displays
- [ ] Charts render correctly
- [ ] Export functions work
- [ ] Mobile responsive
- [ ] No console errors
- [ ] Database saves data
- [ ] HTTPS enabled

---

## 🎉 You're Live!

Share your deployed app:

- LinkedIn portfolio
- GitHub README
- Twitter/X
- Personal website
- Resume projects section

**Example URL to share:**
```
🧠 Check out my AI Mood Tracker app!
Built with Flask, AI, and modern web design.

🔗 https://your-app.com
📦 Code: https://github.com/your-username/moodflow
```

---

**Need help? Check the logs, documentation, or GitHub issues!**
