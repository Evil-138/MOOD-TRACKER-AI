"""
AI Mood Tracker & Daily Journal Web App
A Flask application that analyzes emotions and tracks mood patterns
"""

import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
from transformers import pipeline
import plotly
import plotly.graph_objs as go
from collections import Counter
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Initialize sentiment analysis pipeline
sentiment_analyzer = None

def get_sentiment_analyzer():
    """Lazy load sentiment analyzer to improve startup time"""
    global sentiment_analyzer
    if sentiment_analyzer is None:
        print("Loading sentiment analysis model...")
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
    return sentiment_analyzer

# Database setup
DATABASE = 'mood_tracker.db'

def get_db():
    """Create database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            entry_text TEXT NOT NULL,
            mood TEXT NOT NULL,
            mood_score REAL NOT NULL,
            emoji TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

def analyze_mood(text):
    """
    Analyze mood from text using AI sentiment analysis
    Returns: dict with mood, score, emoji
    """
    analyzer = get_sentiment_analyzer()
    result = analyzer(text[:512])[0]  # Limit text length for model
    
    label = result['label']
    score = result['score']
    
    # Map sentiment to mood and emoji
    if label == 'POSITIVE':
        if score > 0.95:
            mood = 'Very Happy'
            emoji = '😄'
        elif score > 0.85:
            mood = 'Happy'
            emoji = '🙂'
        else:
            mood = 'Slightly Happy'
            emoji = '😊'
    else:  # NEGATIVE
        if score > 0.95:
            mood = 'Very Sad'
            emoji = '😢'
        elif score > 0.85:
            mood = 'Sad'
            emoji = '😔'
        else:
            mood = 'Slightly Sad'
            emoji = '😕'
    
    return {
        'mood': mood,
        'score': score,
        'emoji': emoji,
        'sentiment': label
    }

def get_motivational_quote(mood):
    """Get motivational quote based on mood"""
    positive_quotes = [
        "Keep shining! Your positive energy is contagious! ✨",
        "You're doing amazing! Keep up the great vibes! 🌟",
        "Your happiness is inspiring! Share it with the world! 🌈",
        "What a wonderful day! Keep that smile going! 😊"
    ]
    
    negative_quotes = [
        "Every storm runs out of rain. Better days are coming! 🌈",
        "You're stronger than you think. This too shall pass! 💪",
        "Be kind to yourself. Tomorrow is a new day! 🌅",
        "It's okay to not be okay. Take care of yourself! 💙"
    ]
    
    neutral_quotes = [
        "Every day is a fresh start! Make it count! 🌟",
        "You're on your own unique journey. Embrace it! 🚀",
        "Small steps every day lead to big changes! 🌱",
        "Keep going, you're making progress! 💫"
    ]
    
    if 'Happy' in mood:
        return positive_quotes[hash(str(datetime.now().date())) % len(positive_quotes)]
    elif 'Sad' in mood:
        return negative_quotes[hash(str(datetime.now().date())) % len(negative_quotes)]
    else:
        return neutral_quotes[hash(str(datetime.now().date())) % len(neutral_quotes)]

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/add-entry')
def add_entry_page():
    """Add new journal entry page"""
    return render_template('add_entry.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard with mood analytics"""
    conn = get_db()
    
    # Get recent entries
    entries = conn.execute(
        'SELECT * FROM journal_entries ORDER BY date DESC LIMIT 10'
    ).fetchall()
    
    # Get mood statistics
    all_entries = conn.execute(
        'SELECT mood, date, mood_score FROM journal_entries ORDER BY date DESC'
    ).fetchall()
    
    conn.close()
    
    # Calculate statistics
    mood_counts = Counter([e['mood'] for e in all_entries])
    total_entries = len(all_entries)
    
    # Generate weekly summary
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    weekly_moods = [e for e in all_entries if e['date'] >= week_ago]
    
    if weekly_moods:
        avg_score = sum(e['mood_score'] for e in weekly_moods) / len(weekly_moods)
        most_common_mood = Counter([e['mood'] for e in weekly_moods]).most_common(1)[0][0]
        summary = f"This week, you felt mostly {most_common_mood.lower()}! You logged {len(weekly_moods)} entries."
    else:
        summary = "Start logging your moods to see your weekly summary!"
    
    # Create mood trend chart
    chart_data = create_mood_chart(all_entries)
    
    return render_template(
        'dashboard.html',
        entries=entries,
        mood_counts=dict(mood_counts),
        total_entries=total_entries,
        summary=summary,
        chart_data=chart_data
    )

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint to analyze mood from text"""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text or len(text.strip()) < 10:
        return jsonify({'error': 'Please write at least 10 characters'}), 400
    
    # Analyze mood
    mood_result = analyze_mood(text)
    
    # Get motivational quote
    quote = get_motivational_quote(mood_result['mood'])
    
    return jsonify({
        'mood': mood_result['mood'],
        'emoji': mood_result['emoji'],
        'score': round(mood_result['score'], 2),
        'quote': quote
    })

@app.route('/api/save-entry', methods=['POST'])
def api_save_entry():
    """API endpoint to save journal entry"""
    data = request.get_json()
    
    entry_text = data.get('entry_text', '')
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    emoji = data.get('emoji')
    
    # If emoji is provided (quick mood), use predefined mood
    if emoji and not entry_text:
        mood_map = {
            '😄': ('Very Happy', 0.98),
            '🙂': ('Happy', 0.90),
            '😊': ('Slightly Happy', 0.75),
            '😐': ('Neutral', 0.50),
            '😕': ('Slightly Sad', 0.75),
            '😔': ('Sad', 0.90),
            '😢': ('Very Sad', 0.98)
        }
        mood, score = mood_map.get(emoji, ('Neutral', 0.50))
        entry_text = f"Quick mood log: {emoji}"
    else:
        # Analyze mood from text
        mood_result = analyze_mood(entry_text)
        mood = mood_result['mood']
        score = mood_result['score']
        emoji = mood_result['emoji']
    
    # Save to database
    conn = get_db()
    conn.execute(
        'INSERT INTO journal_entries (date, entry_text, mood, mood_score, emoji) VALUES (?, ?, ?, ?, ?)',
        (date, entry_text, mood, score, emoji)
    )
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'mood': mood,
        'emoji': emoji,
        'message': 'Entry saved successfully!'
    })

@app.route('/api/entries')
def api_entries():
    """API endpoint to get all entries"""
    conn = get_db()
    entries = conn.execute(
        'SELECT * FROM journal_entries ORDER BY date DESC'
    ).fetchall()
    conn.close()
    
    return jsonify([dict(e) for e in entries])

@app.route('/api/export/<format>')
def api_export(format):
    """Export entries as CSV or JSON"""
    conn = get_db()
    entries = conn.execute(
        'SELECT * FROM journal_entries ORDER BY date DESC'
    ).fetchall()
    conn.close()
    
    if format == 'json':
        return jsonify([dict(e) for e in entries])
    
    elif format == 'csv':
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Date', 'Mood', 'Emoji', 'Entry', 'Score'])
        
        for entry in entries:
            writer.writerow([
                entry['date'],
                entry['mood'],
                entry['emoji'],
                entry['entry_text'],
                entry['mood_score']
            ])
        
        output.seek(0)
        return output.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=mood_tracker_export.csv'
        }
    
    return jsonify({'error': 'Invalid format'}), 400

def create_mood_chart(entries):
    """Create interactive mood trend chart using Plotly"""
    if not entries:
        return json.dumps({})
    
    # Prepare data
    dates = [e['date'] for e in reversed(entries[-30:])]  # Last 30 days
    scores = [e['mood_score'] for e in reversed(entries[-30:])]
    moods = [e['mood'] for e in reversed(entries[-30:])]
    emojis = [e.get('emoji', '😐') for e in reversed(entries[-30:])]
    
    # Create hover text
    hover_text = [f"{mood} {emoji}<br>{date}" for date, mood, emoji in zip(dates, moods, emojis)]
    
    # Create trace
    trace = go.Scatter(
        x=dates,
        y=scores,
        mode='lines+markers',
        name='Mood Score',
        line=dict(color='#00f5ff', width=3, shape='spline'),
        marker=dict(size=10, color='#ff00ff', line=dict(color='#00f5ff', width=2)),
        hovertext=hover_text,
        hoverinfo='text'
    )
    
    # Create layout
    layout = go.Layout(
        title='Mood Trend Over Time',
        xaxis=dict(title='Date', gridcolor='#333'),
        yaxis=dict(title='Mood Score', gridcolor='#333', range=[0, 1]),
        plot_bgcolor='#1a1a2e',
        paper_bgcolor='#1a1a2e',
        font=dict(color='#00f5ff'),
        hovermode='closest'
    )
    
    fig = go.Figure(data=[trace], layout=layout)
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
