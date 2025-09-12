from database import db
from datetime import datetime
import json

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=True)  # Auto-generated title
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with messages
    messages = db.relationship('ChatMessage', backref='session', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ChatSession {self.id} - User {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'title': self.title,
            'isActive': self.is_active,
            'messageCount': len(self.messages),
            'lastMessage': self.messages[-1].to_dict() if self.messages else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Message content
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    message_type = db.Column(db.String(20), default='text')  # text, soil_analysis, recommendation
    
    # Context data for intelligent responses
    context_data = db.Column(db.Text, nullable=True)  # JSON string for additional context
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatMessage {self.id} - Session {self.session_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'sessionId': self.session_id,
            'userId': self.user_id,
            'message': self.message,
            'response': self.response,
            'messageType': self.message_type,
            'contextData': json.loads(self.context_data) if self.context_data else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
    
    def set_context_data(self, data):
        """Set context data as JSON string"""
        self.context_data = json.dumps(data) if data else None
    
    def get_context_data(self):
        """Get context data as Python object"""
        return json.loads(self.context_data) if self.context_data else None
