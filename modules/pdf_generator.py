"""
PDF Generator Module
Creates beautiful PDFs for meal plans
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os

def generate_meal_plan_pdf(meal_plan, user_profile, filename):
    """
    Generate a beautiful PDF for the meal plan
    """
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#FF69B4'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#FF1493'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#C71585'),
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    # Title
    title = Paragraph("Your Personalized 7-Day Meal Plan", title_style)
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # Date
    date_text = Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", 
                         styles['Normal'])
    story.append(date_text)
    story.append(Spacer(1, 0.3*inch))
    
    # User Profile Summary
    profile_heading = Paragraph("Your Fitness Profile", heading_style)
    story.append(profile_heading)
    
    profile_data = [
        ['BMI', f"{user_profile['bmi']} ({user_profile['bmi_category']})"],
        ['Daily Calorie Goal', f"{user_profile['calorie_goal']} calories"],
        ['Protein Target', f"{user_profile['macros']['protein']}g"],
        ['Carbs Target', f"{user_profile['macros']['carbs']}g"],
        ['Fats Target', f"{user_profile['macros']['fats']}g"]
    ]
    
    profile_table = Table(profile_data, colWidths=[2.5*inch, 3*inch])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FFB6C1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#800080')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#DDA0DD'))
    ]))
    
    story.append(profile_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Meal Plan
    meals_heading = Paragraph("Your Weekly Meal Plan", heading_style)
    story.append(meals_heading)
    story.append(Spacer(1, 0.2*inch))
    
    # Generate each day
    for day_data in meal_plan:
        day_heading = Paragraph(f"Day {day_data['day']}", subheading_style)
        story.append(day_heading)
        
        # Create table for the day
        day_meals = [
            ['Meal', 'Food', 'Calories', 'Protein', 'Carbs', 'Fats'],
            [
                'Breakfast',
                day_data['breakfast']['name'],
                str(day_data['breakfast']['calories']),
                f"{day_data['breakfast']['protein']}g",
                f"{day_data['breakfast']['carbs']}g",
                f"{day_data['breakfast']['fats']}g"
            ],
            [
                'Lunch',
                day_data['lunch']['name'],
                str(day_data['lunch']['calories']),
                f"{day_data['lunch']['protein']}g",
                f"{day_data['lunch']['carbs']}g",
                f"{day_data['lunch']['fats']}g"
            ],
            [
                'Dinner',
                day_data['dinner']['name'],
                str(day_data['dinner']['calories']),
                f"{day_data['dinner']['protein']}g",
                f"{day_data['dinner']['carbs']}g",
                f"{day_data['dinner']['fats']}g"
            ],
            [
                'Snack',
                day_data['snack']['name'],
                str(day_data['snack']['calories']),
                f"{day_data['snack']['protein']}g",
                f"{day_data['snack']['carbs']}g",
                f"{day_data['snack']['fats']}g"
            ],
            [
                'TOTAL',
                '',
                str(day_data['daily_total']['calories']),
                f"{day_data['daily_total']['protein']}g",
                f"{day_data['daily_total']['carbs']}g",
                f"{day_data['daily_total']['fats']}g"
            ]
        ]
        
        day_table = Table(day_meals, colWidths=[0.8*inch, 2.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
        day_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF69B4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Data rows
            ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#FFF0F5')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#4B0082')),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
            
            # Total row
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#DDA0DD')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#DB7093')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(day_table)
        story.append(Spacer(1, 0.3*inch))
    
    # Tips section
    story.append(PageBreak())
    tips_heading = Paragraph("Helpful Tips", heading_style)
    story.append(tips_heading)
    
    tips = [
        "• Drink at least 8 glasses of water daily",
        "• Prepare meals in advance to stay on track",
        "• Feel free to swap meals within the same category",
        "• Listen to your body and adjust portions if needed",
        "• Combine this meal plan with regular exercise",
        "• Get 7-9 hours of sleep for optimal results"
    ]
    
    for tip in tips:
        tip_para = Paragraph(tip, styles['Normal'])
        story.append(tip_para)
        story.append(Spacer(1, 0.1*inch))
    
    # Build PDF
    doc.build(story)
    
    return filename