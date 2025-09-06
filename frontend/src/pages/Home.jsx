import React from 'react'
import { Link } from 'react-router-dom'

function Home() {
  return (
    <div>
      {/* Hero Section */}
      <div className="home-hero">
        <h1>Terra Scope 🌱</h1>
        <p>Predict and monitor soil fertility with AI-powered insights</p>
        <div>
          <Link to="/signup" className="btn btn-primary">Get Started</Link>
          <Link to="/login" className="btn btn-secondary" style={{marginLeft: '1rem'}}>Login</Link>
        </div>
      </div>

      {/* Features Section */}
      <div className="features">
        <div className="feature-card">
          <h3>🧪 Soil Testing</h3>
          <p>Input your soil test results including pH, NPK values, and organic carbon content.</p>
        </div>
        
        <div className="feature-card">
          <h3>🤖 AI Predictions</h3>
          <p>Advanced machine learning models analyze your soil data to predict fertility levels.</p>
        </div>
        
        <div className="feature-card">
          <h3>🌦️ Weather Integration</h3>
          <p>Real-time weather data helps provide more accurate soil condition assessments.</p>
        </div>
        
        <div className="feature-card">
          <h3>💡 Smart Recommendations</h3>
          <p>Get personalized fertilizer recommendations and crop suggestions based on your soil.</p>
        </div>
        
        <div className="feature-card">
          <h3>📊 Soil History</h3>
          <p>Track your soil fertility over time with detailed history and trends.</p>
        </div>
        
        <div className="feature-card">
          <h3>🌾 Crop Planning</h3>
          <p>Discover which crops are most suitable for your soil conditions and season.</p>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="container">
        <div className="card">
          <h2 className="text-center">How Terra Scope Works</h2>
          <div style={{textAlign: 'left', maxWidth: '600px', margin: '0 auto'}}>
            <h4>1. Test Your Soil</h4>
            <p>Use a soil testing kit to measure pH, Nitrogen (N), Phosphorus (P), Potassium (K), and Organic Carbon levels.</p>
            
            <h4>2. Input Your Data</h4>
            <p>Enter your soil test results into our simple form along with your location and crop information.</p>
            
            <h4>3. Get AI Analysis</h4>
            <p>Our advanced ML model analyzes your data considering weather patterns and seasonal factors.</p>
            
            <h4>4. Receive Recommendations</h4>
            <p>Get specific fertilizer dosage recommendations and suitable crop suggestions for your soil.</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
