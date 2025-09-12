#!/usr/bin/env python3

from services.enhanced_predictor import enhanced_predictor
import json

# Test with very different soil conditions
test_cases = [
    {
        'name': 'Very Poor Soil',
        'data': {'ph': 4.5, 'nitrogen': 30, 'phosphorus': 8, 'potassium': 50, 'organic_matter': 0.8, 'moisture': 15}
    },
    {
        'name': 'Excellent Soil', 
        'data': {'ph': 7.2, 'nitrogen': 180, 'phosphorus': 45, 'potassium': 220, 'organic_matter': 3.5, 'moisture': 28}
    },
    {
        'name': 'Alkaline Poor Soil',
        'data': {'ph': 8.8, 'nitrogen': 60, 'phosphorus': 12, 'potassium': 80, 'organic_matter': 1.2, 'moisture': 18}
    }
]

print('🧪 Testing ML model with different inputs:')
print('=' * 60)

for i, test_case in enumerate(test_cases):
    test_data = test_case['data']
    result = enhanced_predictor.predict_fertility(test_data)
    
    print(f"\n{i+1}. {test_case['name']}:")
    print(f"   Input: pH={test_data['ph']}, N={test_data['nitrogen']}, P={test_data['phosphorus']}, K={test_data['potassium']}")
    print(f"   Result: {result['fertility_level']} - Score: {result['fertility_score']}")
    print(f"   Fertilizers: {', '.join(result['fertilizer_recommendations'][:3])}")
    print(f"   Crops: {', '.join(result['crop_recommendations'][:3])}")

# Check if models are actually loaded
print(f"\n🔍 Model Status:")
print(f"   Models loaded: {enhanced_predictor.models_loaded}")
if enhanced_predictor.models_loaded:
    print(f"   Expected features: {len(enhanced_predictor.feature_columns)}")
    print(f"   Features: {enhanced_predictor.feature_columns}")
else:
    print("   ❌ Models not loaded - using fallback predictions!")
