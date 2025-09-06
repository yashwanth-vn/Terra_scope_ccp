from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.soil_data import SoilData
from ml_models.fertility_model import FertilityPredictor
from utils.weather import get_weather_data
from utils.recommendations import get_fertilizer_recommendations, get_crop_suggestions
from database import db
import json

predictions_bp = Blueprint('predictions', __name__)

@predictions_bp.route('/fertility', methods=['POST'])
@jwt_required()
def predict_fertility():
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Get soil parameters
        soil_params = {
            'ph': float(data['ph']),
            'nitrogen': float(data['nitrogen']),
            'phosphorus': float(data['phosphorus']),
            'potassium': float(data['potassium']),
            'organic_carbon': float(data['organicCarbon']),
            'moisture': float(data.get('moisture', 20))  # Default moisture
        }
        
        # Get weather data if location is available
        weather_data = {}
        if user.location:
            weather_data = get_weather_data(user.location)
        
        # Create fertility predictor instance
        predictor = FertilityPredictor()
        
        # Make prediction
        fertility_prediction = predictor.predict_fertility(soil_params, weather_data)
        
        # Get recommendations
        fertilizer_recs = get_fertilizer_recommendations(soil_params, fertility_prediction)
        crop_suggestions = get_crop_suggestions(soil_params, data.get('season', 'spring'))
        
        # Store prediction result (optional)
        latest_soil = SoilData.query.filter_by(user_id=user.id).order_by(SoilData.created_at.desc()).first()
        if latest_soil:
            latest_soil.fertility_level = fertility_prediction['level']
            latest_soil.fertility_score = fertility_prediction['score']
            latest_soil.recommendations = json.dumps(fertilizer_recs)
            latest_soil.crop_suggestions = json.dumps(crop_suggestions)
            db.session.commit()
        
        return jsonify({
            'fertility': fertility_prediction,
            'fertilizer_recommendations': fertilizer_recs,
            'crop_suggestions': crop_suggestions,
            'weather_impact': weather_data
        }), 200
        
    except ValueError as e:
        return jsonify({'error': 'Invalid input values'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@predictions_bp.route('/analyze-latest', methods=['GET'])
@jwt_required()
def analyze_latest_soil():
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get latest soil data
        latest_soil = SoilData.query.filter_by(user_id=user.id).order_by(SoilData.created_at.desc()).first()
        
        if not latest_soil:
            return jsonify({'error': 'No soil data found. Please add soil data first.'}), 404
        
        # Prepare soil parameters
        soil_params = {
            'ph': latest_soil.ph,
            'nitrogen': latest_soil.nitrogen,
            'phosphorus': latest_soil.phosphorus,
            'potassium': latest_soil.potassium,
            'organic_carbon': latest_soil.organic_carbon,
            'moisture': latest_soil.moisture
        }
        
        # Get weather data
        weather_data = {}
        if user.location:
            weather_data = get_weather_data(user.location)
        
        # Create fertility predictor instance
        predictor = FertilityPredictor()
        
        # Make prediction
        fertility_prediction = predictor.predict_fertility(soil_params, weather_data)
        
        # Get recommendations
        fertilizer_recs = get_fertilizer_recommendations(soil_params, fertility_prediction)
        crop_suggestions = get_crop_suggestions(soil_params, latest_soil.season or 'spring')
        
        # Update soil record with predictions
        latest_soil.fertility_level = fertility_prediction['level']
        latest_soil.fertility_score = fertility_prediction['score']
        latest_soil.recommendations = json.dumps(fertilizer_recs)
        latest_soil.crop_suggestions = json.dumps(crop_suggestions)
        db.session.commit()
        
        return jsonify({
            'soil_data': {
                'id': latest_soil.id,
                'ph': latest_soil.ph,
                'nitrogen': latest_soil.nitrogen,
                'phosphorus': latest_soil.phosphorus,
                'potassium': latest_soil.potassium,
                'organicCarbon': latest_soil.organic_carbon,
                'moisture': latest_soil.moisture,
                'cropType': latest_soil.crop_type,
                'season': latest_soil.season,
                'createdAt': latest_soil.created_at.isoformat()
            },
            'fertility': fertility_prediction,
            'fertilizer_recommendations': fertilizer_recs,
            'crop_suggestions': crop_suggestions,
            'weather_impact': weather_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
