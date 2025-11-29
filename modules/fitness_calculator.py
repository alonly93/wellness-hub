"""
Fitness Calculator Module
Handles BMI calculations and calorie requirements
"""

def calculate_bmi(weight_kg, height_cm):
    """Calculate Body Mass Index"""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi):
    """Return BMI category"""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_bmr(age, weight_kg, height_cm, gender):
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation
    More accurate than Harris-Benedict
    """
    if gender.lower() == 'male':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    
    return round(bmr, 2)

def calculate_tdee(bmr, activity_level):
    """
    Calculate Total Daily Energy Expenditure
    Activity levels:
    - sedentary: little or no exercise
    - light: exercise 1-3 days/week
    - moderate: exercise 3-5 days/week
    - active: exercise 6-7 days/week
    - very_active: intense exercise daily
    """
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    multiplier = activity_multipliers.get(activity_level.lower(), 1.2)
    tdee = bmr * multiplier
    
    return round(tdee, 2)

def calculate_calorie_goal(tdee, goal):
    """
    Calculate daily calorie goal based on fitness goal
    - lose: 500 calorie deficit (lose ~0.5kg/week)
    - gain: 500 calorie surplus (gain ~0.5kg/week)
    - maintain: no change
    """
    if goal.lower() == 'lose':
        return round(tdee - 500, 2)
    elif goal.lower() == 'gain':
        return round(tdee + 500, 2)
    else:  # maintain
        return round(tdee, 2)

def calculate_macros(calories, goal):
    """
    Calculate macro distribution (protein, carbs, fats)
    Based on common recommendations for different goals
    """
    if goal.lower() == 'lose':
        # High protein, moderate carbs, moderate fat
        protein_ratio = 0.35
        carbs_ratio = 0.35
        fat_ratio = 0.30
    elif goal.lower() == 'gain':
        # High protein, high carbs, moderate fat
        protein_ratio = 0.30
        carbs_ratio = 0.45
        fat_ratio = 0.25
    else:  # maintain
        # Balanced
        protein_ratio = 0.30
        carbs_ratio = 0.40
        fat_ratio = 0.30
    
    # Calculate grams (4 cal per g protein/carbs, 9 cal per g fat)
    protein_grams = round((calories * protein_ratio) / 4, 1)
    carbs_grams = round((calories * carbs_ratio) / 4, 1)
    fat_grams = round((calories * fat_ratio) / 9, 1)
    
    return {
        'protein': protein_grams,
        'carbs': carbs_grams,
        'fats': fat_grams
    }

def get_complete_profile(age, weight_kg, height_cm, gender, activity_level, goal):
    """
    Generate complete fitness profile with all calculations
    """
    bmi = calculate_bmi(weight_kg, height_cm)
    bmi_category = get_bmi_category(bmi)
    bmr = calculate_bmr(age, weight_kg, height_cm, gender)
    tdee = calculate_tdee(bmr, activity_level)
    calorie_goal = calculate_calorie_goal(tdee, goal)
    macros = calculate_macros(calorie_goal, goal)
    
    return {
        'bmi': bmi,
        'bmi_category': bmi_category,
        'bmr': bmr,
        'tdee': tdee,
        'calorie_goal': calorie_goal,
        'macros': macros
    }