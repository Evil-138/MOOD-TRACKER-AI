# 🧪 Testing & Development Guide

## Local Development Setup

### Step 1: Environment Setup

```powershell
# Navigate to project
cd "d:\MOOD TRACKER"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run Application

```powershell
# Run Flask app
python app.py
```

**Expected Output:**
```
Loading sentiment analysis model...
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Step 3: Access Application

Open browser: `http://localhost:5000`

---

## Testing Features

### Test 1: AI Mood Analysis

**Positive Text Test:**
```
"I had an amazing day! Everything went perfectly and I'm so happy!"
```
Expected: 😄 Very Happy (Score: 0.95+)

**Negative Text Test:**
```
"Today was terrible. I feel sad and everything went wrong."
```
Expected: 😢 Very Sad (Score: 0.85+)

**Neutral Text Test:**
```
"I went to the store and bought groceries. Then came home."
```
Expected: 😐 Neutral (Score: 0.50-0.70)

### Test 2: Quick Mood Logger

1. Go to "New Entry"
2. Click each emoji (😄 🙂 😊 😐 😕 😔 😢)
3. Confirm quick save
4. Check dashboard for logged moods

### Test 3: Dashboard Visualization

**With No Data:**
- Should show empty state
- "Create Your First Entry" button

**With Data:**
- Run: `python create_demo_data.py`
- Refresh dashboard
- Should see:
  - Pie chart with mood distribution
  - Line chart with trend
  - Summary cards
  - Recent entries grid

### Test 4: Export Functionality

1. Create several entries
2. Go to dashboard
3. Click "Export CSV"
4. Click "Export JSON"
5. Verify downloaded files contain data

---

## API Testing

### Using PowerShell (curl equivalent)

**Test Analyze Endpoint:**
```powershell
$body = @{
    text = "I am feeling great today!"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/analyze" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Test Save Entry:**
```powershell
$body = @{
    entry_text = "Test journal entry"
    date = "2025-10-07"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/save-entry" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Get All Entries:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/entries"
```

---

## Database Testing

### Inspect Database

```powershell
# Install DB Browser for SQLite (if not installed)
# Or use command line

# Connect to database
sqlite3 mood_tracker.db

# View tables
.tables

# View all entries
SELECT * FROM journal_entries;

# Count entries
SELECT COUNT(*) FROM journal_entries;

# View by mood
SELECT mood, COUNT(*) FROM journal_entries GROUP BY mood;

# Exit
.exit
```

---

## Performance Testing

### Test AI Model Loading

**First Run (Cold Start):**
```powershell
Measure-Command { python app.py }
```
Expected: 5-15 seconds (model download)

**Subsequent Runs (Warm Start):**
Expected: 1-3 seconds

### Test Analysis Speed

Create entry with 500 characters and measure analysis time.
Expected: < 2 seconds

---

## Browser Testing

### Desktop Browsers
- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari (Mac)

### Mobile Testing
Use DevTools responsive mode:
- 📱 iPhone SE (375px)
- 📱 iPhone 12 Pro (390px)
- 📱 iPad (768px)
- 📱 iPad Pro (1024px)

### Features to Test
1. Navigation responsive
2. Emoji buttons size
3. Form inputs touch-friendly
4. Charts render correctly
5. Modals center properly

---

## Common Issues & Solutions

### Issue 1: Port Already in Use

```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F

# Or change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue 2: AI Model Download Fails

**Solution:**
```powershell
# Install/upgrade transformers
pip install --upgrade transformers torch

# Clear cache and retry
python -c "from transformers import pipeline; pipeline('sentiment-analysis')"
```

### Issue 3: Database Locked

**Solution:**
```powershell
# Close all connections
# Delete database and restart
Remove-Item mood_tracker.db
python app.py
```

### Issue 4: Static Files Not Loading

**Solution:**
```powershell
# Clear browser cache (Ctrl + Shift + Delete)
# Hard reload (Ctrl + F5)
# Check static folder structure
```

---

## Code Quality Checks

### Check Python Syntax

```powershell
python -m py_compile app.py
```

### Check for Security Issues

```powershell
pip install bandit
bandit -r .
```

### Check Dependencies

```powershell
pip list
pip check
```

---

## Deployment Testing

### Test Production Mode

```powershell
# Set production environment
$env:FLASK_ENV = "production"

# Run with gunicorn
gunicorn app:app
```

### Test Docker Build

```powershell
# Build image
docker build -t moodflow .

# Run container
docker run -p 5000:7860 moodflow

# Access: http://localhost:5000
```

---

## Load Testing (Optional)

### Using Apache Bench (ab)

```powershell
# Install Apache Bench or use online tool

# Test home page (100 requests, 10 concurrent)
ab -n 100 -c 10 http://localhost:5000/

# Test API endpoint
ab -n 50 -c 5 -p test_data.json -T "application/json" http://localhost:5000/api/analyze
```

---

## Continuous Testing Checklist

- [ ] All pages load without errors
- [ ] Navigation links work
- [ ] AI analysis returns results
- [ ] Quick mood logger saves correctly
- [ ] Dashboard displays charts
- [ ] Export buttons download files
- [ ] Mobile view responsive
- [ ] Forms validate input
- [ ] Modals open/close correctly
- [ ] Database saves data
- [ ] No console errors
- [ ] Smooth animations
- [ ] Colors display correctly
- [ ] Text readable on all backgrounds

---

## Demo Data Management

### Create Demo Data

```powershell
python create_demo_data.py
# Enter number of days (default: 30)
```

### Clear All Data

```powershell
# Backup first!
Copy-Item mood_tracker.db mood_tracker.db.backup

# Delete database
Remove-Item mood_tracker.db

# Restart app (creates fresh DB)
python app.py
```

### Reset to Demo State

```powershell
Remove-Item mood_tracker.db
python app.py
# Wait for DB creation
# Stop app (Ctrl+C)
python create_demo_data.py
python app.py
```

---

## Debugging Tips

### Enable Debug Mode

Already enabled in `app.py`:
```python
app.run(debug=True, ...)
```

### Check Logs

Flask outputs to console. Watch for:
- 200 OK (successful requests)
- 404 Not Found (missing routes)
- 500 Internal Server Error (bugs)

### Browser DevTools

**Console Tab:**
- Check for JavaScript errors
- View API responses

**Network Tab:**
- Monitor API calls
- Check request/response data

**Elements Tab:**
- Inspect CSS styles
- Verify HTML structure

---

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] No console errors
- [ ] AI model works
- [ ] Charts render
- [ ] Export works
- [ ] Mobile responsive
- [ ] README complete
- [ ] requirements.txt updated
- [ ] .gitignore includes database
- [ ] Secret key changed
- [ ] Production mode tested
- [ ] Demo data optional

---

**Ready to deploy? Check DEPLOYMENT.md for platform-specific guides!**
