from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.soil_data import SoilData
from services.enhanced_predictor import enhanced_predictor
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
            'organic_matter': float(data.get('organicCarbon', 2.5)),  # Map to organic_matter
            'moisture': float(data.get('moisture', 25)),
            'temperature': float(data.get('temperature', 22)),
            'sulfur': float(data.get('sulfur', 20)),
            'magnesium': float(data.get('magnesium', 50)),
            'calcium': float(data.get('calcium', 500)),
            'clay': float(data.get('clay', 25)),
            'silt': float(data.get('silt', 35)),
            'sand': float(data.get('sand', 40))
        }
        
        # Get weather data if location is available
        weather_data = {}
        if user.location:
            weather_data = get_weather_data(user.location)
        
        # Make prediction using enhanced model
        prediction_result = enhanced_predictor.predict_fertility(soil_params)
        
        # Format fertility prediction
        fertility_prediction = {
            'level': prediction_result['fertility_level'],
            'score': prediction_result['fertility_score'],
            'analysis': prediction_result['analysis']
        }
        
        fertilizer_recs = prediction_result['fertilizer_recommendations']
        crop_suggestions = prediction_result['crop_recommendations']
        
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
            'crop_recommendations': crop_suggestions,
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
            'organic_matter': latest_soil.organic_carbon,
            'moisture': latest_soil.moisture,
            'temperature': 22.0,  # Default temperature
            'sulfur': 20.0,      # Default sulfur
            'magnesium': 50.0,   # Default magnesium
            'calcium': 500.0,    # Default calcium
            'clay': 25.0,        # Default clay
            'silt': 35.0,        # Default silt
            'sand': 40.0         # Default sand
        }
        
        # Get weather data
        weather_data = {}
        if user.location:
            weather_data = get_weather_data(user.location)
        
        # Make prediction using enhanced model
        prediction_result = enhanced_predictor.predict_fertility(soil_params)
        
        # Format fertility prediction
        fertility_prediction = {
            'level': prediction_result['fertility_level'],
            'score': prediction_result['fertility_score'],
            'analysis': prediction_result['analysis']
        }
        
        fertilizer_recs = prediction_result['fertilizer_recommendations']
        crop_suggestions = prediction_result['crop_recommendations']
        
        # Update soil record with predictions
        latest_soil.fertility_level = fertility_prediction['level']
        latest_soil.fertility_score = fertility_prediction['score']
        latest_soil.recommendations = json.dumps(fertilizer_recs)
        latest_soil.crop_suggestions = json.dumps(crop_suggestions)
        db.session.commit()
        
        return jsonify({
            'soilData': {
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
            'crop_recommendations': crop_suggestions,
            'weather_impact': weather_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
