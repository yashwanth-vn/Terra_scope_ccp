from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.soil_data import SoilData
from database import db
from datetime import datetime

soil_bp = Blueprint('soil', __name__)

@soil_bp.route('/input', methods=['POST'])
@jwt_required()
def add_soil_data():
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Validate required soil parameters
        required_fields = ['ph', 'nitrogen', 'phosphorus', 'potassium', 'organicCarbon']
        for field in required_fields:
            if data.get(field) is None:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new soil data entry
        soil_data = SoilData(
            user_id=user.id,
            ph=float(data['ph']),
            nitrogen=float(data['nitrogen']),
            phosphorus=float(data['phosphorus']),
            potassium=float(data['potassium']),
            organic_carbon=float(data['organicCarbon']),
            moisture=float(data.get('moisture', 0)),
            crop_type=data.get('cropType', ''),
            season=data.get('season', ''),
            created_at=datetime.utcnow()
        )
        
        db.session.add(soil_data)
        db.session.commit()
        
        return jsonify({
            'message': 'Soil data saved successfully',
            'soil_data': {
                'id': soil_data.id,
                'ph': soil_data.ph,
                'nitrogen': soil_data.nitrogen,
                'phosphorus': soil_data.phosphorus,
                'potassium': soil_data.potassium,
                'organicCarbon': soil_data.organic_carbon,
                'moisture': soil_data.moisture,
                'cropType': soil_data.crop_type,
                'season': soil_data.season,
                'createdAt': soil_data.created_at.isoformat()
            }
        }), 201
        
    except ValueError as e:
        return jsonify({'error': 'Invalid numeric values provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@soil_bp.route('/history', methods=['GET'])
@jwt_required()
def get_soil_history():
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get soil data history for the user
        soil_records = SoilData.query.filter_by(user_id=user.id).order_by(SoilData.created_at.desc()).limit(10).all()
        
        history = []
        for record in soil_records:
            history.append({
                'id': record.id,
                'ph': record.ph,
                'nitrogen': record.nitrogen,
                'phosphorus': record.phosphorus,
                'potassium': record.potassium,
                'organicCarbon': record.organic_carbon,
                'moisture': record.moisture,
                'cropType': record.crop_type,
                'season': record.season,
                'createdAt': record.created_at.isoformat()
            })
        
        return jsonify({'history': history}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@soil_bp.route('/latest', methods=['GET'])
@jwt_required()
def get_latest_soil_data():
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get the latest soil data for the user
        latest_record = SoilData.query.filter_by(user_id=user.id).order_by(SoilData.created_at.desc()).first()
        
        if not latest_record:
            return jsonify({'error': 'No soil data found'}), 404
        
        return jsonify({
            'soil_data': {
                'id': latest_record.id,
                'ph': latest_record.ph,
                'nitrogen': latest_record.nitrogen,
                'phosphorus': latest_record.phosphorus,
                'potassium': latest_record.potassium,
                'organicCarbon': latest_record.organic_carbon,
                'moisture': latest_record.moisture,
                'cropType': latest_record.crop_type,
                'season': latest_record.season,
                'createdAt': latest_record.created_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
