# 🚀 Quick Start Guide

## Installation

1. **Install Python 3.8+** if you haven't already

2. **Open PowerShell** and navigate to the project folder:
```powershell
cd "d:\MOOD TRACKER"
```

3. **Create virtual environment** (recommended):
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

4. **Install dependencies**:
```powershell
pip install -r requirements.txt
```

5. **Run the app**:
```powershell
python app.py
```

6. **Open browser** and go to:
```
http://localhost:5000
```

## First Time Use

### 📝 Create Your First Entry

1. Click **"New Entry"** in the navigation
2. Choose either:
   - **Quick Mood Log**: Tap an emoji (😄 🙂 😊 😐 😕 😔 😢)
   - **Write Journal**: Type your thoughts and click "Analyze Mood"
3. Save your entry!

### 📊 View Dashboard

1. Click **"Dashboard"** to see:
   - Mood distribution chart
   - Mood trends over time
   - Weekly summary
   - Recent entries

### 💾 Export Data

From the dashboard, click:
- **Export CSV** - for spreadsheet analysis
- **Export JSON** - for programmatic use

## Tips

- Write at least 10 characters for accurate AI mood analysis
- Use the quick emoji selector for fast logging
- Check your dashboard weekly to see patterns
- Export your data regularly for backup

## Troubleshooting

**AI model loading slow?**
- First run downloads ~250MB model (one-time)
- Be patient, it's worth it! 🚀

**Port 5000 busy?**
- Edit `app.py` and change port to 5001 or 8000

**Database issues?**
- Delete `mood_tracker.db` and restart

## Need Help?

Check the full README.md for detailed documentation!

---

**Enjoy tracking your moods! 🌈✨**
