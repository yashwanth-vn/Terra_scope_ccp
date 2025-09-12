#!/usr/bin/env python3

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from database import db
from models.user import User
from models.soil_data import SoilData
from services.enhanced_predictor import enhanced_predictor
import json

def add_diverse_soil_samples():
    """Add diverse soil samples for testing ML predictions"""
    
    with app.app_context():
        # Get demo user
        user = User.query.filter_by(email='demo@terrascope.com').first()
        if not user:
            print("❌ Demo user not found. Run 'python manage_db.py sample-user' first.")
            return
        
        # Clear existing soil data for clean testing
        SoilData.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        print("🗑️ Cleared existing soil data")
        
        # Define diverse test cases
        test_cases = [
            {
                'name': 'Very Acidic Poor Soil',
                'data': {
                    'ph': 4.2,
                    'nitrogen': 25,
                    'phosphorus': 6,
                    'potassium': 40,
                    'organic_carbon': 0.5,
                    'moisture': 12,
                    'crop_type': 'Blueberries',
                    'season': 'Spring'
                }
            },
            {
                'name': 'Excellent Fertile Soil',
                'data': {
                    'ph': 6.8,
                    'nitrogen': 200,
                    'phosphorus': 55,
                    'potassium': 280,
                    'organic_carbon': 4.2,
                    'moisture': 32,
                    'crop_type': 'Tomatoes',
                    'season': 'Summer'
                }
            },
            {
                'name': 'Alkaline Clay Soil',
                'data': {
                    'ph': 8.5,
                    'nitrogen': 85,
                    'phosphorus': 18,
                    'potassium': 120,
                    'organic_carbon': 1.8,
                    'moisture': 35,
                    'crop_type': 'Asparagus',
                    'season': 'Spring'
                }
            },
            {
                'name': 'Sandy Desert Soil',
                'data': {
                    'ph': 7.8,
                    'nitrogen': 35,
                    'phosphorus': 8,
                    'potassium': 60,
                    'organic_carbon': 0.3,
                    'moisture': 8,
                    'crop_type': 'Cacti',
                    'season': 'All Season'
                }
            }
        ]
        
        print("🌱 Adding diverse soil samples...")
        
        for i, test_case in enumerate(test_cases):
            # Create soil data record
            soil_data = SoilData(
                user_id=user.id,
                ph=test_case['data']['ph'],
                nitrogen=test_case['data']['nitrogen'],
                phosphorus=test_case['data']['phosphorus'],
                potassium=test_case['data']['potassium'],
                organic_carbon=test_case['data']['organic_carbon'],
                moisture=test_case['data']['moisture'],
                crop_type=test_case['data']['crop_type'],
                season=test_case['data']['season']
            )
            
            # Get ML predictions for this data
            soil_params = {
                'ph': test_case['data']['ph'],
                'nitrogen': test_case['data']['nitrogen'],
                'phosphorus': test_case['data']['phosphorus'],
                'potassium': test_case['data']['potassium'],
                'organic_matter': test_case['data']['organic_carbon'],
                'moisture': test_case['data']['moisture']
            }
            
            prediction = enhanced_predictor.predict_fertility(soil_params)
            
            # Update soil data with predictions
            soil_data.fertility_level = prediction['fertility_level']
            soil_data.fertility_score = prediction['fertility_score']
            soil_data.recommendations = json.dumps(prediction['fertilizer_recommendations'])
            soil_data.crop_suggestions = json.dumps(prediction['crop_recommendations'])
            
            db.session.add(soil_data)
            
            print(f"   {i+1}. {test_case['name']}:")
            print(f"      pH: {test_case['data']['ph']}, N: {test_case['data']['nitrogen']}, P: {test_case['data']['phosphorus']}, K: {test_case['data']['potassium']}")
            print(f"      Result: {prediction['fertility_level']} (Score: {prediction['fertility_score']})")
            print(f"      Fertilizers: {', '.join(prediction['fertilizer_recommendations'][:2])}")
        
        # Commit all changes
        db.session.commit()
        print(f"\\n✅ Successfully added {len(test_cases)} diverse soil samples!")
        print("\\n🎯 Now test the dashboard - each sample should show different results!")
        
        # Show latest record for verification
        latest = SoilData.query.filter_by(user_id=user.id).order_by(SoilData.created_at.desc()).first()
        if latest:
            print(f"\\n📊 Latest record: {latest.fertility_level} soil (Score: {latest.fertility_score})")

if __name__ == "__main__":
    add_diverse_soil_samples()
