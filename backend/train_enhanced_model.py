#!/usr/bin/env python3
"""
Enhanced Terra Scope ML Model Training with Synthetic Agricultural Data
Creates realistic soil fertility prediction models with varied outputs
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
import joblib
import random
import warnings
warnings.filterwarnings('ignore')

def generate_comprehensive_synthetic_data(n_samples=5000):
    """Generate comprehensive synthetic soil data with realistic relationships"""
    print(f"Generating {n_samples} synthetic soil samples...")
    
    np.random.seed(42)
    random.seed(42)
    
    # Define realistic ranges for soil parameters
    data = []
    
    for i in range(n_samples):
        # Basic soil properties
        ph = np.random.normal(6.8, 1.2)  # pH typically 5.5-8.5
        ph = np.clip(ph, 4.0, 9.5)
        
        # Organic matter (0.5-8%)
        organic_matter = np.random.exponential(2.5)
        organic_matter = np.clip(organic_matter, 0.5, 8.0)
        
        # Nutrients (mg/kg or ppm)
        nitrogen = np.random.gamma(2, 50)  # 20-300 ppm
        nitrogen = np.clip(nitrogen, 20, 400)
        
        phosphorus = np.random.gamma(1.5, 25)  # 10-150 ppm
        phosphorus = np.clip(phosphorus, 5, 200)
        
        potassium = np.random.gamma(2, 75)  # 50-400 ppm
        potassium = np.clip(potassium, 30, 600)
        
        # Micronutrients
        sulfur = np.random.gamma(1.8, 15)  # 10-50 ppm
        sulfur = np.clip(sulfur, 5, 80)
        
        magnesium = np.random.gamma(2, 30)  # 25-150 ppm
        magnesium = np.clip(magnesium, 15, 200)
        
        calcium = np.random.gamma(3, 100)  # 200-2000 ppm
        calcium = np.clip(calcium, 100, 2500)
        
        # Physical properties
        moisture = np.random.normal(25, 8)  # 10-50%
        moisture = np.clip(moisture, 8, 60)
        
        temperature = np.random.normal(22, 6)  # 10-35°C
        temperature = np.clip(temperature, 5, 45)
        
        # Soil texture (clay, silt, sand percentages)
        clay = np.random.normal(25, 12)
        clay = np.clip(clay, 5, 60)
        
        silt = np.random.normal(35, 15)
        silt = np.clip(silt, 10, 70)
        
        sand = 100 - clay - silt
        sand = np.clip(sand, 10, 80)
        
        # Normalize texture to sum to 100
        total = clay + silt + sand
        clay = (clay / total) * 100
        silt = (silt / total) * 100
        sand = (sand / total) * 100
        
        # Calculate fertility score based on multiple factors
        # pH factor (optimal around 6.5-7.0)
        ph_factor = 1.0 - abs(ph - 6.75) * 0.2
        ph_factor = max(0.2, ph_factor)
        
        # Nutrient factors
        n_factor = min(1.0, nitrogen / 200)  # Optimal around 200 ppm
        p_factor = min(1.0, phosphorus / 50)  # Optimal around 50 ppm  
        k_factor = min(1.0, potassium / 250)  # Optimal around 250 ppm
        
        # Organic matter factor
        om_factor = min(1.0, organic_matter / 4.0)  # Optimal around 4%
        
        # Moisture factor (optimal around 25-30%)
        if 20 <= moisture <= 35:
            moisture_factor = 1.0
        else:
            moisture_factor = max(0.3, 1.0 - abs(moisture - 27.5) * 0.03)
        
        # Temperature factor (optimal around 20-25°C)
        if 15 <= temperature <= 30:
            temp_factor = 1.0
        else:
            temp_factor = max(0.4, 1.0 - abs(temperature - 22.5) * 0.04)
        
        # Calculate base fertility score (0-100)
        fertility_score = (ph_factor * 0.2 + 
                          n_factor * 0.25 + 
                          p_factor * 0.2 + 
                          k_factor * 0.15 + 
                          om_factor * 0.1 + 
                          moisture_factor * 0.05 + 
                          temp_factor * 0.05) * 100
        
        # Add some controlled randomness
        fertility_score += np.random.normal(0, 3)
        fertility_score = np.clip(fertility_score, 15, 98)
        
        # Determine fertility level
        if fertility_score >= 80:
            fertility_level = "Excellent"
        elif fertility_score >= 65:
            fertility_level = "Good" 
        elif fertility_score >= 50:
            fertility_level = "Fair"
        elif fertility_score >= 35:
            fertility_level = "Poor"
        else:
            fertility_level = "Very Poor"
        
        # Determine fertilizer recommendation based on nutrient deficiencies
        fertilizer_recs = []
        
        if nitrogen < 80:
            fertilizer_recs.extend(["Urea", "Ammonium Sulfate", "Calcium Nitrate"])
        if phosphorus < 25:
            fertilizer_recs.extend(["Superphosphate", "DAP", "MAP"])
        if potassium < 120:
            fertilizer_recs.extend(["Potassium Chloride", "Potassium Sulfate"])
        if magnesium < 50:
            fertilizer_recs.extend(["Epsom Salt", "Dolomite"])
        if calcium < 400:
            fertilizer_recs.extend(["Lime", "Gypsum"])
        if sulfur < 20:
            fertilizer_recs.extend(["Elemental Sulfur", "Ammonium Sulfate"])
        
        # Default to balanced fertilizer if no deficiencies
        if not fertilizer_recs:
            fertilizer_recs = ["NPK Complex", "Balanced Fertilizer"]
        elif len(fertilizer_recs) > 3:
            # If many deficiencies, recommend NPK complex plus specific supplements
            fertilizer_recs = ["NPK Complex"] + random.sample(fertilizer_recs[:3], 2)
        
        fertilizer_rec = random.choice(fertilizer_recs)
        
        # Crop recommendations based on soil conditions
        crop_recs = []
        
        # pH-based crops
        if ph < 6.0:  # Acidic soil
            crop_recs.extend(["Blueberries", "Potatoes", "Sweet Potatoes", "Radishes"])
        elif ph > 7.5:  # Alkaline soil
            crop_recs.extend(["Asparagus", "Cabbage", "Sugar Beets"])
        else:  # Neutral soil
            crop_recs.extend(["Tomatoes", "Corn", "Wheat", "Soybeans", "Lettuce"])
        
        # Moisture-based crops
        if moisture > 35:
            crop_recs.extend(["Rice", "Celery", "Watercress"])
        elif moisture < 20:
            crop_recs.extend(["Cacti", "Succulents", "Drought-resistant crops"])
        else:
            crop_recs.extend(["Carrots", "Beans", "Peas", "Spinach"])
        
        # Fertility-based crops
        if fertility_score > 70:
            crop_recs.extend(["Leafy Greens", "Brassicas", "Heavy Feeders"])
        else:
            crop_recs.extend(["Legumes", "Root Vegetables", "Light Feeders"])
        
        # Select 2-4 diverse crop recommendations
        crop_rec = ", ".join(random.sample(list(set(crop_recs)), min(4, len(set(crop_recs)))))
        
        # Append data point
        data.append({
            'ph': round(ph, 2),
            'organic_matter': round(organic_matter, 2),
            'nitrogen': round(nitrogen, 1),
            'phosphorus': round(phosphorus, 1),
            'potassium': round(potassium, 1),
            'sulfur': round(sulfur, 1),
            'magnesium': round(magnesium, 1),
            'calcium': round(calcium, 1),
            'moisture': round(moisture, 1),
            'temperature': round(temperature, 1),
            'clay': round(clay, 1),
            'silt': round(silt, 1),
            'sand': round(sand, 1),
            'fertility_score': round(fertility_score, 1),
            'fertility_level': fertility_level,
            'fertilizer_recommendation': fertilizer_rec,
            'crop_recommendation': crop_rec
        })
    
    return pd.DataFrame(data)

def train_enhanced_models():
    """Train enhanced ML models with synthetic data"""
    print("Starting enhanced model training...")
    
    # Generate synthetic data
    df = generate_comprehensive_synthetic_data(5000)
    
    # Display data statistics
    print(f"\nDataset shape: {df.shape}")
    print(f"\nFertility score distribution:")
    print(df['fertility_score'].describe())
    print(f"\nFertility level distribution:")
    print(df['fertility_level'].value_counts())
    print(f"\nFertilizer recommendation distribution:")
    print(df['fertilizer_recommendation'].value_counts())
    
    # Prepare features for training
    feature_columns = ['ph', 'organic_matter', 'nitrogen', 'phosphorus', 'potassium', 
                      'sulfur', 'magnesium', 'calcium', 'moisture', 'temperature',
                      'clay', 'silt', 'sand']
    
    X = df[feature_columns]
    y_score = df['fertility_score']
    y_level = df['fertility_level']
    
    # Split data
    X_train, X_test, y_score_train, y_score_test, y_level_train, y_level_test = train_test_split(
        X, y_score, y_level, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train fertility score regression model
    print("\nTraining fertility score regression model...")
    score_model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    score_model.fit(X_train_scaled, y_score_train)
    
    # Evaluate score model
    score_pred = score_model.predict(X_test_scaled)
    score_mse = mean_squared_error(y_score_test, score_pred)
    score_rmse = np.sqrt(score_mse)
    print(f"Fertility score RMSE: {score_rmse:.2f}")
    
    # Train fertility level classification model
    print("Training fertility level classification model...")
    level_model = GradientBoostingClassifier(
        n_estimators=150,
        learning_rate=0.1,
        max_depth=8,
        random_state=42
    )
    level_model.fit(X_train_scaled, y_level_train)
    
    # Evaluate level model
    level_pred = level_model.predict(X_test_scaled)
    level_accuracy = accuracy_score(y_level_test, level_pred)
    print(f"Fertility level accuracy: {level_accuracy:.3f}")
    
    # Create encoders for categorical variables
    fertilizer_encoder = LabelEncoder()
    fertilizer_encoder.fit(df['fertilizer_recommendation'])
    
    # Save models and preprocessing objects
    print("\nSaving models and preprocessing objects...")
    joblib.dump(score_model, 'models/fertility_score_model.pkl')
    joblib.dump(level_model, 'models/fertility_level_model.pkl')
    joblib.dump(scaler, 'models/feature_scaler.pkl')
    joblib.dump(fertilizer_encoder, 'models/fertilizer_encoder.pkl')
    
    # Save feature names and sample data for reference
    joblib.dump(feature_columns, 'models/feature_names.pkl')
    df.sample(100).to_csv('models/sample_data.csv', index=False)
    
    # Display feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': score_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature importance for fertility score prediction:")
    print(feature_importance)
    
    return score_model, level_model, scaler, fertilizer_encoder, feature_columns

def test_model_predictions():
    """Test the trained models with various input scenarios"""
    print("\nTesting model predictions with sample inputs...")
    
    # Load trained models
    score_model = joblib.load('models/fertility_score_model.pkl')
    level_model = joblib.load('models/fertility_level_model.pkl')
    scaler = joblib.load('models/feature_scaler.pkl')
    feature_columns = joblib.load('models/feature_names.pkl')
    
    # Test scenarios
    test_scenarios = [
        {
            'name': 'High Quality Soil',
            'ph': 6.8, 'organic_matter': 4.5, 'nitrogen': 180, 'phosphorus': 45,
            'potassium': 220, 'sulfur': 25, 'magnesium': 80, 'calcium': 800,
            'moisture': 28, 'temperature': 23, 'clay': 30, 'silt': 40, 'sand': 30
        },
        {
            'name': 'Poor Quality Soil',
            'ph': 5.2, 'organic_matter': 1.2, 'nitrogen': 40, 'phosphorus': 12,
            'potassium': 60, 'sulfur': 8, 'magnesium': 20, 'calcium': 150,
            'moisture': 15, 'temperature': 18, 'clay': 15, 'silt': 25, 'sand': 60
        },
        {
            'name': 'Alkaline Soil',
            'ph': 8.2, 'organic_matter': 2.8, 'nitrogen': 120, 'phosphorus': 30,
            'potassium': 150, 'sulfur': 15, 'magnesium': 60, 'calcium': 1200,
            'moisture': 22, 'temperature': 25, 'clay': 25, 'silt': 35, 'sand': 40
        },
        {
            'name': 'Acidic Soil',
            'ph': 5.8, 'organic_matter': 3.2, 'nitrogen': 90, 'phosphorus': 20,
            'potassium': 100, 'sulfur': 12, 'magnesium': 35, 'calcium': 300,
            'moisture': 30, 'temperature': 20, 'clay': 35, 'silt': 30, 'sand': 35
        },
        {
            'name': 'Sandy Soil',
            'ph': 6.5, 'organic_matter': 1.8, 'nitrogen': 60, 'phosphorus': 15,
            'potassium': 80, 'sulfur': 10, 'magnesium': 25, 'calcium': 200,
            'moisture': 18, 'temperature': 26, 'clay': 10, 'silt': 15, 'sand': 75
        }
    ]
    
    for scenario in test_scenarios:
        name = scenario.pop('name')
        
        # Prepare input data
        input_data = pd.DataFrame([scenario], columns=feature_columns)
        input_scaled = scaler.transform(input_data)
        
        # Make predictions
        fertility_score = score_model.predict(input_scaled)[0]
        fertility_level = level_model.predict(input_scaled)[0]
        
        print(f"\n{name}:")
        print(f"  Fertility Score: {fertility_score:.1f}")
        print(f"  Fertility Level: {fertility_level}")
        print(f"  Input - pH: {scenario['ph']}, N: {scenario['nitrogen']}, P: {scenario['phosphorus']}, K: {scenario['potassium']}")

if __name__ == "__main__":
    # Create models directory if it doesn't exist
    import os
    os.makedirs('models', exist_ok=True)
    
    # Train enhanced models
    train_enhanced_models()
    
    # Test predictions
    test_model_predictions()
    
    print("\n✅ Enhanced model training completed successfully!")
    print("Models saved in 'models/' directory")
    print("\nModel files created:")
    print("- fertility_score_model.pkl")
    print("- fertility_level_model.pkl") 
    print("- feature_scaler.pkl")
    print("- fertilizer_encoder.pkl")
    print("- feature_names.pkl")
    print("- sample_data.csv")
