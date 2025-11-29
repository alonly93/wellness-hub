"""
Wellness Hub - Main Flask Application with Database
Three integrated apps: Fitness Planner, Mental Health Journal, Self-Tracking Dashboard
"""

from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
from datetime import datetime, date
import os

# Import configuration
from config import config

# Import database models
from models import db, JournalEntry, DailyLog, MealPlan

# Import modules
from modules.fitness_calculator import get_complete_profile
from modules.meal_generator import generate_meal_plan, generate_grocery_list
from modules.pdf_generator import generate_meal_plan_pdf
from modules.sentiment_analyzer import (
    analyze_sentiment, extract_keywords, analyze_mood_trend,
    generate_weekly_summary, calculate_streak
)
from modules.insights_generator import (
    calculate_averages, calculate_trends, find_correlations,
    generate_weekly_report, calculate_progress_badges
)

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize database

db.init_app(app)

# Create tables within app context
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")

# Create all database tables
with app.app_context():
       db.create_all()

# ===================== ROUTES =====================

# Landing Page
@app.route('/')
def landing():
    """Main landing page"""
    return render_template('landing.html')

# ===================== FITNESS PLANNER =====================

@app.route('/fitness')
def fitness_input():
    """Fitness planner input page"""
    return render_template('fitness/input.html')

@app.route('/fitness/calculate', methods=['POST'])
def fitness_calculate():
    """Calculate fitness profile and generate meal plan"""
    # Get form data
    age = int(request.form.get('age'))
    weight = float(request.form.get('weight'))
    height = float(request.form.get('height'))
    gender = request.form.get('gender')
    activity_level = request.form.get('activity_level')
    goal = request.form.get('goal')
    
    # Dietary restrictions
    restrictions = request.form.getlist('restrictions')
    
    # Calculate fitness profile
    profile = get_complete_profile(age, weight, height, gender, activity_level, goal)
    
    # Generate meal plan
    meal_plan = generate_meal_plan(profile['calorie_goal'], restrictions)
    
    # Generate grocery list
    grocery_list = generate_grocery_list(meal_plan)
    
    # Save to database
    new_plan = MealPlan(
        age=age,
        weight=weight,
        height=height,
        gender=gender,
        activity_level=activity_level,
        goal=goal,
        restrictions=restrictions,
        bmi=profile['bmi'],
        bmr=profile['bmr'],
        calorie_goal=profile['calorie_goal'],
        meal_plan_data=meal_plan
    )
    db.session.add(new_plan)
    db.session.commit()
    
    # Store in session for PDF generation and meal swapping
    session['fitness_profile'] = profile
    session['meal_plan'] = meal_plan
    session['grocery_list'] = grocery_list
    session['user_info'] = {
        'age': age,
        'weight': weight,
        'height': height,
        'gender': gender,
        'activity_level': activity_level,
        'goal': goal,
        'restrictions': restrictions
    }
    
    return render_template('fitness/results.html',
                         profile=profile,
                         meal_plan=meal_plan,
                         grocery_list=grocery_list)

@app.route('/fitness/download-pdf')
def fitness_download_pdf():
    """Generate and download meal plan as PDF"""
    meal_plan = session.get('meal_plan')
    profile = session.get('fitness_profile')
    
    if not meal_plan or not profile:
        return redirect(url_for('fitness_input'))
    
    # Generate PDF
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(app.config['MEAL_PLANS_DIR'], f'meal_plan_{timestamp}.pdf')
    
    generate_meal_plan_pdf(meal_plan, profile, filename)
    
    return send_file(filename, as_attachment=True, download_name='my_meal_plan.pdf')

@app.route('/fitness/swap-meal', methods=['POST'])
def swap_meal():
    """Swap a meal with a new option"""
    data = request.json
    day = int(data.get('day'))
    meal_type = data.get('meal_type')
    
    meal_plan = session.get('meal_plan')
    restrictions = session.get('user_info', {}).get('restrictions', [])
    calorie_goal = session.get('fitness_profile', {}).get('calorie_goal', 2000)
    
    if meal_plan:
        # Generate new meal for that slot
        new_plan = generate_meal_plan(calorie_goal, restrictions, days=1)
        new_meal = new_plan[0][meal_type]
        
        # Update meal plan
        meal_plan[day - 1][meal_type] = new_meal
        
        # Recalculate daily total
        day_data = meal_plan[day - 1]
        day_data['daily_total'] = {
            'calories': sum([day_data[m]['calories'] for m in ['breakfast', 'lunch', 'dinner', 'snack']]),
            'protein': round(sum([day_data[m]['protein'] for m in ['breakfast', 'lunch', 'dinner', 'snack']]), 1),
            'carbs': round(sum([day_data[m]['carbs'] for m in ['breakfast', 'lunch', 'dinner', 'snack']]), 1),
            'fats': round(sum([day_data[m]['fats'] for m in ['breakfast', 'lunch', 'dinner', 'snack']]), 1)
        }
        
        session['meal_plan'] = meal_plan
        
        return jsonify({'success': True, 'new_meal': new_meal, 'daily_total': day_data['daily_total']})
    
    return jsonify({'success': False})

# ===================== MENTAL HEALTH JOURNAL =====================

@app.route('/journal')
def journal_write():
    """Journal writing page"""
    entries = JournalEntry.query.order_by(JournalEntry.date.desc()).all()
    streak = calculate_streak([e.to_dict() for e in entries])
    return render_template('journal/write.html', streak=streak)

@app.route('/journal/save', methods=['POST'])
def journal_save():
    """Save journal entry"""
    content = request.form.get('content')
    title = request.form.get('title', 'Untitled Entry')
    
    if content:
        # Analyze sentiment
        analysis = analyze_sentiment(content)
        
        # Create entry
        entry = JournalEntry(
            title=title,
            content=content,
            date=datetime.now().date(),
            time=datetime.now().time(),
            sentiment=analysis['sentiment'],
            score=analysis['score'],
            polarity=analysis.get('polarity'),
            subjectivity=analysis.get('subjectivity')
        )
        
        db.session.add(entry)
        db.session.commit()
    
    return redirect(url_for('journal_entries'))

@app.route('/journal/entries')
def journal_entries():
    """View all journal entries"""
    entries = JournalEntry.query.order_by(JournalEntry.date.desc(), JournalEntry.time.desc()).all()
    entries_dict = [e.to_dict() for e in entries]
    
    return render_template('journal/entries.html', entries=entries_dict)

@app.route('/journal/delete/<int:entry_id>')
def journal_delete(entry_id):
    """Delete a journal entry"""
    entry = JournalEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    
    return redirect(url_for('journal_entries'))

@app.route('/journal/edit/<int:entry_id>')
def journal_edit(entry_id):
    """Edit a journal entry"""
    entry = JournalEntry.query.get_or_404(entry_id)
    entry_dict = entry.to_dict()
    entry_dict['id'] = entry_id
    
    return render_template('journal/write.html', entry=entry_dict, editing=True)

@app.route('/journal/update/<int:entry_id>', methods=['POST'])
def journal_update(entry_id):
    """Update an existing journal entry"""
    content = request.form.get('content')
    title = request.form.get('title', 'Untitled Entry')
    
    entry = JournalEntry.query.get_or_404(entry_id)
    
    # Re-analyze sentiment
    analysis = analyze_sentiment(content)
    
    entry.title = title
    entry.content = content
    entry.sentiment = analysis['sentiment']
    entry.score = analysis['score']
    entry.polarity = analysis.get('polarity')
    entry.subjectivity = analysis.get('subjectivity')
    entry.edited_at = datetime.now()
    
    db.session.commit()
    
    return redirect(url_for('journal_entries'))

@app.route('/journal/analysis')
def journal_analysis():
    """View mood analysis and trends"""
    entries = JournalEntry.query.order_by(JournalEntry.date).all()
    entries_dict = [e.to_dict() for e in entries]
    
    if not entries_dict:
        return render_template('journal/analysis.html', no_data=True)
    
    # Analyze trends
    trend_data = analyze_mood_trend(entries_dict)
    weekly_summary = generate_weekly_summary(entries_dict)
    
    # Extract common keywords
    all_text = ' '.join([e.content for e in entries])
    keywords = extract_keywords(all_text, top_n=15)
    
    # Prepare chart data
    chart_data = {
        'dates': list(trend_data['daily_scores'].keys()),
        'scores': list(trend_data['daily_scores'].values()),
        'sentiment_labels': list(trend_data['sentiment_distribution'].keys()),
        'sentiment_counts': list(trend_data['sentiment_distribution'].values())
    }
    
    return render_template('journal/analysis.html',
                         trend_data=trend_data,
                         weekly_summary=weekly_summary,
                         keywords=keywords,
                         chart_data=chart_data,
                         no_data=False)

@app.route('/journal/download')
def journal_download():
    """Download all entries as text file"""
    entries = JournalEntry.query.order_by(JournalEntry.date).all()
    
    # Create text content
    content = "MY JOURNAL ENTRIES\n"
    content += "=" * 50 + "\n\n"
    
    for entry in entries:
        content += f"Date: {entry.date.strftime('%Y-%m-%d')} at {entry.time.strftime('%H:%M')}\n"
        content += f"Title: {entry.title}\n"
        content += f"Mood: {entry.sentiment.title() if entry.sentiment else 'N/A'}\n"
        content += "-" * 50 + "\n"
        content += entry.content + "\n"
        content += "=" * 50 + "\n\n"
    
    # Save to temp file
    temp_file = os.path.join(app.config['DATA_DIR'], 'journal_export.txt')
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return send_file(temp_file, as_attachment=True, download_name='my_journal.txt')

# ===================== SELF-TRACKING DASHBOARD =====================

@app.route('/dashboard')
def dashboard_log():
    """Dashboard log input page"""
    return render_template('dashboard/log.html', today=date.today().strftime('%Y-%m-%d'))

@app.route('/dashboard/save', methods=['POST'])
def dashboard_save():
    """Save daily log"""
    log_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
    
    # Check if entry exists
    log = DailyLog.query.filter_by(date=log_date).first()
    
    if log:
        # Update existing
        log.sleep_hours = float(request.form.get('sleep_hours', 0))
        log.mood_rating = float(request.form.get('mood_rating', 5))
        log.study_hours = float(request.form.get('study_hours', 0))
        log.water_intake = int(request.form.get('water_intake', 0))
        log.exercise_minutes = int(request.form.get('exercise_minutes', 0))
        log.productivity_score = int(request.form.get('productivity_score', 50))
    else:
        # Create new
        log = DailyLog(
            date=log_date,
            sleep_hours=float(request.form.get('sleep_hours', 0)),
            mood_rating=float(request.form.get('mood_rating', 5)),
            study_hours=float(request.form.get('study_hours', 0)),
            water_intake=int(request.form.get('water_intake', 0)),
            exercise_minutes=int(request.form.get('exercise_minutes', 0)),
            productivity_score=int(request.form.get('productivity_score', 50))
        )
        db.session.add(log)
    
    db.session.commit()
    
    return redirect(url_for('dashboard_view'))

@app.route('/dashboard/view')
def dashboard_view():
    """View dashboard with all metrics and insights"""
    logs = DailyLog.query.order_by(DailyLog.date).all()
    logs_dict = [log.to_dict() for log in logs]
    
    if not logs_dict:
        return render_template('dashboard/view.html', no_data=True)
    
    # Calculate analytics
    averages = calculate_averages(logs_dict)
    trends = calculate_trends(logs_dict) if len(logs_dict) >= 7 else None
    insights = find_correlations(logs_dict)
    weekly_report = generate_weekly_report(logs_dict)
    badges = calculate_progress_badges(logs_dict)
    
    # Prepare chart data
    chart_data = {
        'dates': [log['date'] for log in logs_dict[-30:]],
        'sleep': [log['sleep_hours'] for log in logs_dict[-30:]],
        'mood': [log['mood_rating'] for log in logs_dict[-30:]],
        'study': [log['study_hours'] for log in logs_dict[-30:]],
        'water': [log['water_intake'] for log in logs_dict[-30:]],
        'exercise': [log['exercise_minutes'] for log in logs_dict[-30:]],
        'productivity': [log['productivity_score'] for log in logs_dict[-30:]]
    }
    
    return render_template('dashboard/view.html',
                         logs=logs_dict[-7:],
                         averages=averages,
                         trends=trends,
                         insights=insights,
                         weekly_report=weekly_report,
                         badges=badges,
                         chart_data=chart_data,
                         no_data=False)

@app.route('/dashboard/export-csv')
def dashboard_export():
    """Export all data as CSV"""
    logs = DailyLog.query.order_by(DailyLog.date).all()
    
    # Create CSV content
    csv_content = "Date,Sleep Hours,Mood Rating,Study Hours,Water Intake,Exercise Minutes,Productivity Score\n"
    
    for log in logs:
        csv_content += f"{log.date.strftime('%Y-%m-%d')},{log.sleep_hours},{log.mood_rating},"
        csv_content += f"{log.study_hours},{log.water_intake},{log.exercise_minutes},"
        csv_content += f"{log.productivity_score}\n"
    
    # Save to temp file
    temp_file = os.path.join(app.config['DATA_DIR'], 'dashboard_export.csv')
    with open(temp_file, 'w') as f:
        f.write(csv_content)
    
    return send_file(temp_file, as_attachment=True, download_name='my_tracking_data.csv')

# ===================== ERROR HANDLERS =====================

@app.errorhandler(404)
def not_found(e):
    return render_template('landing.html'), 404

@app.errorhandler(500)
def server_error(e):
    return "Internal server error. Please try again.", 500

# ===================== RUN APPLICATION =====================

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    
