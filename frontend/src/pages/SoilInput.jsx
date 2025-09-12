import React, { useState } from 'react'
import { Link } from 'react-router-dom'

function SoilInput() {
  const [soilData, setSoilData] = useState({
    ph: '',
    nitrogen: '',
    phosphorus: '',
    potassium: '',
    organicCarbon: '',
    moisture: '',
    cropType: '',
    season: 'spring'
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  const handleChange = (e) => {
    setSoilData({
      ...soilData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setSuccess(false)

    try {
      const authToken = localStorage.getItem('authToken')
      if (!authToken) {
        setError('Authentication required. Please log in.')
        return
      }

      // Submit soil data to backend
      const soilResponse = await fetch('http://localhost:5000/api/soil/input', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(soilData),
      })

      if (!soilResponse.ok) {
        throw new Error(`Failed to save soil data: ${soilResponse.status}`)
      }

      // Get predictions immediately
      const predictionResponse = await fetch('http://localhost:5000/api/predictions/fertility', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(soilData),
      })

      if (!predictionResponse.ok) {
        throw new Error(`Failed to get predictions: ${predictionResponse.status}`)
      }

      console.log('✅ Soil data saved and analyzed successfully!')
      setSuccess(true)
      
    } catch (err) {
      console.error('Error submitting soil data:', err)
      setError(`Failed to save soil data: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const resetForm = () => {
    setSoilData({
      ph: '',
      nitrogen: '',
      phosphorus: '',
      potassium: '',
      organicCarbon: '',
      moisture: '',
      cropType: '',
      season: 'spring'
    })
    setSuccess(false)
    setError('')
  }

  if (success) {
    return (
      <div className="container">
        <div className="card text-center">
          <h2>✅ Soil Data Saved Successfully!</h2>
          <p>Your soil test results have been recorded and are ready for analysis.</p>
          <div className="btn-group">
            <Link to="/dashboard" className="btn btn-primary">View Analysis</Link>
            <button 
              onClick={resetForm} 
              className="btn btn-secondary"
            >
              Add More Data
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="card">
        <h2 className="text-center mb-3">Enter Soil Test Results</h2>
        <p className="text-center" style={{color: '#666', marginBottom: '30px'}}>
          Use your soil testing kit to measure these parameters and enter the values below.
        </p>

        {error && (
          <div style={{background: '#ffebee', color: '#c62828', padding: '10px', borderRadius: '4px', marginBottom: '20px'}}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="soil-form">
            <div className="form-group">
              <label>pH Level *</label>
              <input
                type="number"
                name="ph"
                value={soilData.ph}
                onChange={handleChange}
                placeholder="6.5"
                step="0.1"
                min="0"
                max="14"
                required
              />
              <small style={{color: '#666'}}>Range: 0-14</small>
            </div>

            <div className="form-group">
              <label>Nitrogen (N) * mg/kg</label>
              <input
                type="number"
                name="nitrogen"
                value={soilData.nitrogen}
                onChange={handleChange}
                placeholder="100"
                step="0.1"
                min="0"
                required
              />
            </div>

            <div className="form-group">
              <label>Phosphorus (P) * mg/kg</label>
              <input
                type="number"
                name="phosphorus"
                value={soilData.phosphorus}
                onChange={handleChange}
                placeholder="20"
                step="0.1"
                min="0"
                required
              />
            </div>

            <div className="form-group">
              <label>Potassium (K) * mg/kg</label>
              <input
                type="number"
                name="potassium"
                value={soilData.potassium}
                onChange={handleChange}
                placeholder="120"
                step="0.1"
                min="0"
                required
              />
            </div>

            <div className="form-group">
              <label>Organic Carbon * %</label>
              <input
                type="number"
                name="organicCarbon"
                value={soilData.organicCarbon}
                onChange={handleChange}
                placeholder="1.5"
                step="0.01"
                min="0"
                max="10"
                required
              />
            </div>

            <div className="form-group">
              <label>Moisture %</label>
              <input
                type="number"
                name="moisture"
                value={soilData.moisture}
                onChange={handleChange}
                placeholder="25"
                step="0.1"
                min="0"
                max="100"
              />
              <small style={{color: '#666'}}>Optional</small>
            </div>
          </div>

          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '2rem'}}>
            <div className="form-group">
              <label>Crop Type</label>
              <input
                type="text"
                name="cropType"
                value={soilData.cropType}
                onChange={handleChange}
                placeholder="e.g., Wheat, Rice, Tomato"
              />
              <small style={{color: '#666'}}>What do you plan to grow?</small>
            </div>

            <div className="form-group">
              <label>Season</label>
              <select
                name="season"
                value={soilData.season}
                onChange={handleChange}
              >
                <option value="spring">Spring</option>
                <option value="summer">Summer</option>
                <option value="autumn">Autumn/Fall</option>
                <option value="winter">Winter</option>
              </select>
            </div>
          </div>

          <div className="text-center">
            <button 
              type="submit" 
              className="btn btn-success" 
              style={{padding: '12px 40px'}}
              disabled={loading}
            >
              {loading ? 'Saving Data...' : 'Save & Analyze Soil'}
            </button>
          </div>
        </form>

        <div className="card" style={{marginTop: '30px', background: '#f8f9fa'}}>
          <h4>💡 Soil Testing Tips</h4>
          <ul style={{textAlign: 'left', paddingLeft: '20px'}}>
            <li>Test soil when it's moist but not waterlogged</li>
            <li>Take samples from multiple spots and average the results</li>
            <li>Test at a depth of 6-8 inches for most crops</li>
            <li>pH is crucial - most crops prefer 6.0-7.5</li>
            <li>NPK values vary by region - compare with local standards</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default SoilInput
