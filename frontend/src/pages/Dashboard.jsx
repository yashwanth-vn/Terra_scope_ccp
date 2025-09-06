import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

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

      <div className="results-grid">
        {/* Fertility Status */}
        <div className={`result-card fertility-${data.fertility.level.toLowerCase()}`}>
          <h3>Fertility Level</h3>
          <div style={{fontSize: '2rem', fontWeight: 'bold', color: getFertilityColor(data.fertility.level)}}>
            {data.fertility.level}
          </div>
          <p>Score: {data.fertility.score}/100</p>
          <p>Confidence: {data.fertility.confidence}%</p>
        </div>

        {/* Soil Parameters */}
        <div className="result-card">
          <h3>Soil Parameters</h3>
          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px'}}>
            <div><strong>pH:</strong> {data.soilData.ph}</div>
            <div><strong>Moisture:</strong> {data.soilData.moisture}%</div>
            <div><strong>Nitrogen:</strong> {data.soilData.nitrogen} mg/kg</div>
            <div><strong>Phosphorus:</strong> {data.soilData.phosphorus} mg/kg</div>
            <div><strong>Potassium:</strong> {data.soilData.potassium} mg/kg</div>
            <div><strong>Organic Carbon:</strong> {data.soilData.organicCarbon}%</div>
          </div>
        </div>

        {/* Weather Impact */}
        <div className="result-card">
          <h3>Weather Conditions</h3>
          <p><strong>Temperature:</strong> {data.weather_impact.temperature}°C</p>
          <p><strong>Humidity:</strong> {data.weather_impact.humidity}%</p>
          <p><strong>Conditions:</strong> {data.weather_impact.description}</p>
          <p><strong>Location:</strong> {data.weather_impact.location}</p>
        </div>

        {/* Crop Info */}
        <div className="result-card">
          <h3>Current Crop Plan</h3>
          <p><strong>Crop:</strong> {data.soilData.cropType || 'Not specified'}</p>
          <p><strong>Season:</strong> {data.soilData.season}</p>
          <div style={{marginTop: '15px'}}>
            <Link to="/soil-input" className="btn btn-secondary">Update Info</Link>
          </div>
        </div>
      </div>

      {/* Fertilizer Recommendations */}
      <div className="card">
        <h3>💡 Fertilizer Recommendations</h3>
        {data.fertilizer_recommendations.primary_fertilizers.map((fertilizer, index) => (
          <div key={index} style={{marginBottom: '15px', padding: '15px', background: '#f8f9fa', borderRadius: '5px'}}>
            <h4 style={{margin: '0 0 10px 0', color: '#2c5530'}}>{fertilizer.name}</h4>
            <p><strong>Purpose:</strong> {fertilizer.purpose}</p>
            <p><strong>Application Rate:</strong> {fertilizer.application_rate}</p>
            <p><strong>Priority:</strong> 
              <span style={{
                color: fertilizer.priority === 'high' ? '#dc3545' : fertilizer.priority === 'medium' ? '#ffc107' : '#28a745',
                marginLeft: '8px',
                fontWeight: 'bold'
              }}>
                {fertilizer.priority.toUpperCase()}
              </span>
            </p>
          </div>
        ))}

        {data.fertilizer_recommendations.application_timing.length > 0 && (
          <div>
            <h4>Application Timing:</h4>
            <ul>
              {data.fertilizer_recommendations.application_timing.map((tip, index) => (
                <li key={index}>{tip}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Crop Suggestions */}
      <div className="card">
        <h3>🌾 Suitable Crops for Your Soil</h3>
        
        {data.crop_suggestions.highly_suitable.length > 0 && (
          <div style={{marginBottom: '20px'}}>
            <h4 style={{color: '#28a745'}}>Highly Suitable Crops</h4>
            <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px'}}>
              {data.crop_suggestions.highly_suitable.map((crop, index) => (
                <div key={index} style={{padding: '10px', background: '#d4edda', borderRadius: '5px', border: '1px solid #c3e6cb'}}>
                  <strong>{crop.name}</strong> ({crop.type})
                  <br />
                  <small>Suitability: {crop.suitability_score}%</small>
                </div>
              ))}
            </div>
          </div>
        )}

        {data.crop_suggestions.moderately_suitable.length > 0 && (
          <div>
            <h4 style={{color: '#ffc107'}}>Moderately Suitable Crops</h4>
            <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px'}}>
              {data.crop_suggestions.moderately_suitable.map((crop, index) => (
                <div key={index} style={{padding: '10px', background: '#fff3cd', borderRadius: '5px', border: '1px solid #ffeaa7'}}>
                  <strong>{crop.name}</strong> ({crop.type})
                  <br />
                  <small>Suitability: {crop.suitability_score}%</small>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="text-center" style={{margin: '30px 0'}}>
        <Link to="/soil-input" className="btn btn-primary">Add New Soil Data</Link>
      </div>
    </div>
  )
}

export default Dashboard
