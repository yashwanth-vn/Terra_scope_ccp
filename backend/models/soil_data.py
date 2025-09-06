from database import db
from datetime import datetime
import json

class SoilData(db.Model):
    __tablename__ = 'soil_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Soil parameters
    ph = db.Column(db.Float, nullable=False)
    nitrogen = db.Column(db.Float, nullable=False)  # N in mg/kg
    phosphorus = db.Column(db.Float, nullable=False)  # P in mg/kg
    potassium = db.Column(db.Float, nullable=False)  # K in mg/kg
    organic_carbon = db.Column(db.Float, nullable=False)  # OC in %
    moisture = db.Column(db.Float, nullable=True, default=0)  # Moisture in %
    
    # Additional information
    crop_type = db.Column(db.String(50), nullable=True)
    season = db.Column(db.String(20), nullable=True)
    
    # ML prediction results
    fertility_level = db.Column(db.String(20), nullable=True)  # Low, Medium, High
    fertility_score = db.Column(db.Float, nullable=True)  # 0-100 score
    recommendations = db.Column(db.Text, nullable=True)  # JSON string
    crop_suggestions = db.Column(db.Text, nullable=True)  # JSON string
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SoilData {self.id} - User {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'ph': self.ph,
            'nitrogen': self.nitrogen,
            'phosphorus': self.phosphorus,
            'potassium': self.potassium,
            'organicCarbon': self.organic_carbon,
            'moisture': self.moisture,
            'cropType': self.crop_type,
            'season': self.season,
            'fertilityLevel': self.fertility_level,
            'fertilityScore': self.fertility_score,
            'recommendations': json.loads(self.recommendations) if self.recommendations else None,
            'cropSuggestions': json.loads(self.crop_suggestions) if self.crop_suggestions else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_npk_ratio(self):
        """Calculate NPK ratio for analysis"""
        total = self.nitrogen + self.phosphorus + self.potassium
        if total == 0:
            return {'N': 0, 'P': 0, 'K': 0}
        return {
            'N': round((self.nitrogen / total) * 100, 2),
            'P': round((self.phosphorus / total) * 100, 2),
            'K': round((self.potassium / total) * 100, 2)
        }
    
    def is_ph_optimal(self):
        """Check if pH is in optimal range (6.0-7.5)"""
        return 6.0 <= self.ph <= 7.5
    
    def get_fertility_category(self):
        """Get fertility category based on multiple parameters"""
        if self.fertility_level:
            return self.fertility_level
        
        # Simple rule-based classification if ML prediction is not available
        score = 0
        
        # pH scoring (6.0-7.5 is optimal)
        if 6.0 <= self.ph <= 7.5:
            score += 25
        elif 5.5 <= self.ph <= 8.0:
            score += 15
        else:
            score += 5
        
        # Nutrient scoring (simplified thresholds)
        if self.nitrogen > 200: score += 20
        elif self.nitrogen > 100: score += 15
        elif self.nitrogen > 50: score += 10
        else: score += 5
        
        if self.phosphorus > 25: score += 20
        elif self.phosphorus > 15: score += 15
        elif self.phosphorus > 10: score += 10
        else: score += 5
        
        if self.potassium > 150: score += 20
        elif self.potassium > 100: score += 15
        elif self.potassium > 50: score += 10
        else: score += 5
        
        # Organic carbon scoring
        if self.organic_carbon > 1.5: score += 15
        elif self.organic_carbon > 1.0: score += 10
        elif self.organic_carbon > 0.5: score += 5
        
        if score >= 70:
            return 'High'
        elif score >= 50:
            return 'Medium'
        else:
            return 'Low'
