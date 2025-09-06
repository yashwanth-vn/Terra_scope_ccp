import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Home from './pages/Home'
import Login from './pages/Login'
import Signup from './pages/Signup'
import SoilInput from './pages/SoilInput'
import Dashboard from './pages/Dashboard'
import Profile from './pages/Profile'
import './App.css'

function Navigation() {
  const { isAuthenticated, user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/')
  }

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <Link to="/">Terra Scope 🌱</Link>
      </div>
      <div className="nav-links">
        {isAuthenticated() ? (
          <>
            <Link to="/soil-input">🧪 Soil Data</Link>
            <Link to="/dashboard">📊 Dashboard</Link>
            <Link to="/profile">👤 Profile</Link>
            <span className="nav-user-greeting">Welcome, {user?.firstName}! 👋</span>
            <button 
              onClick={handleLogout}
            >
              Logout 🚪
            </button>
          </>
        ) : (
          <>
            <Link to="/login">🔑 Sign In</Link>
            <Link to="/signup">🌱 Join Terra Scope</Link>
          </>
        )}
      </div>
    </nav>
  )
}

function AppContent() {
  const { loading } = useAuth()

  if (loading) {
    return (
      <div className="App">
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100vh',
          fontSize: '18px',
          color: '#2c5530'
        }}>
          Loading Terra Scope...
        </div>
      </div>
    )
  }

  return (
    <div className="App">
      <Navigation />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/soil-input" element={<SoilInput />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </main>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  )
}

export default App
