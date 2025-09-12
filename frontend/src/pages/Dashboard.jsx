import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

// Simple Fertilizer Cost Calculator Component
function FertilizerCostCalculator({ fertilizers }) {
  const [landSize, setLandSize] = useState('')
  const [landUnit, setLandUnit] = useState('acres')
  const [region, setRegion] = useState('')
  const [cost, setCost] = useState(null)

  // Regional fertilizer pricing (per acre in INR)
  const regionalPricing = {
    'North India': 3500,
    'South India': 3800,
    'West India': 3600,
    'East India': 3300
  }

  const calculateCost = () => {
    if (!landSize || !region) return
    
    let acres = parseFloat(landSize)
    if (landUnit === 'hectares') {
      acres = acres * 2.47105
    }
    
    const pricePerAcre = regionalPricing[region] || 3500
    const totalCost = Math.round(pricePerAcre * acres)
    
    setCost({
      totalCost,
      pricePerAcre,
      acres: acres.toFixed(2)
    })
  }

  return (
    <div>
      <div style={{display: 'grid', gridTemplateColumns: '2fr 1fr 2fr', gap: '15px', marginBottom: '20px'}}>
        <div>
          <label style={{fontSize: '14px', fontWeight: 'bold', color: '#2c5530'}}>Land Size</label>
          <input
            type="number"
            value={landSize}
            onChange={(e) => setLandSize(e.target.value)}
            placeholder="Enter size"
            style={{width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '14px'}}
            step="0.1"
            min="0.1"
          />
        </div>
        
        <div>
          <label style={{fontSize: '14px', fontWeight: 'bold', color: '#2c5530'}}>Unit</label>
          <select
            value={landUnit}
            onChange={(e) => setLandUnit(e.target.value)}
            style={{width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '14px'}}
          >
            <option value="acres">Acres</option>
            <option value="hectares">Hectares</option>
          </select>
        </div>
        
        <div>
          <label style={{fontSize: '14px', fontWeight: 'bold', color: '#2c5530'}}>Region</label>
          <select
            value={region}
            onChange={(e) => setRegion(e.target.value)}
            style={{width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '14px'}}
          >
            <option value="">Select region</option>
            <option value="North India">North India</option>
            <option value="South India">South India</option>
            <option value="West India">West India</option>
            <option value="East India">East India</option>
          </select>
        </div>
      </div>
      
      <div style={{textAlign: 'center', marginBottom: '20px'}}>
        <button 
          onClick={calculateCost}
          disabled={!landSize || !region}
          style={{
            padding: '10px 20px',
            backgroundColor: landSize && region ? '#28a745' : '#ccc',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            fontSize: '14px',
            cursor: landSize && region ? 'pointer' : 'not-allowed'
          }}
        >
          Calculate Fertilizer Cost
        </button>
      </div>
      
      {cost && (
        <div style={{padding: '15px', background: '#e8f5e8', borderRadius: '5px', border: '2px solid #28a745', textAlign: 'center'}}>
          <h4 style={{color: '#155724', margin: '0 0 10px 0'}}>Estimated Fertilizer Cost</h4>
          <div style={{fontSize: '24px', fontWeight: 'bold', color: '#155724', marginBottom: '5px'}}>
            ₹{cost.totalCost.toLocaleString()}
          </div>
          <div style={{fontSize: '12px', color: '#155724'}}>
            For {cost.acres} acres in {region} (₹{cost.pricePerAcre}/acre)
          </div>
        </div>
      )}
      
      <div style={{fontSize: '12px', color: '#666', marginTop: '15px', textAlign: 'center'}}>
        <strong>Recommended:</strong> {Array.isArray(fertilizers) && fertilizers.length > 0 ? fertilizers[0] : 'NPK fertilizer'} - Standard application rate
      </div>
    </div>
  )
}

function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [refreshing, setRefreshing] = useState(false)
  const { isAuthenticated, token } = useAuth()
  const navigate = useNavigate()

  // Redirect to login if not authenticated
  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem('authToken')
      const user = localStorage.getItem('user')
      
      if (!token || !user || !isAuthenticated()) {
        console.log('Authentication check failed, redirecting to login')
        navigate('/login')
        return
      }
    }
    
    checkAuth()
  }, [isAuthenticated, navigate])

  useEffect(() => {
    // Test backend connectivity first
    const testBackendConnectivity = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/health', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          timeout: 5000
        })
        if (!response.ok) {
          throw new Error('Backend health check failed')
        }
        console.log('✅ Backend connectivity test: SUCCESS')
      } catch (err) {
        console.error('❌ Backend connectivity test: FAILED', err)
        setError('Cannot connect to backend server. Please ensure the backend is running on http://localhost:5000')
        setLoading(false)
        return false
      }
      return true
    }
    
    // Make real API call to get latest soil analysis
    const fetchData = async () => {
      // Test connectivity first
      const isConnected = await testBackendConnectivity()
      if (!isConnected) return
      try {
        const authToken = localStorage.getItem('authToken')
        if (!authToken) {
          setError('Authentication required')
          setLoading(false)
          return
        }

        const response = await fetch('http://localhost:5000/api/predictions/analyze-latest', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json',
          },
        })

        if (!response.ok) {
          // Handle authentication errors
          if (response.status === 401) {
            localStorage.removeItem('authToken')
            localStorage.removeItem('user')
            navigate('/login')
            return
          }
          
          // If no soil data exists, create sample data and analyze it
          if (response.status === 404) {
            // Create sample soil data first
            const sampleSoilData = {
              ph: 6.5,
              nitrogen: Math.floor(Math.random() * 100) + 50,
              phosphorus: Math.floor(Math.random() * 50) + 20,
              potassium: Math.floor(Math.random() * 200) + 100,
              organicCarbon: (Math.random() * 3 + 1.5).toFixed(1),
              moisture: Math.floor(Math.random() * 20) + 20,
              cropType: 'Mixed',
              season: 'All Season'
            }

            // Submit soil data
            const submitResponse = await fetch('http://localhost:5000/api/soil/input', {
              method: 'POST',
              headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(sampleSoilData),
            })

            if (submitResponse.ok) {
              // Now analyze the submitted data
              const analysisResponse = await fetch('http://localhost:5000/api/predictions/analyze-latest', {
                method: 'GET',
                headers: {
                  'Authorization': `Bearer ${authToken}`,
                  'Content-Type': 'application/json',
                },
              })

              if (analysisResponse.ok) {
                const analysisData = await analysisResponse.json()
                setData(analysisData)
              } else if (analysisResponse.status === 401) {
                localStorage.removeItem('authToken')
                localStorage.removeItem('user')
                navigate('/login')
                return
              } else {
                throw new Error('Failed to analyze soil data')
              }
            } else if (submitResponse.status === 401) {
              localStorage.removeItem('authToken')
              localStorage.removeItem('user')
              navigate('/login')
              return
            } else {
              throw new Error('Failed to submit soil data')
            }
          } else {
            throw new Error(`API error: ${response.status}`)
          }
        } else {
          const responseData = await response.json()
          setData(responseData)
        }
      } catch (err) {
        console.error('Dashboard fetch error:', err)
        
        // Enhanced error handling with detailed debugging info
        let errorMessage = 'Failed to load dashboard data: '
        
        if (err.message === 'Failed to fetch') {
          errorMessage += 'Cannot connect to backend server. Please check if the backend is running on http://localhost:5000'
        } else if (err.message.includes('NetworkError')) {
          errorMessage += 'Network error - check your internet connection and backend server'
        } else if (err.message.includes('401')) {
          errorMessage += 'Authentication expired. Please login again.'
          localStorage.removeItem('authToken')
          localStorage.removeItem('user')
          navigate('/login')
          return
        } else {
          errorMessage += err.message
        }
        
        // Add debugging info in development
        console.log('Debug Info:')  
        console.log('- Auth token exists:', !!localStorage.getItem('authToken'))
        console.log('- User data exists:', !!localStorage.getItem('user'))
        console.log('- Backend URL:', 'http://localhost:5000/api/predictions/analyze-latest')
        console.log('- Error type:', typeof err)
        console.log('- Full error:', err)
        
        setError(errorMessage)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const refreshDashboard = async () => {
    setRefreshing(true)
    setError('')
    
    try {
      const authToken = localStorage.getItem('authToken')
      if (!authToken) {
        setError('Authentication required')
        return
      }

      const response = await fetch('http://localhost:5000/api/predictions/analyze-latest', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const responseData = await response.json()
        setData(responseData)
        console.log('✅ Dashboard refreshed successfully!')
      } else if (response.status === 401) {
        localStorage.removeItem('authToken')
        localStorage.removeItem('user')
        navigate('/login')
      } else {
        throw new Error(`Failed to refresh: ${response.status}`)
      }
    } catch (err) {
      console.error('Refresh error:', err)
      setError(`Failed to refresh data: ${err.message}`)
    } finally {
      setRefreshing(false)
    }
  }

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
    const isAuthError = error.includes('401') || error.includes('Authentication')
    return (
      <div className="container">
        <div className="card text-center">
          <h2>⚠️ {isAuthError ? 'Login Required' : 'Error Loading Data'}</h2>
          <p>{error}</p>
          {isAuthError ? (
            <div>
              <p style={{color: '#666', marginBottom: '20px'}}>You need to log in to view your dashboard.</p>
              <div className="btn-group">
                <Link to="/login" className="btn btn-primary">Login</Link>
                <Link to="/signup" className="btn btn-secondary">Sign Up</Link>
              </div>
            </div>
          ) : (
            <Link to="/soil-input" className="btn btn-primary">Add Soil Data</Link>
          )}
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
      case 'excellent': return '#28a745'
      case 'good': return '#28a745'
      case 'fair': return '#ffc107'
      case 'poor': return '#fd7e14'
      case 'very poor': return '#dc3545'
      case 'high': return '#28a745'
      case 'medium': return '#ffc107'
      case 'low': return '#dc3545'
      default: return '#6c757d'
    }
  }

  return (
    <div className="container">
      <div className="card">
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px'}}>
          <h1 style={{margin: 0}}>🌱 Soil Fertility Dashboard</h1>
          <button 
            onClick={refreshDashboard}
            disabled={refreshing}
            className="btn btn-secondary"
            style={{fontSize: '14px', padding: '8px 16px'}}
          >
            {refreshing ? '🔄 Refreshing...' : '🔄 Refresh'}
          </button>
        </div>
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
          {data.fertility.analysis && <p><strong>Analysis:</strong> {data.fertility.analysis.substring(0, 100)}...</p>}
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
        
        {Array.isArray(data.fertilizer_recommendations) ? data.fertilizer_recommendations.map((fertilizer, index) => (
          <div key={index} style={{marginBottom: '15px', padding: '15px', background: '#f8f9fa', borderRadius: '5px', border: '1px solid #e9ecef'}}>
            <h4 style={{margin: '0 0 8px 0', color: '#2c5530', fontSize: '16px'}}>{fertilizer}</h4>
            <p style={{margin: '4px 0', fontSize: '14px'}}><strong>Purpose:</strong> Soil nutrient enhancement</p>
            <p style={{margin: '4px 0', fontSize: '14px'}}><strong>Application:</strong> As per soil requirements</p>
          </div>
        )) : (
          <div style={{marginBottom: '15px', padding: '15px', background: '#f8f9fa', borderRadius: '5px', border: '1px solid #e9ecef'}}>
            <h4 style={{margin: '0 0 8px 0', color: '#2c5530', fontSize: '16px'}}>No specific recommendations available</h4>
            <p style={{margin: '4px 0', fontSize: '14px'}}>Please add soil data for personalized recommendations</p>
          </div>
        )}
      </div>

      {/* Crop Suggestions */}
      <div className="card" style={{padding: '20px', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', marginBottom: '30px'}}>
        <h3 style={{color: '#2c5530', marginBottom: '20px'}}>🌾 Recommended Crops</h3>
        
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px'}}>
          {Array.isArray(data.crop_recommendations) ? data.crop_recommendations.slice(0, 6).map((crop, index) => (
            <div key={index} style={{padding: '15px', background: '#d4edda', borderRadius: '5px', border: '1px solid #c3e6cb', textAlign: 'center'}}>
              <div style={{fontSize: '16px', fontWeight: 'bold', color: '#155724', marginBottom: '5px'}}>{crop}</div>
              <div style={{fontSize: '12px', color: '#155724', textTransform: 'capitalize'}}>Recommended</div>
              <div style={{fontSize: '12px', color: '#28a745', marginTop: '8px', fontWeight: 'bold'}}>Suitable for your soil</div>
            </div>
          )) : (
            <div style={{padding: '15px', background: '#fff3cd', borderRadius: '5px', border: '1px solid #ffeaa7', textAlign: 'center'}}>
              <div style={{fontSize: '16px', fontWeight: 'bold', color: '#856404', marginBottom: '5px'}}>No specific recommendations</div>
              <div style={{fontSize: '12px', color: '#856404'}}>Please add soil data for personalized crop suggestions</div>
            </div>
          )}
        </div>
      </div>

      {/* Simple Fertilizer Cost Calculator */}
      <div className="card" style={{padding: '20px', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', marginBottom: '30px'}}>
        <h3 style={{color: '#2c5530', marginBottom: '20px'}}>💰 Fertilizer Cost Calculator</h3>
        <FertilizerCostCalculator fertilizers={data.fertilizer_recommendations || []} />
      </div>

      <div className="text-center" style={{margin: '30px 0'}}>
        <Link to="/soil-input" className="btn btn-primary" style={{padding: '12px 24px', fontSize: '16px'}}>Add New Soil Data</Link>
      </div>
    </div>
  )
}

export default Dashboard
