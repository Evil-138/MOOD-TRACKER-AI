"""
Demo Data Generator for MoodFlow
Creates sample journal entries for testing and demonstration
"""

import sqlite3
from datetime import datetime, timedelta
import random

# Sample journal entries
SAMPLE_ENTRIES = [
    ("Had an amazing day at work! Got promoted and the team celebrated with me. Feeling on top of the world!", "Very Happy", 0.98, "😄"),
    ("Nice quiet evening reading my favorite book. Felt peaceful and content.", "Happy", 0.88, "🙂"),
    ("Met up with old friends today. Always good to reconnect!", "Happy", 0.91, "😊"),
    ("Just a normal day. Nothing special happened.", "Neutral", 0.50, "😐"),
    ("Feeling a bit down today. Work was stressful and I'm exhausted.", "Slightly Sad", 0.72, "😕"),
    ("Not a great day. Had an argument with a friend and feeling upset.", "Sad", 0.87, "😔"),
    ("Really struggling today. Everything feels overwhelming.", "Very Sad", 0.95, "😢"),
    ("Accomplished all my goals today! Feeling proud and motivated.", "Very Happy", 0.96, "😄"),
    ("Went for a long walk in nature. Felt so refreshing and calming.", "Happy", 0.85, "🙂"),
    ("Tried a new hobby today - painting! It was therapeutic.", "Slightly Happy", 0.78, "😊"),
    ("Feeling anxious about upcoming deadlines. Need to manage my time better.", "Slightly Sad", 0.75, "😕"),
    ("Woke up feeling energized! Ready to tackle the day ahead.", "Happy", 0.89, "🙂"),
    ("Spent quality time with family. These moments are precious.", "Very Happy", 0.97, "😄"),
    ("Work presentation went well! Boss was impressed.", "Happy", 0.92, "😊"),
    ("Feeling under the weather today. Just want to rest.", "Slightly Sad", 0.70, "😕"),
    ("Completed my first 5k run! Can't believe I did it!", "Very Happy", 0.99, "😄"),
    ("Meditation session helped me find inner peace today.", "Happy", 0.86, "🙂"),
    ("Dealing with some personal challenges. Taking it one day at a time.", "Slightly Sad", 0.76, "😕"),
    ("Cooked a delicious meal tonight. Cooking is my therapy!", "Happy", 0.84, "😊"),
    ("Feeling grateful for all the good things in my life.", "Happy", 0.90, "🙂"),
]

def create_demo_data(num_days=30):
    """Create demo journal entries for the past num_days"""
    
    conn = sqlite3.connect('mood_tracker.db')
    cursor = conn.cursor()
    
    # Clear existing demo data (optional)
    print("Creating demo data...")
    
    # Generate entries
    for i in range(num_days):
        # Calculate date
        entry_date = (datetime.now() - timedelta(days=num_days - i - 1)).strftime('%Y-%m-%d')
        
        # Pick random sample entry
        text, mood, score, emoji = random.choice(SAMPLE_ENTRIES)
        
        # Add some variation to scores
        score_variation = score + random.uniform(-0.05, 0.05)
        score_variation = max(0.5, min(0.99, score_variation))  # Keep in valid range
        
        # Insert into database
        cursor.execute(
            'INSERT INTO journal_entries (date, entry_text, mood, mood_score, emoji) VALUES (?, ?, ?, ?, ?)',
            (entry_date, text, mood, score_variation, emoji)
        )
    
    conn.commit()
    conn.close()
    
    print(f"✅ Created {num_days} demo entries!")
    print("You can now run the app and see the dashboard with data.")

if __name__ == '__main__':
    # Ask user for confirmation
    print("🧠 MoodFlow - Demo Data Generator")
    print("=" * 50)
    print("\nThis script will add sample journal entries to your database.")
    print("This is useful for testing and seeing how the app looks with data.\n")
    
    choice = input("How many days of demo data? (default: 30): ").strip()
    
    try:
        num_days = int(choice) if choice else 30
        if num_days < 1 or num_days > 365:
            print("❌ Please enter a number between 1 and 365")
        else:
            create_demo_data(num_days)
    except ValueError:
        print("❌ Invalid input. Using default (30 days)")
        create_demo_data(30)
