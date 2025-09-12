from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models.chat import ChatSession, ChatMessage
from models.user import User
from services.improved_chatbot import ImprovedAgriChatbot
from datetime import datetime

chat_bp = Blueprint('chat', __name__)
chatbot = ImprovedAgriChatbot()

@chat_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_chat_sessions():
    """Get all chat sessions for the current user"""
    try:
        current_user_id = get_jwt_identity()
        
        sessions = ChatSession.query.filter_by(user_id=current_user_id)\
                                  .order_by(ChatSession.updated_at.desc()).all()
        
        return jsonify({
            'success': True,
            'sessions': [session.to_dict() for session in sessions]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving chat sessions: {str(e)}'
        }), 500

@chat_bp.route('/sessions', methods=['POST'])
@jwt_required()
def create_chat_session():
    """Create a new chat session"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Create new chat session
        session = ChatSession(
            user_id=current_user_id,
            title=data.get('title', f'Chat - {datetime.now().strftime("%b %d, %Y")}'),
            is_active=True
        )
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Chat session created successfully',
            'session': session.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating chat session: {str(e)}'
        }), 500

@chat_bp.route('/sessions/<int:session_id>/messages', methods=['GET'])
@jwt_required()
def get_chat_messages(session_id):
    """Get all messages for a specific chat session"""
    try:
        current_user_id = get_jwt_identity()
        
        # Verify session belongs to current user
        session = ChatSession.query.filter_by(id=session_id, user_id=current_user_id).first()
        if not session:
            return jsonify({
                'success': False,
                'message': 'Chat session not found'
            }), 404
        
        messages = ChatMessage.query.filter_by(session_id=session_id)\
                                   .order_by(ChatMessage.created_at.asc()).all()
        
        return jsonify({
            'success': True,
            'messages': [message.to_dict() for message in messages],
            'session': session.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving messages: {str(e)}'
        }), 500

@chat_bp.route('/sessions/<int:session_id>/messages', methods=['POST'])
@jwt_required()
def send_message(session_id):
    """Send a message and get chatbot response"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('message'):
            return jsonify({
                'success': False,
                'message': 'Message content is required'
            }), 400
        
        # Verify session belongs to current user
        session = ChatSession.query.filter_by(id=session_id, user_id=current_user_id).first()
        if not session:
            return jsonify({
                'success': False,
                'message': 'Chat session not found'
            }), 404
        
        user_message = data.get('message')
        message_type = data.get('message_type', 'text')
        context_data = data.get('context_data')
        
        # Generate chatbot response
        bot_response_data = chatbot.generate_response(
            message=user_message,
            user_id=current_user_id,
            context_data=context_data
        )
        
        # Update session title if it's the first message
        if not session.messages:
            session.title = chatbot.generate_session_title(user_message)
        
        # Create new message record
        message = ChatMessage(
            session_id=session_id,
            user_id=current_user_id,
            message=user_message,
            response=bot_response_data['response'],
            message_type=message_type
        )
        
        if context_data:
            message.set_context_data(context_data)
        
        # Update session timestamp
        session.updated_at = datetime.utcnow()
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Message sent successfully',
            'chat_message': message.to_dict(),
            'bot_response': bot_response_data['response'],
            'suggestions': bot_response_data['suggestions'],
            'session': session.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error sending message: {str(e)}'
        }), 500

@chat_bp.route('/sessions/<int:session_id>', methods=['PUT'])
@jwt_required()
def update_chat_session(session_id):
    """Update chat session (e.g., title, active status)"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        session = ChatSession.query.filter_by(id=session_id, user_id=current_user_id).first()
        if not session:
            return jsonify({
                'success': False,
                'message': 'Chat session not found'
            }), 404
        
        # Update session properties
        if 'title' in data:
            session.title = data['title']
        if 'is_active' in data:
            session.is_active = data['is_active']
        
        session.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Chat session updated successfully',
            'session': session.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating chat session: {str(e)}'
        }), 500

@chat_bp.route('/sessions/<int:session_id>', methods=['DELETE'])
@jwt_required()
def delete_chat_session(session_id):
    """Delete a chat session and all its messages"""
    try:
        current_user_id = get_jwt_identity()
        
        session = ChatSession.query.filter_by(id=session_id, user_id=current_user_id).first()
        if not session:
            return jsonify({
                'success': False,
                'message': 'Chat session not found'
            }), 404
        
        # Delete session (messages will be deleted due to cascade)
        db.session.delete(session)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Chat session deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting chat session: {str(e)}'
        }), 500

@chat_bp.route('/quick-ask', methods=['POST'])
@jwt_required()
def quick_ask():
    """Quick ask without creating a session (for simple queries)"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('message'):
            return jsonify({
                'success': False,
                'message': 'Message content is required'
            }), 400
        
        user_message = data.get('message')
        context_data = data.get('context_data')
        
        # Generate chatbot response
        bot_response_data = chatbot.generate_response(
            message=user_message,
            user_id=current_user_id,
            context_data=context_data
        )
        
        return jsonify({
            'success': True,
            'response': bot_response_data['response'],
            'suggestions': bot_response_data['suggestions'],
            'message_type': bot_response_data['message_type']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing quick ask: {str(e)}'
        }), 500
