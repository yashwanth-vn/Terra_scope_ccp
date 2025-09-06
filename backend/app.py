from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///terra_scope.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

# Initialize extensions
db = SQLAlchemy(app)
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
    return jsonify({"message": "Terra Scope API is running!"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
