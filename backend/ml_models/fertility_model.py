import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import xgboost as xgb
import joblib
import os
from datetime import datetime

class FertilityPredictor:
    def __init__(self, model_path=None):
        self.model_path = model_path or 'ml_models/trained_fertility_model.pkl'
        self.scaler_path = 'ml_models/scaler.pkl'
        self.model = None
        self.scaler = None
        self.feature_names = [
            'ph', 'nitrogen', 'phosphorus', 'potassium', 
            'organic_carbon', 'moisture', 'temperature', 'rainfall'
        ]
        
        # Load pre-trained model if it exists
        self.load_model()
        
        # If no model exists, create and train a basic one with synthetic data
        if self.model is None:
            self.train_initial_model()
    
    def create_stacking_model(self):
        """Create the Stacking Ensemble Model with Random Forest + XGBoost base learners"""
        
        # Base learners
        rf_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        
        xgb_classifier = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            eval_metric='mlogloss'
        )
        
        # Meta-learner
        meta_learner = LogisticRegression(
            random_state=42,
            max_iter=1000
        )
        
        # Create stacking classifier
        stacking_model = StackingClassifier(
            estimators=[
                ('rf', rf_classifier),
                ('xgb', xgb_classifier)
            ],
            final_estimator=meta_learner,
            cv=3,
            stack_method='predict_proba',
            n_jobs=-1
        )
        
        return stacking_model
    
    def generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic soil data for initial training"""
        np.random.seed(42)
        
        # Generate realistic soil parameter ranges
        data = []
        labels = []
        
        for _ in range(n_samples):
            # Generate soil parameters with realistic ranges
            ph = np.random.normal(6.5, 1.0)  # pH typically 4.5-8.5
            ph = np.clip(ph, 4.0, 9.0)
            
            nitrogen = np.random.exponential(80)  # N in mg/kg, typically 20-300
            nitrogen = np.clip(nitrogen, 10, 400)
            
            phosphorus = np.random.exponential(20)  # P in mg/kg, typically 5-60
            phosphorus = np.clip(phosphorus, 2, 100)
            
            potassium = np.random.exponential(100)  # K in mg/kg, typically 30-300
            potassium = np.clip(potassium, 20, 500)
            
            organic_carbon = np.random.exponential(1.2)  # OC in %, typically 0.5-3.0
            organic_carbon = np.clip(organic_carbon, 0.2, 4.0)
            
            moisture = np.random.uniform(10, 40)  # Moisture in %
            temperature = np.random.normal(25, 8)  # Temperature in Celsius
            rainfall = np.random.exponential(50)  # Rainfall in mm
            
            # Create fertility labels based on rules
            score = 0
            
            # pH contribution (optimal 6.0-7.5)
            if 6.0 <= ph <= 7.5:
                score += 0.3
            elif 5.5 <= ph <= 8.0:
                score += 0.2
            else:
                score += 0.1
            
            # Nutrient contributions
            if nitrogen > 150: score += 0.25
            elif nitrogen > 80: score += 0.2
            elif nitrogen > 40: score += 0.1
            
            if phosphorus > 20: score += 0.2
            elif phosphorus > 10: score += 0.15
            elif phosphorus > 5: score += 0.1
            
            if potassium > 120: score += 0.2
            elif potassium > 80: score += 0.15
            elif potassium > 40: score += 0.1
            
            # Organic carbon contribution
            if organic_carbon > 1.5: score += 0.15
            elif organic_carbon > 1.0: score += 0.1
            elif organic_carbon > 0.7: score += 0.05
            
            # Classify based on score
            if score >= 0.7:
                fertility = 2  # High
            elif score >= 0.45:
                fertility = 1  # Medium
            else:
                fertility = 0  # Low
            
            data.append([ph, nitrogen, phosphorus, potassium, 
                        organic_carbon, moisture, temperature, rainfall])
            labels.append(fertility)
        
        return np.array(data), np.array(labels)
    
    def train_initial_model(self):
        """Train the model with synthetic data"""
        print("Training initial fertility prediction model...")
        
        # Generate synthetic training data
        X, y = self.generate_synthetic_data(1000)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Create and train the stacking model
        self.model = self.create_stacking_model()
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate the model
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        print(f"Model training completed!")
        print(f"Training accuracy: {train_score:.3f}")
        print(f"Testing accuracy: {test_score:.3f}")
        
        # Save the model
        self.save_model()
    
    def save_model(self):
        """Save the trained model and scaler"""
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            print(f"Model saved to {self.model_path}")
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def load_model(self):
        """Load pre-trained model and scaler"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                print("Pre-trained model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
            self.scaler = None
    
    def preprocess_input(self, soil_params, weather_data=None):
        """Preprocess input parameters for prediction"""
        # Extract soil parameters
        features = [
            soil_params.get('ph', 6.5),
            soil_params.get('nitrogen', 100),
            soil_params.get('phosphorus', 20),
            soil_params.get('potassium', 100),
            soil_params.get('organic_carbon', 1.0),
            soil_params.get('moisture', 25),
        ]
        
        # Add weather parameters
        if weather_data:
            features.extend([
                weather_data.get('temperature', 25),
                weather_data.get('rainfall', 50)
            ])
        else:
            # Use default weather values
            features.extend([25, 50])
        
        return np.array(features).reshape(1, -1)
    
    def predict_fertility(self, soil_params, weather_data=None):
        """Predict soil fertility level"""
        try:
            # Preprocess input
            features = self.preprocess_input(soil_params, weather_data)
            
            # Scale features
            if self.scaler:
                features_scaled = self.scaler.transform(features)
            else:
                features_scaled = features
            
            # Make prediction
            prediction = self.model.predict(features_scaled)[0]
            probabilities = self.model.predict_proba(features_scaled)[0]
            
            # Convert prediction to label
            labels = ['Low', 'Medium', 'High']
            predicted_label = labels[prediction]
            
            # Calculate confidence score
            confidence = max(probabilities) * 100
            
            # Calculate fertility score (0-100)
            fertility_score = (prediction * 50) + (confidence * 0.5)
            fertility_score = min(fertility_score, 100)
            
            return {
                'level': predicted_label,
                'score': round(fertility_score, 1),
                'confidence': round(confidence, 1),
                'probabilities': {
                    'Low': round(probabilities[0] * 100, 1),
                    'Medium': round(probabilities[1] * 100, 1),
                    'High': round(probabilities[2] * 100, 1)
                }
            }
            
        except Exception as e:
            print(f"Error in fertility prediction: {e}")
            # Fallback to simple rule-based prediction
            return self.simple_fertility_prediction(soil_params)
    
    def simple_fertility_prediction(self, soil_params):
        """Simple rule-based fertility prediction as fallback"""
        score = 0
        
        ph = soil_params.get('ph', 6.5)
        nitrogen = soil_params.get('nitrogen', 100)
        phosphorus = soil_params.get('phosphorus', 20)
        potassium = soil_params.get('potassium', 100)
        organic_carbon = soil_params.get('organic_carbon', 1.0)
        
        # pH contribution
        if 6.0 <= ph <= 7.5:
            score += 25
        elif 5.5 <= ph <= 8.0:
            score += 15
        else:
            score += 5
        
        # Nutrient contributions
        if nitrogen > 150: score += 25
        elif nitrogen > 80: score += 20
        elif nitrogen > 40: score += 10
        else: score += 5
        
        if phosphorus > 20: score += 20
        elif phosphorus > 10: score += 15
        elif phosphorus > 5: score += 10
        else: score += 5
        
        if potassium > 120: score += 20
        elif potassium > 80: score += 15
        elif potassium > 40: score += 10
        else: score += 5
        
        # Organic carbon contribution
        if organic_carbon > 1.5: score += 10
        elif organic_carbon > 1.0: score += 5
        
        # Classify
        if score >= 70:
            level = 'High'
        elif score >= 50:
            level = 'Medium'
        else:
            level = 'Low'
        
        return {
            'level': level,
            'score': score,
            'confidence': 75.0,
            'probabilities': {'Low': 20.0, 'Medium': 30.0, 'High': 50.0}
        }
    
    def retrain_model(self, new_data, new_labels):
        """Retrain the model with new data"""
        try:
            # Combine with synthetic data for better performance
            synthetic_X, synthetic_y = self.generate_synthetic_data(500)
            
            # Combine datasets
            X_combined = np.vstack([synthetic_X, new_data])
            y_combined = np.hstack([synthetic_y, new_labels])
            
            # Retrain model
            X_train, X_test, y_train, y_test = train_test_split(
                X_combined, y_combined, test_size=0.2, random_state=42
            )
            
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            self.model = self.create_stacking_model()
            self.model.fit(X_train_scaled, y_train)
            
            # Save updated model
            self.save_model()
            
            print("Model retrained successfully!")
            return True
            
        except Exception as e:
            print(f"Error retraining model: {e}")
            return False
