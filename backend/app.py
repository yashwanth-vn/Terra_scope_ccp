from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from database import db
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///terra_scope.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')

# Initialize extensions
db.init_app(app)
cors = CORS(app, origins=['http://localhost:3000', 'http://localhost:3001', 'http://127.0.0.1:3000', 'http://127.0.0.1:3001', 'http://[::1]:3000', 'http://[::1]:3001'], 
           supports_credentials=True, 
           allow_headers=['Content-Type', 'Authorization'])
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Import routes after app initialization
from routes.auth import auth_bp
from routes.soil import soil_bp
from routes.predictions import predictions_bp
from routes.chat import chat_bp
from routes.history import history_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(soil_bp, url_prefix='/api/soil')
app.register_blueprint(predictions_bp, url_prefix='/api/predictions')
app.register_blueprint(chat_bp, url_prefix='/api/chat')
app.register_blueprint(history_bp, url_prefix='/api/history')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Terra Scope API!"})

@app.route('/api/test')
def test_api():
    return jsonify({"status": "API is working", "routes": [str(rule) for rule in app.url_map.iter_rules()]})

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Backend is running",
        "cors_enabled": True,
        "timestamp": str(datetime.now() if 'datetime' in globals() else 'N/A')
    })

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Import all models to ensure they're created
    from models.user import User
    from models.soil_data import SoilData
    from models.chat import ChatSession, ChatMessage
    from models.history import AnalysisHistory, UserActivity
    
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
