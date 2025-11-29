"""
Sentiment Analyzer Module
Analyzes mood and sentiment from journal entries
"""

from textblob import TextBlob
import re
from collections import Counter
from datetime import datetime

# Emotion keywords for enhanced analysis
EMOTION_KEYWORDS = {
    'positive': [
        'happy', 'joy', 'excited', 'grateful', 'blessed', 'wonderful', 'amazing',
        'great', 'fantastic', 'excellent', 'love', 'loved', 'peaceful', 'calm',
        'content', 'satisfied', 'proud', 'accomplished', 'successful', 'confident',
        'hopeful', 'optimistic', 'energized', 'motivated', 'inspired'
    ],
    'negative': [
        'sad', 'depressed', 'anxious', 'worried', 'stressed', 'frustrated', 'angry',
        'upset', 'disappointed', 'lonely', 'tired', 'exhausted', 'overwhelmed',
        'difficult', 'hard', 'struggle', 'pain', 'hurt', 'scared', 'afraid',
        'nervous', 'insecure', 'doubt', 'regret', 'guilty'
    ],
    'neutral': [
        'okay', 'fine', 'normal', 'usual', 'regular', 'same', 'routine'
    ]
}

def analyze_sentiment(text):
    """
    Analyze sentiment using TextBlob and keyword matching
    Returns: sentiment score, polarity, subjectivity, and emotion
    """
    # TextBlob analysis
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to 1
    subjectivity = blob.sentiment.subjectivity  # 0 to 1
    
    # Keyword-based emotion detection
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    positive_count = sum(1 for word in words if word in EMOTION_KEYWORDS['positive'])
    negative_count = sum(1 for word in words if word in EMOTION_KEYWORDS['negative'])
    
    # Combined sentiment score (-1 to 1)
    # Weight TextBlob polarity (70%) and keyword ratio (30%)
    if len(words) > 0:
        keyword_score = (positive_count - negative_count) / max(len(words), 1)
        combined_score = (0.7 * polarity) + (0.3 * keyword_score)
    else:
        combined_score = polarity
    
    # Determine sentiment category
    if combined_score > 0.1:
        sentiment = 'positive'
    elif combined_score < -0.1:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return {
        'sentiment': sentiment,
        'score': round(combined_score, 3),
        'polarity': round(polarity, 3),
        'subjectivity': round(subjectivity, 3),
        'positive_keywords': positive_count,
        'negative_keywords': negative_count
    }

def extract_keywords(text, top_n=10):
    """
    Extract most common meaningful words from text
    """
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your',
        'his', 'her', 'its', 'our', 'their', 'me', 'him', 'them', 'what',
        'which', 'who', 'when', 'where', 'why', 'how', 'just', 'so', 'today',
        'felt', 'feel', 'feeling'
    }
    
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    meaningful_words = [w for w in words if w not in stop_words and len(w) > 3]
    
    word_freq = Counter(meaningful_words)
    return word_freq.most_common(top_n)

def analyze_mood_trend(entries):
    """
    Analyze mood trends across multiple entries
    """
    if not entries:
        return None
    
    sentiments = []
    dates = []
    daily_scores = {}
    
    for entry in entries:
        analysis = analyze_sentiment(entry['content'])
        entry_date = entry.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        sentiments.append(analysis['sentiment'])
        dates.append(entry_date)
        
        # Store daily score
        if entry_date not in daily_scores:
            daily_scores[entry_date] = []
        daily_scores[entry_date].append(analysis['score'])
    
    # Calculate averages
    avg_scores = {date: sum(scores)/len(scores) 
                  for date, scores in daily_scores.items()}
    
    # Count sentiment types
    sentiment_counts = Counter(sentiments)
    
    # Find best and worst days
    best_day = max(avg_scores.items(), key=lambda x: x[1]) if avg_scores else None
    worst_day = min(avg_scores.items(), key=lambda x: x[1]) if avg_scores else None
    
    return {
        'total_entries': len(entries),
        'sentiment_distribution': dict(sentiment_counts),
        'daily_scores': avg_scores,
        'best_day': best_day,
        'worst_day': worst_day,
        'overall_mood': calculate_overall_mood(sentiments)
    }

def calculate_overall_mood(sentiments):
    """Calculate overall mood from list of sentiments"""
    if not sentiments:
        return 'neutral'
    
    counts = Counter(sentiments)
    positive_ratio = counts.get('positive', 0) / len(sentiments)
    
    if positive_ratio >= 0.6:
        return 'mostly positive'
    elif positive_ratio >= 0.4:
        return 'balanced'
    else:
        return 'needs attention'

def generate_weekly_summary(entries):
    """
    Generate a natural language summary of the week
    """
    if not entries:
        return "No entries to analyze yet. Start journaling to see your mood trends!"
    
    trend = analyze_mood_trend(entries)
    
    # Build summary
    summary_parts = []
    
    # Entry count
    summary_parts.append(f"You made {trend['total_entries']} journal entries.")
    
    # Sentiment distribution
    dist = trend['sentiment_distribution']
    if dist.get('positive', 0) > 0:
        summary_parts.append(f"You had {dist.get('positive', 0)} positive days")
    if dist.get('negative', 0) > 0:
        summary_parts.append(f"{dist.get('negative', 0)} challenging days")
    if dist.get('neutral', 0) > 0:
        summary_parts.append(f"and {dist.get('neutral', 0)} neutral days.")
    
    # Best and worst days
    if trend['best_day']:
        best_date = datetime.strptime(trend['best_day'][0], '%Y-%m-%d').strftime('%A, %B %d')
        summary_parts.append(f"Your most positive day was {best_date}.")
    
    if trend['worst_day'] and trend['worst_day'][1] < -0.1:
        worst_date = datetime.strptime(trend['worst_day'][0], '%Y-%m-%d').strftime('%A, %B %d')
        summary_parts.append(f"You seemed to struggle most on {worst_date}.")
    
    # Overall mood
    summary_parts.append(f"Overall, your mood appears {trend['overall_mood']}.")
    
    return " ".join(summary_parts)

def calculate_streak(entries):
    """Calculate consecutive days of journaling"""
    if not entries:
        return 0
    
    dates = sorted([entry['date'] for entry in entries], reverse=True)
    
    if not dates:
        return 0
    
    streak = 1
    current_date = datetime.strptime(dates[0], '%Y-%m-%d')
    
    for i in range(1, len(dates)):
        date = datetime.strptime(dates[i], '%Y-%m-%d')
        days_diff = (current_date - date).days
        
        if days_diff == 1:
            streak += 1
            current_date = date
        elif days_diff > 1:
            break
    
    return streak