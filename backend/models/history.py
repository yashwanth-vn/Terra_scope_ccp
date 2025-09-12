from database import db
from datetime import datetime
import json

class AnalysisHistory(db.Model):
    __tablename__ = 'analysis_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    soil_data_id = db.Column(db.Integer, db.ForeignKey('soil_data.id'), nullable=True)
    
    # History details
    analysis_type = db.Column(db.String(50), nullable=False)  # 'soil_test', 'prediction', 'recommendation'
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Analysis results snapshot
    results_data = db.Column(db.Text, nullable=True)  # JSON string of results
    
    # Location and context
    location = db.Column(db.String(100), nullable=True)
    crop_type = db.Column(db.String(50), nullable=True)
    season = db.Column(db.String(20), nullable=True)
    
    # Status
    status = db.Column(db.String(20), default='completed')  # completed, pending, failed
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AnalysisHistory {self.id} - User {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'soilDataId': self.soil_data_id,
            'analysisType': self.analysis_type,
            'title': self.title,
            'description': self.description,
            'resultsData': json.loads(self.results_data) if self.results_data else None,
            'location': self.location,
            'cropType': self.crop_type,
            'season': self.season,
            'status': self.status,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
    
    def set_results_data(self, data):
        """Set results data as JSON string"""
        self.results_data = json.dumps(data) if data else None
    
    def get_results_data(self):
        """Get results data as Python object"""
        return json.loads(self.results_data) if self.results_data else None

class UserActivity(db.Model):
    __tablename__ = 'user_activity'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Activity details
    activity_type = db.Column(db.String(50), nullable=False)  # 'login', 'soil_analysis', 'chat', 'profile_update'
    activity_description = db.Column(db.String(200), nullable=True)
    
    # Additional data
    meta_data = db.Column(db.Text, nullable=True)  # JSON string for additional data
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserActivity {self.id} - User {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'activityType': self.activity_type,
            'activityDescription': self.activity_description,
            'metadata': json.loads(self.meta_data) if self.meta_data else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
    
    def set_metadata(self, data):
        """Set metadata as JSON string"""
        self.meta_data = json.dumps(data) if data else None
    
    def get_metadata(self):
        """Get metadata as Python object"""
        return json.loads(self.meta_data) if self.meta_data else None
