"""
Meal Plan Generator Module
Generates 7-day meal plans based on dietary restrictions and calorie goals
"""

import random

# Meal database with different dietary options
MEALS = {
    'breakfast': [
        {
            'name': 'Oatmeal with Berries and Almonds',
            'calories': 350,
            'protein': 12,
            'carbs': 55,
            'fats': 10,
            'tags': ['vegetarian', 'vegan', 'halal']
        },
        {
            'name': 'Scrambled Eggs with Whole Wheat Toast',
            'calories': 400,
            'protein': 25,
            'carbs': 35,
            'fats': 15,
            'tags': ['vegetarian', 'halal']
        },
        {
            'name': 'Greek Yogurt Parfait with Granola',
            'calories': 380,
            'protein': 20,
            'carbs': 50,
            'fats': 10,
            'tags': ['vegetarian', 'halal']
        },
        {
            'name': 'Avocado Toast with Chickpeas',
            'calories': 420,
            'protein': 15,
            'carbs': 45,
            'fats': 18,
            'tags': ['vegetarian', 'vegan', 'halal']
        },
        {
            'name': 'Smoothie Bowl with Banana and Chia Seeds',
            'calories': 360,
            'protein': 10,
            'carbs': 60,
            'fats': 8,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        },
        {
            'name': 'Whole Grain Pancakes with Maple Syrup',
            'calories': 450,
            'protein': 14,
            'carbs': 70,
            'fats': 12,
            'tags': ['vegetarian', 'halal']
        },
        {
            'name': 'Protein Smoothie with Almond Milk',
            'calories': 320,
            'protein': 25,
            'carbs': 35,
            'fats': 8,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        }
    ],
    'lunch': [
        {
            'name': 'Quinoa Salad with Roasted Vegetables',
            'calories': 480,
            'protein': 18,
            'carbs': 65,
            'fats': 15,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        },
        {
            'name': 'Grilled Chicken Wrap with Hummus',
            'calories': 520,
            'protein': 35,
            'carbs': 50,
            'fats': 18,
            'tags': ['halal']
        },
        {
            'name': 'Lentil Soup with Whole Grain Bread',
            'calories': 450,
            'protein': 22,
            'carbs': 70,
            'fats': 8,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        },
        {
            'name': 'Chickpea and Spinach Curry with Rice',
            'calories': 500,
            'protein': 20,
            'carbs': 75,
            'fats': 12,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        },
        {
            'name': 'Veggie Burger with Sweet Potato Fries',
            'calories': 550,
            'protein': 25,
            'carbs': 68,
            'fats': 20,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        },
        {
            'name': 'Tuna Salad with Mixed Greens',
            'calories': 420,
            'protein': 35,
            'carbs': 25,
            'fats': 20,
            'tags': ['halal', 'lactose_free']
        },
        {
            'name': 'Falafel Bowl with Tahini Sauce',
            'calories': 510,
            'protein': 18,
            'carbs': 60,
            'fats': 22,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        }
    ],
    'dinner': [
        {
            'name': 'Baked Salmon with Asparagus and Brown Rice',
            'calories': 580,
            'protein': 40,
            'carbs': 55,
            'fats': 18,
            'tags': ['halal', 'lactose_free']
        },
        {
            'name': 'Stir-Fried Tofu with Vegetables and Noodles',
            'calories': 520,
            'protein': 25,
            'carbs': 65,
            'fats': 15,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        },
        {
            'name': 'Grilled Chicken Breast with Roasted Potatoes',
            'calories': 550,
            'protein': 45,
            'carbs': 50,
            'fats': 15,
            'tags': ['halal', 'lactose_free']
        },
        {
            'name': 'Vegetable Lasagna with Marinara',
            'calories': 500,
            'protein': 22,
            'carbs': 60,
            'fats': 18,
            'tags': ['vegetarian', 'halal']
        },
        {
            'name': 'Black Bean and Sweet Potato Enchiladas',
            'calories': 530,
            'protein': 20,
            'carbs': 75,
            'fats': 16,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        },
        {
            'name': 'Mushroom Risotto with Garden Salad',
            'calories': 490,
            'protein': 15,
            'carbs': 70,
            'fats': 16,
            'tags': ['vegetarian', 'halal']
        },
        {
            'name': 'Grilled Portobello Mushroom Steaks',
            'calories': 460,
            'protein': 18,
            'carbs': 55,
            'fats': 20,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        }
    ],
    'snacks': [
        {
            'name': 'Apple with Almond Butter',
            'calories': 200,
            'protein': 5,
            'carbs': 25,
            'fats': 10,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        },
        {
            'name': 'Hummus with Carrot Sticks',
            'calories': 150,
            'protein': 6,
            'carbs': 18,
            'fats': 6,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        },
        {
            'name': 'Trail Mix with Dried Fruits',
            'calories': 180,
            'protein': 5,
            'carbs': 22,
            'fats': 9,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        },
        {
            'name': 'Protein Bar',
            'calories': 220,
            'protein': 15,
            'carbs': 25,
            'fats': 8,
            'tags': ['vegetarian', 'halal']
        },
        {
            'name': 'Rice Cakes with Peanut Butter',
            'calories': 190,
            'protein': 7,
            'carbs': 20,
            'fats': 9,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        },
        {
            'name': 'Fresh Fruit Salad',
            'calories': 120,
            'protein': 2,
            'carbs': 30,
            'fats': 1,
            'tags': ['vegetarian', 'vegan', 'halal', 'lactose_free']
        }
    ]
}

def filter_meals_by_restrictions(meals, restrictions):
    """Filter meals based on dietary restrictions"""
    if not restrictions:
        return meals
    
    filtered = []
    for meal in meals:
        # Check if meal matches all restrictions
        if all(restriction in meal['tags'] for restriction in restrictions):
            filtered.append(meal)
    
    return filtered if filtered else meals  # Return all if no matches

def scale_meal(meal, target_calories, meal_type_calories):
    """Scale meal proportionally to meet calorie target"""
    if meal['calories'] == 0:
        return meal
    
    scale_factor = meal_type_calories / meal['calories']
    
    return {
        'name': meal['name'],
        'calories': round(meal['calories'] * scale_factor),
        'protein': round(meal['protein'] * scale_factor, 1),
        'carbs': round(meal['carbs'] * scale_factor, 1),
        'fats': round(meal['fats'] * scale_factor, 1)
    }

def generate_meal_plan(calorie_goal, restrictions, days=7):
    """
    Generate a complete meal plan
    restrictions: list of dietary restrictions ['vegetarian', 'halal', etc.]
    """
    # Calorie distribution (approximately)
    breakfast_cals = calorie_goal * 0.25
    lunch_cals = calorie_goal * 0.35
    dinner_cals = calorie_goal * 0.30
    snack_cals = calorie_goal * 0.10
    
    meal_plan = []
    
    for day in range(1, days + 1):
        # Filter meals by restrictions
        breakfast_options = filter_meals_by_restrictions(MEALS['breakfast'], restrictions)
        lunch_options = filter_meals_by_restrictions(MEALS['lunch'], restrictions)
        dinner_options = filter_meals_by_restrictions(MEALS['dinner'], restrictions)
        snack_options = filter_meals_by_restrictions(MEALS['snacks'], restrictions)
        
        # Select random meals
        breakfast = random.choice(breakfast_options)
        lunch = random.choice(lunch_options)
        dinner = random.choice(dinner_options)
        snack = random.choice(snack_options)
        
        # Scale meals to target calories
        breakfast = scale_meal(breakfast, calorie_goal, breakfast_cals)
        lunch = scale_meal(lunch, calorie_goal, lunch_cals)
        dinner = scale_meal(dinner, calorie_goal, dinner_cals)
        snack = scale_meal(snack, calorie_goal, snack_cals)
        
        # Calculate daily totals
        daily_total = {
            'calories': breakfast['calories'] + lunch['calories'] + dinner['calories'] + snack['calories'],
            'protein': round(breakfast['protein'] + lunch['protein'] + dinner['protein'] + snack['protein'], 1),
            'carbs': round(breakfast['carbs'] + lunch['carbs'] + dinner['carbs'] + snack['carbs'], 1),
            'fats': round(breakfast['fats'] + lunch['fats'] + dinner['fats'] + snack['fats'], 1)
        }
        
        day_plan = {
            'day': day,
            'breakfast': breakfast,
            'lunch': lunch,
            'dinner': dinner,
            'snack': snack,
            'daily_total': daily_total
        }
        
        meal_plan.append(day_plan)
    
    return meal_plan

def generate_grocery_list(meal_plan):
    """Generate a grocery list from meal plan"""
    # This is a simplified version - in production, you'd have ingredient data
    items = set()
    
    for day in meal_plan:
        items.add(day['breakfast']['name'])
        items.add(day['lunch']['name'])
        items.add(day['dinner']['name'])
        items.add(day['snack']['name'])
    
    return sorted(list(items))