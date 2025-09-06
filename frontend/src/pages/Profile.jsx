import React, { useState } from 'react'
import { Link } from 'react-router-dom'

function Profile() {
  // Mock user data - in production this would come from authentication context
  const [user, setUser] = useState({
    firstName: 'John',
    lastName: 'Farmer',
    email: 'john.farmer@email.com',
    location: 'Delhi, India',
    contactNumber: '+91 9876543210',
    joinedDate: '2024-09-06'
  })

  const [isEditing, setIsEditing] = useState(false)
  const [editData, setEditData] = useState({ ...user })

  const handleEditChange = (e) => {
    setEditData({
      ...editData,
      [e.target.name]: e.target.value
    })
  }

  const handleSave = () => {
    // TODO: Implement API call to update user profile
    setUser(editData)
    setIsEditing(false)
    alert('Profile updated successfully!')
  }

  const handleCancel = () => {
    setEditData({ ...user })
    setIsEditing(false)
  }

  const handleLogout = () => {
    // TODO: Implement proper logout - clear tokens, redirect to home
    if (window.confirm('Are you sure you want to log out?')) {
      alert('Logged out successfully! (This will be replaced with proper authentication)')
      // Redirect to home page
    }
  }

  return (
    <div className="container">
      <div className="card">
        <h2 className="text-center mb-3">👤 User Profile</h2>
        
        {!isEditing ? (
          <div>
            <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '2rem'}}>
              <div>
                <h4>Personal Information</h4>
                <p><strong>Name:</strong> {user.firstName} {user.lastName}</p>
                <p><strong>Email:</strong> {user.email}</p>
                <p><strong>Location:</strong> {user.location || 'Not specified'}</p>
                <p><strong>Contact:</strong> {user.contactNumber || 'Not specified'}</p>
                <p><strong>Member since:</strong> {new Date(user.joinedDate).toLocaleDateString()}</p>
              </div>
              
              <div>
                <h4>Account Statistics</h4>
                <p><strong>Soil Tests:</strong> 5 records</p>
                <p><strong>Last Analysis:</strong> 2 days ago</p>
                <p><strong>Fertility Trend:</strong> Improving ↗️</p>
                <p><strong>Favorite Crop:</strong> Wheat</p>
              </div>
            </div>
            
            <div className="text-center">
              <button 
                onClick={() => setIsEditing(true)}
                className="btn btn-primary"
                style={{marginRight: '1rem'}}
              >
                Edit Profile
              </button>
              <button 
                onClick={handleLogout}
                className="btn btn-secondary"
              >
                Logout
              </button>
            </div>
          </div>
        ) : (
          <div>
            <form onSubmit={(e) => { e.preventDefault(); handleSave(); }}>
              <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '2rem'}}>
                <div className="form-group">
                  <label>First Name</label>
                  <input
                    type="text"
                    name="firstName"
                    value={editData.firstName}
                    onChange={handleEditChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Last Name</label>
                  <input
                    type="text"
                    name="lastName"
                    value={editData.lastName}
                    onChange={handleEditChange}
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Email Address</label>
                <input
                  type="email"
                  name="email"
                  value={editData.email}
                  onChange={handleEditChange}
                  required
                  disabled
                  style={{backgroundColor: '#f8f9fa'}}
                />
                <small style={{color: '#666'}}>Email cannot be changed</small>
              </div>

              <div className="form-group">
                <label>Location</label>
                <input
                  type="text"
                  name="location"
                  value={editData.location}
                  onChange={handleEditChange}
                  placeholder="City, Country"
                />
                <small style={{color: '#666'}}>Used for weather data integration</small>
              </div>

              <div className="form-group">
                <label>Contact Number</label>
                <input
                  type="tel"
                  name="contactNumber"
                  value={editData.contactNumber}
                  onChange={handleEditChange}
                  placeholder="Phone number"
                />
              </div>

              <div className="text-center">
                <button 
                  type="submit"
                  className="btn btn-success"
                  style={{marginRight: '1rem'}}
                >
                  Save Changes
                </button>
                <button 
                  type="button"
                  onClick={handleCancel}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3>Quick Actions</h3>
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem'}}>
          <Link to="/soil-input" className="btn btn-primary">
            📝 Add Soil Data
          </Link>
          <Link to="/dashboard" className="btn btn-success">
            📊 View Dashboard
          </Link>
          <button 
            className="btn btn-secondary"
            onClick={() => alert('Feature coming soon!')}
          >
            📈 View History
          </button>
          <button 
            className="btn btn-secondary"
            onClick={() => alert('Feature coming soon!')}
          >
            📋 Export Reports
          </button>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h3>Recent Activity</h3>
        <div style={{textAlign: 'left'}}>
          <div style={{padding: '10px', borderBottom: '1px solid #eee', marginBottom: '10px'}}>
            <p><strong>Soil Analysis Completed</strong></p>
            <small style={{color: '#666'}}>2 days ago - Fertility level: High (78.5 score)</small>
          </div>
          <div style={{padding: '10px', borderBottom: '1px solid #eee', marginBottom: '10px'}}>
            <p><strong>Profile Updated</strong></p>
            <small style={{color: '#666'}}>1 week ago - Added location information</small>
          </div>
          <div style={{padding: '10px', borderBottom: '1px solid #eee', marginBottom: '10px'}}>
            <p><strong>Account Created</strong></p>
            <small style={{color: '#666'}}>{new Date(user.joinedDate).toLocaleDateString()} - Welcome to Terra Scope!</small>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profile
