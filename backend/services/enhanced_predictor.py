#!/usr/bin/env python3
"""
Enhanced Terra Scope Prediction Service
Uses the newly trained ML models for realistic soil fertility predictions
"""

import joblib
import pandas as pd
import numpy as np
import os
import random
from typing import Dict, List, Any

class EnhancedFertilityPredictor:
    def __init__(self):
        """Initialize the enhanced predictor with trained models"""
        self.models_dir = 'models'
        self.models_loaded = False
        self.load_models()
    
    def load_models(self):
        """Load all trained models and preprocessing objects"""
        try:
            if not os.path.exists(self.models_dir):
                raise Exception(f"Models directory '{self.models_dir}' not found")
            
            # Load models
            self.score_model = joblib.load(os.path.join(self.models_dir, 'fertility_score_model.pkl'))
            self.level_model = joblib.load(os.path.join(self.models_dir, 'fertility_level_model.pkl'))
            self.scaler = joblib.load(os.path.join(self.models_dir, 'feature_scaler.pkl'))
            self.fertilizer_encoder = joblib.load(os.path.join(self.models_dir, 'fertilizer_encoder.pkl'))
            self.feature_columns = joblib.load(os.path.join(self.models_dir, 'feature_names.pkl'))
            
            self.models_loaded = True
            print("✅ Enhanced models loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            self.models_loaded = False
    
    def prepare_input_data(self, soil_data: Dict[str, float]) -> pd.DataFrame:
        """Prepare input data for prediction"""
        # Map input data to model features
        feature_mapping = {
            'ph': soil_data.get('ph', 6.5),
            'organic_matter': soil_data.get('organic_matter', 2.5),
            'nitrogen': soil_data.get('nitrogen', 100),
            'phosphorus': soil_data.get('phosphorus', 30),
            'potassium': soil_data.get('potassium', 150),
            'sulfur': soil_data.get('sulfur', 20),
            'magnesium': soil_data.get('magnesium', 50),
            'calcium': soil_data.get('calcium', 500),
            'moisture': soil_data.get('moisture', 25),
            'temperature': soil_data.get('temperature', 22),
            'clay': soil_data.get('clay', 25),
            'silt': soil_data.get('silt', 35),
            'sand': soil_data.get('sand', 40)
        }
        
        # Ensure texture percentages sum to 100
        texture_total = feature_mapping['clay'] + feature_mapping['silt'] + feature_mapping['sand']
        if texture_total != 100:
            feature_mapping['clay'] = (feature_mapping['clay'] / texture_total) * 100
            feature_mapping['silt'] = (feature_mapping['silt'] / texture_total) * 100
            feature_mapping['sand'] = (feature_mapping['sand'] / texture_total) * 100
        
        # Create DataFrame with correct feature order
        input_data = pd.DataFrame([feature_mapping], columns=self.feature_columns)
        return input_data
    
    def predict_fertility(self, soil_data: Dict[str, float]) -> Dict[str, Any]:
        """Predict soil fertility based on input parameters"""
        if not self.models_loaded:
            return self.fallback_prediction(soil_data)
        
        try:
            # Prepare input data
            input_data = self.prepare_input_data(soil_data)
            input_scaled = self.scaler.transform(input_data)
            
            # Make predictions
            fertility_score = self.score_model.predict(input_scaled)[0]
            fertility_level = self.level_model.predict(input_scaled)[0]
            
            # Round fertility score to 1 decimal place
            fertility_score = round(float(fertility_score), 1)
            
            # Generate fertilizer recommendations
            fertilizer_recommendations = self.get_fertilizer_recommendations(soil_data, fertility_score)
            
            # Generate crop recommendations
            crop_recommendations = self.get_crop_recommendations(soil_data, fertility_score)
            
            return {
                'fertility_score': fertility_score,
                'fertility_level': fertility_level,
                'fertilizer_recommendations': fertilizer_recommendations,
                'crop_recommendations': crop_recommendations,
                'analysis': self.generate_analysis(soil_data, fertility_score, fertility_level)
            }
            
        except Exception as e:
            print(f"❌ Error in prediction: {e}")
            return self.fallback_prediction(soil_data)
    
    def get_fertilizer_recommendations(self, soil_data: Dict[str, float], fertility_score: float) -> List[str]:
        """Generate fertilizer recommendations based on soil analysis"""
        recommendations = []
        
        nitrogen = soil_data.get('nitrogen', 100)
        phosphorus = soil_data.get('phosphorus', 30)
        potassium = soil_data.get('potassium', 150)
        ph = soil_data.get('ph', 6.5)
        magnesium = soil_data.get('magnesium', 50)
        calcium = soil_data.get('calcium', 500)
        sulfur = soil_data.get('sulfur', 20)
        
        # Nitrogen recommendations
        if nitrogen < 80:
            if ph < 6.5:
                recommendations.append("Calcium Nitrate (improves pH)")
            else:
                recommendations.append("Urea (high nitrogen content)")
        elif nitrogen < 120:
            recommendations.append("Ammonium Sulfate (balanced N+S)")
        
        # Phosphorus recommendations
        if phosphorus < 25:
            recommendations.append("DAP (Diammonium Phosphate)")
        elif phosphorus < 40:
            recommendations.append("Superphosphate")
        
        # Potassium recommendations
        if potassium < 120:
            recommendations.append("Potassium Chloride (Muriate of Potash)")
        elif potassium < 180:
            recommendations.append("Potassium Sulfate")
        
        # Secondary nutrients
        if magnesium < 50:
            recommendations.append("Epsom Salt (Magnesium Sulfate)")
        
        if calcium < 400:
            if ph < 6.0:
                recommendations.append("Lime (Calcium Carbonate)")
            else:
                recommendations.append("Gypsum (Calcium Sulfate)")
        
        if sulfur < 20:
            recommendations.append("Elemental Sulfur")
        
        # pH adjustments
        if ph < 5.5:
            recommendations.append("Agricultural Lime (pH adjustment)")
        elif ph > 8.0:
            recommendations.append("Sulfur (pH reduction)")
        
        # If no specific deficiencies or if high fertility
        if not recommendations or fertility_score > 75:
            if fertility_score > 80:
                recommendations = ["Balanced NPK (10-10-10)", "Compost", "Organic Fertilizer"]
            else:
                recommendations.append("NPK Complex (20-20-20)")
        
        # Limit recommendations to top 3-4
        return recommendations[:4] if len(recommendations) > 4 else recommendations
    
    def get_crop_recommendations(self, soil_data: Dict[str, float], fertility_score: float) -> List[str]:
        """Generate crop recommendations based on soil conditions"""
        crops = []
        
        ph = soil_data.get('ph', 6.5)
        moisture = soil_data.get('moisture', 25)
        temperature = soil_data.get('temperature', 22)
        clay = soil_data.get('clay', 25)
        sand = soil_data.get('sand', 40)
        nitrogen = soil_data.get('nitrogen', 100)
        
        # pH-based recommendations
        if ph < 6.0:  # Acidic soil lovers
            crops.extend(["Blueberries", "Potatoes", "Sweet Potatoes", "Azaleas"])
        elif ph > 7.5:  # Alkaline soil tolerant
            crops.extend(["Asparagus", "Cabbage", "Spinach", "Sugar Beets"])
        else:  # Neutral pH crops
            crops.extend(["Tomatoes", "Corn", "Wheat", "Soybeans", "Carrots"])
        
        # Temperature-based recommendations
        if temperature < 18:
            crops.extend(["Lettuce", "Peas", "Spinach", "Kale"])
        elif temperature > 28:
            crops.extend(["Okra", "Eggplant", "Peppers", "Melons"])
        else:
            crops.extend(["Beans", "Squash", "Cucumbers", "Broccoli"])
        
        # Soil texture based
        if sand > 60:  # Sandy soil
            crops.extend(["Carrots", "Radishes", "Potatoes", "Herbs"])
        elif clay > 40:  # Clay soil
            crops.extend(["Rice", "Lettuce", "Cabbage", "Chard"])
        else:  # Loamy soil
            crops.extend(["Tomatoes", "Peppers", "Beans", "Squash"])
        
        # Fertility-based recommendations
        if fertility_score > 75:
            crops.extend(["Leafy Greens", "Brassicas", "Heavy Feeders"])
        elif fertility_score < 45:
            crops.extend(["Legumes", "Root Vegetables", "Light Feeders"])
        
        # Moisture-based recommendations
        if moisture > 35:
            crops.extend(["Rice", "Celery", "Watercress"])
        elif moisture < 20:
            crops.extend(["Cacti", "Drought-resistant crops", "Mediterranean herbs"])
        
        # Remove duplicates and select diverse recommendations
        unique_crops = list(set(crops))
        random.shuffle(unique_crops)
        return unique_crops[:6]  # Return up to 6 diverse recommendations
    
    def generate_analysis(self, soil_data: Dict[str, float], fertility_score: float, fertility_level: str) -> str:
        """Generate detailed soil analysis text"""
        ph = soil_data.get('ph', 6.5)
        nitrogen = soil_data.get('nitrogen', 100)
        phosphorus = soil_data.get('phosphorus', 30)
        potassium = soil_data.get('potassium', 150)
        organic_matter = soil_data.get('organic_matter', 2.5)
        moisture = soil_data.get('moisture', 25)
        
        analysis_parts = []
        
        # Fertility level analysis
        if fertility_score >= 80:
            analysis_parts.append("Your soil shows excellent fertility with optimal nutrient levels.")
        elif fertility_score >= 65:
            analysis_parts.append("Your soil has good fertility with most nutrients in acceptable ranges.")
        elif fertility_score >= 50:
            analysis_parts.append("Your soil shows fair fertility but could benefit from targeted improvements.")
        elif fertility_score >= 35:
            analysis_parts.append("Your soil has poor fertility and requires significant nutrient supplementation.")
        else:
            analysis_parts.append("Your soil shows very poor fertility and needs comprehensive soil improvement.")
        
        # pH analysis
        if ph < 5.5:
            analysis_parts.append(f"pH ({ph}) is acidic - consider lime application to improve nutrient availability.")
        elif ph > 8.0:
            analysis_parts.append(f"pH ({ph}) is alkaline - sulfur application may help lower pH.")
        else:
            analysis_parts.append(f"pH ({ph}) is in an optimal range for most crops.")
        
        # Nutrient analysis
        nutrient_status = []
        if nitrogen < 80:
            nutrient_status.append("nitrogen is low")
        if phosphorus < 25:
            nutrient_status.append("phosphorus is deficient")
        if potassium < 120:
            nutrient_status.append("potassium needs supplementation")
        
        if nutrient_status:
            analysis_parts.append(f"Key concerns: {', '.join(nutrient_status)}.")
        else:
            analysis_parts.append("Major nutrients are at adequate levels.")
        
        # Organic matter analysis
        if organic_matter < 2.0:
            analysis_parts.append("Low organic matter - consider compost or organic amendments.")
        elif organic_matter > 4.0:
            analysis_parts.append("Excellent organic matter content supports soil health.")
        
        # Moisture analysis
        if moisture < 20:
            analysis_parts.append("Soil moisture is low - improve irrigation or water retention.")
        elif moisture > 35:
            analysis_parts.append("High moisture content - ensure proper drainage to prevent root problems.")
        
        return " ".join(analysis_parts)
    
    def fallback_prediction(self, soil_data: Dict[str, float]) -> Dict[str, Any]:
        """Fallback prediction when models aren't available"""
        print("⚠️ Using fallback prediction method")
        
        # Simple rule-based prediction
        ph = soil_data.get('ph', 6.5)
        nitrogen = soil_data.get('nitrogen', 100)
        phosphorus = soil_data.get('phosphorus', 30)
        potassium = soil_data.get('potassium', 150)
        
        # Calculate basic fertility score
        ph_score = max(0, 100 - abs(ph - 6.5) * 20)
        n_score = min(100, nitrogen * 0.8)
        p_score = min(100, phosphorus * 2)
        k_score = min(100, potassium * 0.6)
        
        fertility_score = (ph_score + n_score + p_score + k_score) / 4
        fertility_score = round(fertility_score + random.uniform(-5, 5), 1)
        
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
        
        return {
            'fertility_score': fertility_score,
            'fertility_level': fertility_level,
            'fertilizer_recommendations': ["NPK Complex", "Compost"],
            'crop_recommendations': ["Tomatoes", "Lettuce", "Beans", "Carrots"],
            'analysis': f"Basic analysis indicates {fertility_level.lower()} soil fertility with a score of {fertility_score}."
        }

# Initialize the global predictor instance
enhanced_predictor = EnhancedFertilityPredictor()
