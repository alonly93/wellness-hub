"""
Insights Generator Module
Generates insights from self-tracking dashboard data
"""

from datetime import datetime, timedelta
from statistics import mean, stdev
from collections import defaultdict

def calculate_averages(logs):
    """Calculate average values for all metrics"""
    if not logs:
        return None
    
    metrics = ['sleep_hours', 'mood_rating', 'study_hours', 'water_intake', 
               'exercise_minutes', 'productivity_score']
    
    averages = {}
    for metric in metrics:
        values = [log[metric] for log in logs if metric in log]
        if values:
            averages[metric] = round(mean(values), 2)
        else:
            averages[metric] = 0
    
    return averages

def calculate_trends(logs, days=7):
    """
    Calculate trends (improving, declining, stable) for each metric
    """
    if len(logs) < days:
        return None
    
    # Sort logs by date
    sorted_logs = sorted(logs, key=lambda x: x['date'])
    recent_logs = sorted_logs[-days:]
    previous_logs = sorted_logs[-days*2:-days] if len(sorted_logs) >= days*2 else sorted_logs[:days]
    
    metrics = ['sleep_hours', 'mood_rating', 'study_hours', 'water_intake', 
               'exercise_minutes', 'productivity_score']
    
    trends = {}
    for metric in metrics:
        recent_avg = mean([log[metric] for log in recent_logs])
        previous_avg = mean([log[metric] for log in previous_logs])
        
        change_percent = ((recent_avg - previous_avg) / previous_avg * 100) if previous_avg > 0 else 0
        
        if change_percent > 5:
            trend = 'improving'
        elif change_percent < -5:
            trend = 'declining'
        else:
            trend = 'stable'
        
        trends[metric] = {
            'trend': trend,
            'change_percent': round(change_percent, 1),
            'recent_avg': round(recent_avg, 2),
            'previous_avg': round(previous_avg, 2)
        }
    
    return trends

def find_correlations(logs):
    """
    Find correlations between different metrics
    """
    if len(logs) < 7:
        return []
    
    insights = []
    
    # Group logs by sleep quality
    high_sleep = [log for log in logs if log['sleep_hours'] >= 7]
    low_sleep = [log for log in logs if log['sleep_hours'] < 7]
    
    if high_sleep and low_sleep:
        high_sleep_mood = mean([log['mood_rating'] for log in high_sleep])
        low_sleep_mood = mean([log['mood_rating'] for log in low_sleep])
        
        if high_sleep_mood > low_sleep_mood + 0.5:
            insights.append({
                'type': 'sleep_mood',
                'message': f"On days you sleep 7+ hours, your mood is usually {round(high_sleep_mood - low_sleep_mood, 1)} points higher.",
                'icon': '😴'
            })
    
    # Exercise and productivity correlation
    high_exercise = [log for log in logs if log['exercise_minutes'] >= 30]
    low_exercise = [log for log in logs if log['exercise_minutes'] < 30]
    
    if high_exercise and low_exercise:
        high_ex_prod = mean([log['productivity_score'] for log in high_exercise])
        low_ex_prod = mean([log['productivity_score'] for log in low_exercise])
        
        if high_ex_prod > low_ex_prod + 5:
            insights.append({
                'type': 'exercise_productivity',
                'message': f"You tend to be {round(high_ex_prod - low_ex_prod, 1)}% more productive on days you exercise 30+ minutes.",
                'icon': '💪'
            })
    
    # Study hours and mood
    high_study = [log for log in logs if log['study_hours'] >= 4]
    if high_study:
        avg_mood = mean([log['mood_rating'] for log in high_study])
        overall_mood = mean([log['mood_rating'] for log in logs])
        
        if avg_mood < overall_mood - 0.5:
            insights.append({
                'type': 'study_mood',
                'message': "Long study sessions (4+ hours) seem to lower your mood. Consider taking more breaks!",
                'icon': '📚'
            })
    
    # Water intake and productivity
    good_hydration = [log for log in logs if log['water_intake'] >= 8]
    if good_hydration and len(good_hydration) < len(logs):
        good_hydration_prod = mean([log['productivity_score'] for log in good_hydration])
        overall_prod = mean([log['productivity_score'] for log in logs])
        
        if good_hydration_prod > overall_prod + 5:
            insights.append({
                'type': 'water_productivity',
                'message': "Staying well-hydrated (8+ glasses) boosts your productivity!",
                'icon': '💧'
            })
    
    return insights

def generate_weekly_report(logs):
    """
    Generate a comprehensive weekly report
    """
    if not logs:
        return None
    
    # Get last 7 days
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    
    recent_logs = [log for log in logs 
                   if datetime.strptime(log['date'], '%Y-%m-%d') >= week_ago]
    
    if not recent_logs:
        return None
    
    averages = calculate_averages(recent_logs)
    trends = calculate_trends(logs, days=7)
    insights = find_correlations(logs)
    
    # Find best and worst days
    best_day = max(recent_logs, key=lambda x: x['mood_rating'])
    worst_day = min(recent_logs, key=lambda x: x['mood_rating'])
    
    # Most consistent metric
    consistency_scores = {}
    metrics = ['sleep_hours', 'exercise_minutes', 'study_hours']
    
    for metric in metrics:
        values = [log[metric] for log in recent_logs]
        if len(values) > 1:
            std = stdev(values)
            consistency_scores[metric] = std
    
    most_consistent = min(consistency_scores.items(), key=lambda x: x[1])[0] if consistency_scores else None
    
    report = {
        'period': f"{week_ago.strftime('%B %d')} - {today.strftime('%B %d, %Y')}",
        'days_logged': len(recent_logs),
        'averages': averages,
        'trends': trends,
        'insights': insights,
        'best_day': {
            'date': datetime.strptime(best_day['date'], '%Y-%m-%d').strftime('%A, %B %d'),
            'mood': best_day['mood_rating']
        },
        'worst_day': {
            'date': datetime.strptime(worst_day['date'], '%Y-%m-%d').strftime('%A, %B %d'),
            'mood': worst_day['mood_rating']
        },
        'most_consistent': most_consistent
    }
    
    return report

def calculate_progress_badges(logs):
    """
    Calculate achievement badges for gamification
    """
    badges = []
    
    if not logs:
        return badges
    
    # Consistency badge
    if len(logs) >= 7:
        badges.append({
            'name': 'Week Warrior',
            'description': 'Logged 7 days in a row',
            'icon': '🏆'
        })
    
    if len(logs) >= 30:
        badges.append({
            'name': 'Monthly Master',
            'description': 'Logged 30 days',
            'icon': '⭐'
        })
    
    # Sleep champion
    good_sleep_days = len([log for log in logs if log['sleep_hours'] >= 7])
    if good_sleep_days >= 5:
        badges.append({
            'name': 'Sleep Champion',
            'description': 'Got 7+ hours of sleep for 5+ days',
            'icon': '😴'
        })
    
    # Exercise enthusiast
    exercise_days = len([log for log in logs if log['exercise_minutes'] >= 30])
    if exercise_days >= 5:
        badges.append({
            'name': 'Fitness Enthusiast',
            'description': 'Exercised 30+ minutes for 5+ days',
            'icon': '💪'
        })
    
    # Hydration hero
    hydrated_days = len([log for log in logs if log['water_intake'] >= 8])
    if hydrated_days >= 5:
        badges.append({
            'name': 'Hydration Hero',
            'description': 'Drank 8+ glasses of water for 5+ days',
            'icon': '💧'
        })
    
    # High productivity
    productive_days = len([log for log in logs if log['productivity_score'] >= 80])
    if productive_days >= 3:
        badges.append({
            'name': 'Productivity Pro',
            'description': 'Achieved 80+% productivity for 3+ days',
            'icon': '🚀'
        })
    
    return badges

def get_metric_name(metric_key):
    """Get friendly name for metric"""
    names = {
        'sleep_hours': 'Sleep',
        'mood_rating': 'Mood',
        'study_hours': 'Study Time',
        'water_intake': 'Water Intake',
        'exercise_minutes': 'Exercise',
        'productivity_score': 'Productivity'
    }
    return names.get(metric_key, metric_key)