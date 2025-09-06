# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Common Development Commands

### Backend (Flask)
```powershell
# Navigate to backend directory
cd backend

# Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask development server
python app.py

# Run single tests
python -m pytest tests/test_specific.py::test_function_name
```

### Frontend (React + Vite)
```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run linter
npm run lint

# Preview production build
npm run preview
```

### Full Stack Development
```powershell
# Start both servers (run in separate terminals)
# Terminal 1 - Backend
cd backend && python app.py

# Terminal 2 - Frontend  
cd frontend && npm run dev
```

## Architecture Overview

### System Design
Terra Scope is a full-stack web application with clear separation between frontend and backend:

- **Frontend**: React 18 with Vite, uses React Router for client-side routing and Axios for API communication
- **Backend**: Flask REST API with SQLAlchemy ORM, JWT authentication, and ML-powered predictions
- **Database**: SQLite (development) with models for User and SoilData
- **ML Pipeline**: Stacking Ensemble (Random Forest + XGBoost + Logistic Regression) for soil fertility prediction

### Key Architectural Patterns

**Backend Structure (Flask)**:
- Blueprint-based route organization (`routes/` directory)
- Model-based database layer (`models/` directory)  
- Utility modules for external integrations (`utils/` directory)
- ML models encapsulated in dedicated classes (`ml_models/` directory)
- Centralized application factory pattern in `app.py`

**Frontend Structure (React)**:
- Page-based routing with components in `pages/`
- Service layer for API communication in `services/`
- Component-based architecture with reusable UI components

**Data Flow**:
1. User inputs soil parameters via React frontend
2. JWT-authenticated API calls to Flask backend
3. Weather data integration via OpenWeatherMap API
4. ML model processes soil + weather data
5. Fertilizer recommendations generated via rule-based system
6. Results stored in SQLAlchemy models and returned to frontend

### Critical Integration Points

**Authentication Flow**:
- JWT tokens managed by Flask-JWT-Extended
- Frontend stores tokens and includes in API requests
- User model contains profile info and location for weather integration

**ML Prediction Pipeline**:
- `FertilityPredictor` class handles model lifecycle (training, loading, prediction)
- Stacking ensemble combines Random Forest + XGBoost predictions via Logistic Regression meta-learner  
- Weather data from OpenWeatherMap API integrated as additional features
- Fallback to rule-based prediction if ML model fails

**External API Integration**:
- Weather service in `utils/weather.py` handles OpenWeatherMap API calls
- Recommendation engine in `utils/recommendations.py` generates fertilizer and crop suggestions
- Error handling with fallback to default values when APIs unavailable

## Environment Configuration

### Required Environment Variables
Create `.env` file in `backend/` directory:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this-in-production
JWT_SECRET_KEY=jwt-secret-change-this-in-production
OPENWEATHER_API_KEY=your-openweather-api-key-here
DATABASE_URL=sqlite:///terra_scope.db
```

### API Keys Setup
- OpenWeatherMap API: Sign up at https://openweathermap.org/api for free API key
- Required for weather integration that enhances ML predictions
- Application provides fallback weather data if API key missing

## Development Notes

### ML Model Behavior
- Model auto-trains with synthetic data on first run if no pre-trained model exists
- Trained models saved as `.pkl` files in `ml_models/` (ignored by git)
- Model supports incremental learning with new real user data
- Feature scaling handled internally by StandardScaler

### Database Schema
- `users` table: Authentication and profile information
- `soil_data` table: Soil parameters, ML predictions, and recommendations
- Foreign key relationship between users and their soil data
- JSON fields store complex recommendation data

### Frontend-Backend Communication  
- Vite proxy configured to route `/api/*` requests to Flask backend (port 5000)
- Frontend runs on port 3000, backend on port 5000
- CORS enabled in Flask for cross-origin requests during development

### Testing Strategy
- Backend: Flask application context required for database operations
- ML models: Test with synthetic data generation functions
- API endpoints: Test with JWT authentication headers
- Frontend: Component testing with mocked API responses

## Code Style and Patterns

### Backend Conventions
- Blueprint organization by feature (`auth`, `soil`, `predictions`)
- SQLAlchemy model methods for business logic (`to_dict()`, `get_npk_ratio()`)
- Error handling with appropriate HTTP status codes
- Environment variable configuration with fallbacks

### Frontend Conventions
- Functional React components with hooks
- Page components handle routing and state management  
- Service layer abstracts API communication
- Plain CSS styling (no UI frameworks per project requirements)

### ML Code Patterns
- Class-based model encapsulation with clear lifecycle methods
- Synthetic data generation for initial training
- Graceful degradation to rule-based predictions
- Feature preprocessing and scaling handled internally

## Common Issues and Solutions

### Backend Issues
- **Model loading fails**: Check if `.pkl` files exist, model will auto-train if missing
- **Weather API errors**: Application falls back to default weather data
- **Database errors**: Ensure Flask application context for SQLAlchemy operations
- **JWT errors**: Verify token generation and validation in authentication routes

### Frontend Issues  
- **API connection errors**: Verify Vite proxy configuration for `/api` routes
- **CORS errors**: Ensure Flask-CORS is properly configured
- **Build errors**: Check for proper import paths and component structure
- **Routing issues**: Verify React Router setup and component imports
