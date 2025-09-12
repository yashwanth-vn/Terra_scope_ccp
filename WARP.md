# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Commands

### Development Setup
```bash
# Backend setup (from backend directory)
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py

# Frontend setup (from frontend directory)
npm install
npm run dev
```

### Database Management
```bash
# Initialize database and create tables
python manage_db.py

# Key database utilities
python manage_db.py show_db_info     # View database status and table counts
python manage_db.py show_users       # List all users
python manage_db.py show_soil_data   # List all soil analysis records
python manage_db.py create_sample_user    # Create demo user (demo@terrascope.com / demo123)
python manage_db.py backup_database  # Backup database with timestamp

# Quick database queries
python quick_query.py  # Interactive database query tool
```

### Testing & Development
```bash
# Run integration tests
python test_integration.py          # Basic API tests
python test_full_integration.py     # Full workflow tests

# Create test user programmatically
python create_test_user.py

# Train ML model with new data
python train_model.py              # Basic model training
python train_enhanced_model.py     # Enhanced stacking ensemble model
```

### Frontend Commands
```bash
# From frontend directory
npm run dev      # Start development server (localhost:3000)
npm run build    # Build for production
npm run lint     # ESLint code checking
npm run preview  # Preview production build
```

## Architecture Overview

### Full-Stack Structure
Terra Scope is an AI-powered soil fertility analysis platform with a **React frontend** and **Flask backend**, designed to help farmers make data-driven agricultural decisions.

### Backend Architecture (Flask)
- **Main Application**: `app.py` - Flask app with CORS, JWT auth, and blueprint registration
- **Database**: SQLAlchemy ORM with SQLite (dev) / PostgreSQL (production)
- **Authentication**: JWT tokens with Flask-JWT-Extended + bcrypt password hashing
- **API Structure**: Organized into blueprints (`auth`, `soil`, `predictions`, `chat`, `history`)

### Machine Learning Pipeline
The core ML system uses a **Stacking Ensemble** approach:
- **Base Learners**: Random Forest + XGBoost classifiers
- **Meta-Learner**: Logistic Regression for final predictions
- **Training Data**: Synthetic agricultural data with realistic parameter distributions
- **Features**: Soil pH, N-P-K values, organic carbon, moisture, weather integration
- **Prediction Service**: `services/enhanced_predictor.py` handles real-time fertility analysis

### Database Schema
- **Users**: Authentication, profile, location data
- **SoilData**: Lab test results, ML predictions, fertilizer recommendations
- **ChatSession/ChatMessage**: AI chatbot conversation history
- **AnalysisHistory**: Track prediction accuracy and user activity patterns

### Frontend Architecture (React + Vite)
- **State Management**: React Context API (`AuthContext`)
- **Routing**: React Router DOM with protected routes
- **HTTP Client**: Axios with JWT token interceptors
- **Styling**: Plain CSS with agricultural theme (green gradients, glassmorphism effects)
- **Key Components**: Dashboard, SoilInput, Profile, Chatbot, History

### External Integrations
- **Weather API**: OpenWeatherMap for temperature/rainfall data affecting soil analysis
- **Location Services**: Browser geolocation + OpenWeather geocoding
- **ML Models**: scikit-learn and XGBoost for ensemble predictions

## Development Patterns

### API Route Structure
```
/api/auth/*     - User authentication (signup, login, profile)
/api/soil/*     - Soil data CRUD operations
/api/predictions/* - ML fertility analysis and recommendations
/api/chat/*     - AI chatbot interactions
/api/history/*  - User activity and analysis history
```

### Database Patterns
- All models inherit from SQLAlchemy with automatic timestamps
- Foreign key relationships with cascade delete
- JSON storage for complex data (recommendations, chat history)
- Built-in helper methods for data analysis (NPK ratios, pH optimization)

### Frontend Data Flow
1. User inputs soil test data via `SoilInput.jsx`
2. Data sent to `/api/soil/input` and `/api/predictions/fertility`
3. ML model processes data with weather integration
4. Results displayed on `Dashboard.jsx` with recommendations
5. Historical data available via `History.jsx`

### ML Model Integration
- Models are loaded once at app startup in `services/enhanced_predictor.py`
- Real-time prediction via `/api/predictions/fertility`
- Automatic model retraining capabilities with new user data
- Fertilizer recommendations based on nutrient deficiencies
- Crop suggestions considering soil conditions and regional factors

## Key Files to Understand

### Backend Core
- `app.py` - Main Flask application and configuration
- `models/user.py`, `models/soil_data.py` - Database schema
- `ml_models/enhanced_fertility_model.py` - Stacking ensemble ML implementation
- `services/enhanced_predictor.py` - Prediction service layer
- `routes/predictions.py` - ML integration endpoints

### Frontend Core  
- `src/App.jsx` - Main app component with routing
- `src/contexts/AuthContext.jsx` - Authentication state management
- `src/pages/Dashboard.jsx` - Main user interface after analysis
- `src/pages/SoilInput.jsx` - Data collection form

### Development Tools
- `manage_db.py` - Comprehensive database management utilities
- `quick_query.py` - Interactive database queries
- `test_integration.py` - API testing suite

## Environment Variables
Required in `backend/.env`:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=jwt-secret-key  
OPENWEATHER_API_KEY=your-api-key
DATABASE_URL=sqlite:///terra_scope.db
```

## Development Notes
- Backend runs on localhost:5000, frontend on localhost:3000
- CORS configured for both localhost and 127.0.0.1 addresses
- JWT tokens required for all protected endpoints
- Database automatically created on first run
- ML models generate synthetic training data if no real data exists
- Weather integration requires OpenWeatherMap API key
- All passwords are bcrypt hashed
