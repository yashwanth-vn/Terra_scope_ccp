from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models.history import AnalysisHistory, UserActivity
from models.soil_data import SoilData
from models.chat import ChatSession
from datetime import datetime, timedelta
from sqlalchemy import desc, func

history_bp = Blueprint('history', __name__)

@history_bp.route('/analysis', methods=['GET'])
@jwt_required()
def get_analysis_history():
    """Get user's soil analysis history"""
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        analysis_type = request.args.get('type')  # Filter by analysis type
        
        query = AnalysisHistory.query.filter_by(user_id=current_user_id)
        
        if analysis_type:
            query = query.filter_by(analysis_type=analysis_type)
        
        history_items = query.order_by(desc(AnalysisHistory.created_at))\
                           .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'history': [item.to_dict() for item in history_items.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': history_items.total,
                'pages': history_items.pages,
                'has_next': history_items.has_next,
                'has_prev': history_items.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving analysis history: {str(e)}'
        }), 500

@history_bp.route('/analysis', methods=['POST'])
@jwt_required()
def add_analysis_history():
    """Add new analysis history entry"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('analysis_type') or not data.get('title'):
            return jsonify({
                'success': False,
                'message': 'Analysis type and title are required'
            }), 400
        
        # Create new analysis history entry
        history_entry = AnalysisHistory(
            user_id=current_user_id,
            soil_data_id=data.get('soil_data_id'),
            analysis_type=data['analysis_type'],
            title=data['title'],
            description=data.get('description'),
            location=data.get('location'),
            crop_type=data.get('crop_type'),
            season=data.get('season'),
            status=data.get('status', 'completed')
        )
        
        if data.get('results_data'):
            history_entry.set_results_data(data['results_data'])
        
        db.session.add(history_entry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Analysis history added successfully',
            'history_entry': history_entry.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error adding analysis history: {str(e)}'
        }), 500

@history_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics and recent activity"""
    try:
        current_user_id = get_jwt_identity()
        
        # Calculate date ranges
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Get counts for different periods
        total_analyses = SoilData.query.filter_by(user_id=current_user_id).count()
        recent_analyses = SoilData.query.filter_by(user_id=current_user_id)\
                                       .filter(SoilData.created_at >= week_ago).count()
        
        total_chats = ChatSession.query.filter_by(user_id=current_user_id).count()
        recent_chats = ChatSession.query.filter_by(user_id=current_user_id)\
                                      .filter(ChatSession.created_at >= week_ago).count()
        
        # Get recent soil analyses
        recent_soil_data = SoilData.query.filter_by(user_id=current_user_id)\
                                        .order_by(desc(SoilData.created_at))\
                                        .limit(5).all()
        
        # Get recent chat sessions
        recent_chat_sessions = ChatSession.query.filter_by(user_id=current_user_id)\
                                               .order_by(desc(ChatSession.updated_at))\
                                               .limit(5).all()
        
        # Get analysis history
        recent_history = AnalysisHistory.query.filter_by(user_id=current_user_id)\
                                            .order_by(desc(AnalysisHistory.created_at))\
                                            .limit(5).all()
        
        # Calculate fertility distribution
        fertility_distribution = db.session.query(
            SoilData.fertility_level,
            func.count(SoilData.fertility_level)
        ).filter_by(user_id=current_user_id)\
         .group_by(SoilData.fertility_level)\
         .all()
        
        fertility_stats = {level: count for level, count in fertility_distribution}
        
        return jsonify({
            'success': True,
            'stats': {
                'total_analyses': total_analyses,
                'recent_analyses': recent_analyses,
                'total_chats': total_chats,
                'recent_chats': recent_chats,
                'fertility_distribution': fertility_stats
            },
            'recent_activity': {
                'soil_analyses': [item.to_dict() for item in recent_soil_data],
                'chat_sessions': [session.to_dict() for session in recent_chat_sessions],
                'analysis_history': [entry.to_dict() for entry in recent_history]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving dashboard stats: {str(e)}'
        }), 500

@history_bp.route('/activity', methods=['GET'])
@jwt_required()
def get_user_activity():
    """Get user activity log"""
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        activity_type = request.args.get('type')  # Filter by activity type
        
        query = UserActivity.query.filter_by(user_id=current_user_id)
        
        if activity_type:
            query = query.filter_by(activity_type=activity_type)
        
        activities = query.order_by(desc(UserActivity.created_at))\
                         .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'activities': [activity.to_dict() for activity in activities.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': activities.total,
                'pages': activities.pages,
                'has_next': activities.has_next,
                'has_prev': activities.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving user activity: {str(e)}'
        }), 500

@history_bp.route('/activity', methods=['POST'])
@jwt_required()
def log_user_activity():
    """Log user activity"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('activity_type'):
            return jsonify({
                'success': False,
                'message': 'Activity type is required'
            }), 400
        
        # Create new activity log entry
        activity = UserActivity(
            user_id=current_user_id,
            activity_type=data['activity_type'],
            activity_description=data.get('activity_description')
        )
        
        if data.get('metadata'):
            activity.set_metadata(data['metadata'])
        
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Activity logged successfully',
            'activity': activity.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error logging activity: {str(e)}'
        }), 500

@history_bp.route('/export', methods=['POST'])
@jwt_required()
def export_history():
    """Export user's history data"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        export_type = data.get('type', 'all')  # 'all', 'soil_analyses', 'chat_history'
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        
        export_data = {}
        
        # Build date filter
        date_filter = {}
        if date_from:
            date_filter['from'] = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
        if date_to:
            date_filter['to'] = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
        
        if export_type in ['all', 'soil_analyses']:
            # Get soil analyses
            query = SoilData.query.filter_by(user_id=current_user_id)
            
            if 'from' in date_filter:
                query = query.filter(SoilData.created_at >= date_filter['from'])
            if 'to' in date_filter:
                query = query.filter(SoilData.created_at <= date_filter['to'])
            
            soil_analyses = query.order_by(desc(SoilData.created_at)).all()
            export_data['soil_analyses'] = [analysis.to_dict() for analysis in soil_analyses]
        
        if export_type in ['all', 'chat_history']:
            # Get chat sessions and messages
            query = ChatSession.query.filter_by(user_id=current_user_id)
            
            if 'from' in date_filter:
                query = query.filter(ChatSession.created_at >= date_filter['from'])
            if 'to' in date_filter:
                query = query.filter(ChatSession.created_at <= date_filter['to'])
            
            chat_sessions = query.order_by(desc(ChatSession.created_at)).all()
            export_data['chat_history'] = [session.to_dict() for session in chat_sessions]
        
        if export_type in ['all', 'analysis_history']:
            # Get analysis history
            query = AnalysisHistory.query.filter_by(user_id=current_user_id)
            
            if 'from' in date_filter:
                query = query.filter(AnalysisHistory.created_at >= date_filter['from'])
            if 'to' in date_filter:
                query = query.filter(AnalysisHistory.created_at <= date_filter['to'])
            
            analysis_history = query.order_by(desc(AnalysisHistory.created_at)).all()
            export_data['analysis_history'] = [entry.to_dict() for entry in analysis_history]
        
        return jsonify({
            'success': True,
            'export_data': export_data,
            'exported_at': datetime.utcnow().isoformat(),
            'export_type': export_type
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error exporting history: {str(e)}'
        }), 500
