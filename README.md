# 🧠 MoodFlow - AI Mood Tracker & Daily Journal

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![AI Powered](https://img.shields.io/badge/AI-Powered-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**MoodFlow** is a beautiful, AI-powered mood tracking and journaling web application built with Flask. It uses advanced NLP sentiment analysis to automatically detect emotions from journal entries and provides insightful visualizations of emotional patterns over time.

## ✨ Features

- 🤖 **AI-Powered Mood Analysis** - Automatic emotion detection using Hugging Face transformers
- 📊 **Interactive Visualizations** - Beautiful charts showing mood trends with Chart.js and Plotly
- 💡 **Smart Suggestions** - Personalized motivational quotes based on detected mood
- 😊 **Quick Mood Logger** - Fast emoji-based mood tracking
- 📈 **Analytics Dashboard** - Comprehensive mood analytics and insights
- 💾 **Data Export** - Export your journal entries as CSV or JSON
- 🎨 **Modern Dark UI** - Stunning neon-themed dark interface with smooth animations
- 📱 **Responsive Design** - Works perfectly on desktop and mobile devices
- 🔒 **Privacy First** - All data stored locally in SQLite database

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

```powershell
cd "d:\MOOD TRACKER"
```

2. **Create a virtual environment** (recommended)

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. **Install dependencies**

```powershell
pip install -r requirements.txt
```

> **Note**: The first installation may take a few minutes as it downloads the AI model (approximately 250MB).

4. **Run the application**

```powershell
python app.py
```

5. **Open your browser**

Navigate to: `http://localhost:5000`

## 📖 How to Use

### 1. **Quick Mood Log**
- Click on an emoji on the "New Entry" page
- Instantly log your current mood without writing

### 2. **Journal Entry**
- Write your thoughts in the text area
- Click "Analyze Mood" to see AI-detected emotions
- Save your entry with mood analysis

### 3. **View Dashboard**
- See your mood distribution in a pie chart
- Track mood trends over time
- Read weekly summaries and insights
- Export your data

## 🏗️ Project Structure

```
MOOD TRACKER/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── mood_tracker.db       # SQLite database (auto-created)
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── add_entry.html   # Journal entry page
│   └── dashboard.html   # Analytics dashboard
├── static/              # Static assets
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   └── js/
│       └── main.js      # JavaScript utilities
└── README.md            # This file
```

## 🔧 Technology Stack

### Backend
- **Flask** - Python web framework
- **SQLite** - Database
- **Transformers** (Hugging Face) - AI sentiment analysis
- **Plotly** - Interactive charts

### Frontend
- **HTML5/CSS3** - Modern web standards
- **JavaScript (Vanilla)** - Client-side logic
- **Chart.js** - Mood distribution charts
- **Plotly.js** - Trend visualizations

### AI Model
- **distilbert-base-uncased-finetuned-sst-2-english** - Sentiment analysis model

## 🌐 Deployment

### Deploy to Render

1. **Create a new Web Service** on [Render](https://render.com)

2. **Connect your GitHub repository**

3. **Configure the service:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Add Environment Variable**: `PYTHON_VERSION=3.11.0`

4. **Add to `requirements.txt`:**
```
gunicorn==21.2.0
```

5. **Deploy!** Your app will be live in minutes.

### Deploy to Hugging Face Spaces

1. **Create a new Space** at [Hugging Face Spaces](https://huggingface.co/spaces)

2. **Select "Gradio" or "Streamlit"** SDK (or use Docker)

3. **Upload your files** or connect via Git

4. **Create a `Dockerfile`:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "app.py"]
```

5. **Modify `app.py` last line:**
```python
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=7860)
```

### Deploy to Railway

1. **Create a new project** on [Railway](https://railway.app)

2. **Connect GitHub repository**

3. **Railway auto-detects Flask** - No configuration needed!

4. **Add environment variable** (optional):
   - `FLASK_ENV=production`

## 🎨 Customization

### Change Color Scheme

Edit `static/css/style.css`:

```css
:root {
    --primary-cyan: #00f5ff;      /* Change to your color */
    --primary-magenta: #ff00ff;   /* Change to your color */
    --bg-dark: #0f0f1e;           /* Background color */
}
```

### Add More Moods

Edit `app.py` in the `analyze_mood()` function to add custom mood categories.

### Modify Quotes

Edit the quote arrays in `app.py` under the `get_motivational_quote()` function.

## 🐛 Troubleshooting

### Issue: AI model download fails

**Solution**: Ensure you have a stable internet connection. The model is ~250MB and downloads on first run.

### Issue: Database error

**Solution**: Delete `mood_tracker.db` and restart the app. It will create a fresh database.

### Issue: Port already in use

**Solution**: Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

## 📊 Database Schema

```sql
CREATE TABLE journal_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    entry_text TEXT NOT NULL,
    mood TEXT NOT NULL,
    mood_score REAL NOT NULL,
    emoji TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 💡 Future Enhancements

- [ ] User authentication with Firebase
- [ ] Multiple users support
- [ ] Dark/Light theme toggle
- [ ] Voice-to-text journaling
- [ ] Weekly/Monthly email reports
- [ ] Mobile app (React Native)
- [ ] Integration with calendar apps
- [ ] Advanced AI insights with GPT
- [ ] Mood prediction based on patterns

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for the sentiment analysis model
- [Chart.js](https://www.chartjs.org/) for beautiful charts
- [Plotly](https://plotly.com/) for interactive visualizations
- [Flask](https://flask.palletsprojects.com/) for the amazing framework

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ and AI**

*Track your emotions, understand your patterns, improve your wellbeing ✨*
