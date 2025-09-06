# Terra Scope 🌱

A simple web application that helps farmers predict and monitor soil fertility using AI-powered insights.

## Overview

Terra Scope is designed to be a straightforward tool for farmers to:
- Input soil testing data (pH, N-P-K, Organic Carbon)
- Get AI-powered fertility predictions
- Receive fertilizer recommendations
- Find suitable crops for their soil conditions
- Track soil health over time

## Features

### 🔹 User Authentication
- **Signup**: Collects first name, last name, email, password, and optionally location/contact
- **Login**: Simple email and password authentication
- **Logout**: Secure session management

### 🔹 Soil Data Input
- Manual entry of soil parameters from testing kits:
  - pH level
  - Nitrogen (N) in mg/kg
  - Phosphorus (P) in mg/kg  
  - Potassium (K) in mg/kg
  - Organic Carbon percentage
  - Moisture content (optional)

### 🔹 Dynamic Fertility Analysis
- **Weather Integration**: Auto-detects location for temperature & rainfall data
- **Crop Cycle Info**: Considers current crop and season
- **AI/ML Model**: Stacking Ensemble with Random Forest + XGBoost base learners and Logistic Regression meta-learner

### 🔹 Smart Recommendations
- Soil fertility level prediction (Low/Medium/High)
- Specific fertilizer dosage suggestions (kg/acre or per hectare)
- Suitable crop recommendations based on soil health

## Technology Stack

### Frontend (React + Vite)
- **Framework**: React 18 with Vite
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Styling**: Plain CSS (simple, student-project style)

### Backend (Flask)
- **Framework**: Flask with SQLAlchemy
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: JWT tokens with Flask-JWT-Extended
- **ML Libraries**: scikit-learn, XGBoost, pandas, numpy

### External APIs
- **Weather Data**: OpenWeatherMap API
- **Location Services**: Browser geolocation + OpenWeather geocoding

## Project Structure

```
terra-scope/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service functions
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   ├── package.json
│   └── vite.config.js
├── backend/                  # Flask backend
│   ├── routes/              # API route handlers
│   ├── models/              # Database models
│   ├── ml_models/           # Machine learning components
│   ├── utils/               # Utility functions
│   ├── app.py               # Main Flask application
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
├── docs/                    # Documentation
└── README.md
```

## Installation & Setup

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- pip (Python package manager)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux  
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env` file and update values:
   ```bash
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-change-this-in-production
   JWT_SECRET_KEY=jwt-secret-change-this-in-production
   OPENWEATHER_API_KEY=your-openweather-api-key-here
   DATABASE_URL=sqlite:///terra_scope.db
   ```

5. **Run the Flask server**:
   ```bash
   python app.py
   ```

   Backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:3000`

### OpenWeather API Setup

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Add it to the backend `.env` file as `OPENWEATHER_API_KEY`

## Usage Guide

### 1. Create Account
- Go to `/signup` and fill in your details
- Email will be your username
- Location is optional but recommended for weather integration

### 2. Input Soil Data
- Use a soil testing kit to measure pH, N-P-K values
- Go to `/soil-input` and enter your measurements
- Specify crop type and season if known

### 3. View Analysis
- Dashboard shows fertility level, recommendations, and suitable crops
- Weather data is automatically integrated if location is provided
- Fertilizer suggestions include dosage and application timing

### 4. Track Progress
- Soil history shows trends over time
- Profile page displays account statistics

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile

### Soil Data
- `POST /api/soil/input` - Add new soil data
- `GET /api/soil/history` - Get soil data history
- `GET /api/soil/latest` - Get latest soil data

### Predictions  
- `POST /api/predictions/fertility` - Get fertility prediction
- `GET /api/predictions/analyze-latest` - Analyze latest soil data

## Machine Learning Model

The core AI model uses a **Stacking Ensemble** approach:

### Base Learners
1. **Random Forest Classifier**
   - Handles non-linear relationships
   - Robust to outliers
   - Feature importance analysis

2. **XGBoost Classifier** 
   - Gradient boosting for high accuracy
   - Handles missing values well
   - Optimized performance

### Meta-Learner
- **Logistic Regression**
   - Combines base learner predictions
   - Provides interpretable final output
   - Probability estimates for confidence scoring

### Training Data
- Uses synthetic agricultural data for initial training
- Incorporates weather patterns and seasonal factors
- Continuously improves with real user data

## Development Notes

This application is designed to look like a **simple 2nd-year computer science student project**:

- ✅ Basic, clean UI without fancy animations
- ✅ Simple form-based interactions  
- ✅ Straightforward navigation
- ✅ Plain CSS styling (no UI frameworks like Bootstrap/MaterialUI)
- ✅ Direct, functional approach to problem-solving
- ✅ Clear, readable code structure

## Future Enhancements

- [ ] Mobile-responsive design
- [ ] Soil test history charts
- [ ] Export reports functionality
- [ ] Multi-language support
- [ ] Advanced crop planning calendar
- [ ] Integration with IoT soil sensors
- [ ] Community features for farmer collaboration

## Contributing

This is a learning project. Contributions are welcome for:
- Bug fixes
- Feature improvements
- Documentation updates
- Test coverage
- Code optimization

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions or issues:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed description

---

**Terra Scope** - Helping farmers grow better with AI-powered soil insights! 🌾
