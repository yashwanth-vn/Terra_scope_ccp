#!/usr/bin/env python3
"""
Model training script for Terra Scope Enhanced Fertility Predictor
Run this script to train and save the machine learning models.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml_models.enhanced_fertility_model import enhanced_predictor

def main():
    print("🌱 Terra Scope Enhanced ML Model Training")
    print("=" * 50)
    
    # Train the model
    print("Starting model training...")
    results = enhanced_predictor.train_model()
    
    print("\n✅ Training completed successfully!")
    print(f"📊 Model Performance:")
    print(f"   • Fertility Score R² Score: {results['score_r2']:.3f}")
    print(f"   • Fertility Level Accuracy: {results['level_accuracy']:.3f}")
    
    # Test the model with sample data
    print("\n🧪 Testing model with sample predictions...")
    
    test_cases = [
        {
            'name': 'High Fertility Soil',
            'params': (6.8, 180, 35, 250, 2.5, 28)
        },
        {
            'name': 'Medium Fertility Soil',
            'params': (6.2, 120, 20, 150, 1.8, 25)
        },
        {
            'name': 'Low Fertility Soil',
            'params': (5.5, 60, 10, 80, 0.8, 20)
        },
        {
            'name': 'Acidic Soil',
            'params': (4.8, 100, 15, 120, 1.2, 22)
        },
        {
            'name': 'Alkaline Soil',
            'params': (8.2, 90, 25, 140, 1.5, 24)
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🔍 {test_case['name']}:")
        ph, n, p, k, oc, moisture = test_case['params']
        print(f"   pH: {ph}, N: {n}, P: {p}, K: {k}, OC: {oc}%, Moisture: {moisture}%")
        
        prediction = enhanced_predictor.predict(test_case['params'])
        
        print(f"   ✨ Fertility: {prediction['fertility_level']} ({prediction['fertility_score']:.1f}/100)")
        print(f"   🎯 Confidence: {prediction['confidence']:.1f}%")
        print(f"   🌾 Top Crops: {', '.join([crop['name'] for crop in prediction['crop_suggestions']['highly_suitable'][:3]])}")
        
        if prediction['fertilizer_recommendations']['primary_fertilizers']:
            top_fertilizer = prediction['fertilizer_recommendations']['primary_fertilizers'][0]
            print(f"   💡 Primary Fertilizer: {top_fertilizer['name']} - {top_fertilizer['application_rate']}")
    
    print("\n🎉 Model training and testing completed successfully!")
    print("The trained models are now ready for use in the Terra Scope application.")
    
    # Train the model once more to ensure it's properly saved
    enhanced_predictor.train_model()

if __name__ == '__main__':
    main()
