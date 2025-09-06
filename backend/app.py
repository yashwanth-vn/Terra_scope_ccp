from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from database import db
from dotenv import load_dotenv
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
cors = CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Import routes after app initialization
from routes.auth import auth_bp
from routes.soil import soil_bp
from routes.predictions import predictions_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(soil_bp, url_prefix='/api/soil')
app.register_blueprint(predictions_bp, url_prefix='/api/predictions')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Terra Scope API!"})

@app.route('/api/test')
def test_api():
    return jsonify({"status": "API is working", "routes": [str(rule) for rule in app.url_map.iter_rules()]})

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
