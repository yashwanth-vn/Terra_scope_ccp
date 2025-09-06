import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const { isAuthenticated, token } = useAuth()
  const navigate = useNavigate()

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/login')
    }
  }, [isAuthenticated, navigate])

  // Mock data for demonstration
  const mockData = {
    soilData: {
      ph: 6.8,
      nitrogen: 120,
      phosphorus: 25,
      potassium: 150,
      organicCarbon: 1.8,
      moisture: 28,
      cropType: 'Wheat',
      season: 'Spring',
      createdAt: new Date().toISOString()
    },
    fertility: {
      level: 'High',
      score: 78.5,
      confidence: 85.2
    },
    fertilizer_recommendations: {
      primary_fertilizers: [
        {
          name: 'NPK Complex (15-15-15)',
          purpose: 'Maintenance fertilization',
          application_rate: '15-20 kg per hectare',
          priority: 'medium'
        }
      ],
      warnings: [],
      application_timing: [
        'Apply fertilizers during soil preparation',
        'Split nitrogen application for better uptake'
      ]
    },
    crop_suggestions: {
      highly_suitable: [
        { name: 'Wheat', type: 'cereal', suitability_score: 92.5, season_match: true },
        { name: 'Barley', type: 'cereal', suitability_score: 88.0, season_match: true }
      ],
      moderately_suitable: [
        { name: 'Corn', type: 'cereal', suitability_score: 75.0, season_match: true }
      ]
    },
    weather_impact: {
      temperature: 22,
      humidity: 65,
      description: 'partly cloudy',
      location: 'Unknown'
    }
  }

  useEffect(() => {
    // Simulate API call
    const fetchData = async () => {
      try {
        // TODO: Replace with real API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        setData(mockData)
      } catch (err) {
        setError('Failed to load dashboard data')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="container">
        <div className="card text-center">
          <h2>Loading your soil analysis...</h2>
          <p>Please wait while we fetch your latest data.</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container">
        <div className="card text-center">
          <h2>⚠️ Error Loading Data</h2>
          <p>{error}</p>
          <Link to="/soil-input" className="btn btn-primary">Add Soil Data</Link>
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="container">
        <div className="card text-center">
          <h2>📊 Welcome to Your Dashboard</h2>
          <p>No soil data found. Start by entering your soil test results.</p>
          <Link to="/soil-input" className="btn btn-primary">Add Soil Data</Link>
        </div>
      </div>
    )
  }

  const getFertilityColor = (level) => {
    switch(level.toLowerCase()) {
      case 'high': return '#28a745'
      case 'medium': return '#ffc107'
      case 'low': return '#dc3545'
      default: return '#6c757d'
    }
  }

  return (
    <div className="container">
      <div className="card">
        <h1 className="text-center">🌱 Soil Fertility Dashboard</h1>
        <p className="text-center" style={{color: '#666'}}>
          Latest analysis from {new Date(data.soilData.createdAt).toLocaleDateString()}
        </p>
      </div>

      <div className="results-grid" style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px', margin: '20px 0'}}>
        {/* Fertility Status */}
        <div className="result-card" style={{padding: '20px', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)'}}>
          <h3 style={{color: '#2c5530', marginBottom: '15px'}}>🎯 Fertility Level</h3>
          <div style={{fontSize: '2rem', fontWeight: 'bold', color: getFertilityColor(data.fertility.level), marginBottom: '10px'}}>
            {data.fertility.level}
          </div>
          <p><strong>Score:</strong> {data.fertility.score}/100</p>
          <p><strong>Confidence:</strong> {data.fertility.confidence}%</p>
        </div>

        {/* Soil Parameters */}
        <div className="result-card" style={{padding: '20px', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)'}}>
          <h3 style={{color: '#2c5530', marginBottom: '15px'}}>🧪 Soil Analysis</h3>
          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '14px'}}>
            <div><strong>pH:</strong> {data.soilData.ph}</div>
            <div><strong>Moisture:</strong> {data.soilData.moisture}%</div>
            <div><strong>Nitrogen:</strong> {data.soilData.nitrogen} mg/kg</div>
            <div><strong>Phosphorus:</strong> {data.soilData.phosphorus} mg/kg</div>
            <div><strong>Potassium:</strong> {data.soilData.potassium} mg/kg</div>
            <div><strong>Org. Carbon:</strong> {data.soilData.organicCarbon}%</div>
          </div>
        </div>

        {/* Weather & Crop Info Combined */}
        <div className="result-card" style={{padding: '20px', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)'}}>
          <h3 style={{color: '#2c5530', marginBottom: '15px'}}>🌤️ Current Conditions</h3>
          <p><strong>Weather:</strong> {data.weather_impact.temperature}°C, {data.weather_impact.description}</p>
          <p><strong>Humidity:</strong> {data.weather_impact.humidity}%</p>
          <p><strong>Crop:</strong> {data.soilData.cropType || 'Not specified'}</p>
          <p><strong>Season:</strong> {data.soilData.season}</p>
          <div style={{marginTop: '15px'}}>
            <Link to="/soil-input" className="btn btn-secondary" style={{fontSize: '12px', padding: '6px 12px'}}>Update Info</Link>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="card" style={{padding: '20px', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', marginBottom: '20px'}}>
        <h3 style={{color: '#2c5530', marginBottom: '20px'}}>💡 Recommendations</h3>
        
        {data.fertilizer_recommendations.primary_fertilizers.map((fertilizer, index) => (
          <div key={index} style={{marginBottom: '15px', padding: '15px', background: '#f8f9fa', borderRadius: '5px', border: '1px solid #e9ecef'}}>
            <h4 style={{margin: '0 0 8px 0', color: '#2c5530', fontSize: '16px'}}>{fertilizer.name}</h4>
            <p style={{margin: '4px 0', fontSize: '14px'}}><strong>Purpose:</strong> {fertilizer.purpose}</p>
            <p style={{margin: '4px 0', fontSize: '14px'}}><strong>Rate:</strong> {fertilizer.application_rate}</p>
          </div>
        ))}

        {data.fertilizer_recommendations.application_timing.length > 0 && (
          <div style={{marginTop: '15px'}}>
            <h4 style={{fontSize: '16px', color: '#2c5530', marginBottom: '10px'}}>Application Tips:</h4>
            <ul style={{margin: 0, paddingLeft: '20px'}}>
              {data.fertilizer_recommendations.application_timing.slice(0, 2).map((tip, index) => (
                <li key={index} style={{fontSize: '14px', marginBottom: '5px'}}>{tip}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Crop Suggestions */}
      <div className="card" style={{padding: '20px', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', marginBottom: '30px'}}>
        <h3 style={{color: '#2c5530', marginBottom: '20px'}}>🌾 Recommended Crops</h3>
        
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px'}}>
          {data.crop_suggestions.highly_suitable.slice(0, 3).map((crop, index) => (
            <div key={index} style={{padding: '15px', background: '#d4edda', borderRadius: '5px', border: '1px solid #c3e6cb', textAlign: 'center'}}>
              <div style={{fontSize: '16px', fontWeight: 'bold', color: '#155724', marginBottom: '5px'}}>{crop.name}</div>
              <div style={{fontSize: '12px', color: '#155724', textTransform: 'capitalize'}}>{crop.type}</div>
              <div style={{fontSize: '12px', color: '#28a745', marginTop: '8px', fontWeight: 'bold'}}>Suitability: {crop.suitability_score}%</div>
            </div>
          ))}
          
          {data.crop_suggestions.moderately_suitable.slice(0, 2).map((crop, index) => (
            <div key={index + 100} style={{padding: '15px', background: '#fff3cd', borderRadius: '5px', border: '1px solid #ffeaa7', textAlign: 'center'}}>
              <div style={{fontSize: '16px', fontWeight: 'bold', color: '#856404', marginBottom: '5px'}}>{crop.name}</div>
              <div style={{fontSize: '12px', color: '#856404', textTransform: 'capitalize'}}>{crop.type}</div>
              <div style={{fontSize: '12px', color: '#ffc107', marginTop: '8px', fontWeight: 'bold'}}>Suitability: {crop.suitability_score}%</div>
            </div>
          ))}
        </div>
      </div>

      <div className="text-center" style={{margin: '30px 0'}}>
        <Link to="/soil-input" className="btn btn-primary" style={{padding: '12px 24px', fontSize: '16px'}}>Add New Soil Data</Link>
      </div>
    </div>
  )
}

export default Dashboard
