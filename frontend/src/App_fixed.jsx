import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Home from './pages/Home'
import Login from './pages/Login'
import Signup from './pages/Signup'
import SoilInput from './pages/SoilInput'
import Dashboard from './pages/Dashboard'
import Profile from './pages/Profile'
import Chatbot from './pages/Chatbot'
import History from './pages/History'
import './App.css'

function Navigation() {
  const { isAuthenticated, user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/')
  }

  const navStyles = {
    navbar: {
      backgroundColor: 'white',
      boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
      borderBottom: '1px solid #e5e7eb',
      position: 'sticky',
      top: 0,
      zIndex: 1000
    },
    container: {
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '0 1rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      height: '64px'
    },
    logo: {
      fontSize: '1.5rem',
      fontWeight: 'bold',
      color: '#059669',
      textDecoration: 'none',
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem'
    },
    navLinks: {
      display: 'flex',
      alignItems: 'center',
      gap: '1.5rem'
    },
    navLink: {
      padding: '0.5rem 0.75rem',
      color: '#374151',
      textDecoration: 'none',
      borderRadius: '0.375rem',
      fontSize: '0.875rem',
      fontWeight: '500',
      transition: 'all 0.2s',
      display: 'flex',
      alignItems: 'center',
      gap: '0.25rem'
    },
    userWelcome: {
      fontSize: '0.875rem',
      color: '#6b7280',
      marginLeft: '1rem',
      paddingLeft: '1rem',
      borderLeft: '1px solid #e5e7eb'
    },
    userName: {
      fontWeight: '500',
      color: '#059669'
    },
    logoutBtn: {
      padding: '0.5rem 1rem',
      backgroundColor: '#f3f4f6',
      color: '#374151',
      border: '1px solid #d1d5db',
      borderRadius: '0.375rem',
      fontSize: '0.875rem',
      cursor: 'pointer',
      transition: 'all 0.2s',
      marginLeft: '0.75rem'
    },
    loginBtn: {
      padding: '0.5rem 1rem',
      backgroundColor: 'transparent',
      color: '#6b7280',
      textDecoration: 'none',
      borderRadius: '0.375rem',
      fontSize: '0.875rem',
      fontWeight: '500',
      transition: 'all 0.2s'
    },
    signupBtn: {
      padding: '0.5rem 1rem',
      backgroundColor: '#059669',
      color: 'white',
      textDecoration: 'none',
      borderRadius: '0.375rem',
      fontSize: '0.875rem',
      fontWeight: '500',
      transition: 'all 0.2s'
    }
  }

  return (
    <nav style={navStyles.navbar}>
      <div style={navStyles.container}>
        <Link to="/" style={navStyles.logo}>
          🌱 Terra Scope
        </Link>
        
        <div style={navStyles.navLinks}>
          {isAuthenticated() ? (
            <>
              <Link to="/soil-input" style={navStyles.navLink}>🧪 Soil Test</Link>
              <Link to="/dashboard" style={navStyles.navLink}>📊 Dashboard</Link>
              <Link to="/chatbot" style={navStyles.navLink}>🤖 Terra Bot</Link>
              <Link to="/history" style={navStyles.navLink}>📈 History</Link>
              <Link to="/profile" style={navStyles.navLink}>👤 Profile</Link>
              
              <div style={navStyles.userWelcome}>
                Hi, <span style={navStyles.userName}>{user?.firstName}</span>! 👋
                <button 
                  onClick={handleLogout}
                  style={navStyles.logoutBtn}
                  onMouseOver={(e) => {
                    e.target.style.backgroundColor = '#e5e7eb'
                    e.target.style.borderColor = '#9ca3af'
                  }}
                  onMouseOut={(e) => {
                    e.target.style.backgroundColor = '#f3f4f6'
                    e.target.style.borderColor = '#d1d5db'
                  }}
                >
                  Logout 🚪
                </button>
              </div>
            </>
          ) : (
            <>
              <Link 
                to="/login" 
                style={navStyles.loginBtn}
                onMouseOver={(e) => {
                  e.target.style.backgroundColor = '#f3f4f6'
                  e.target.style.color = '#374151'
                }}
                onMouseOut={(e) => {
                  e.target.style.backgroundColor = 'transparent'
                  e.target.style.color = '#6b7280'
                }}
              >
                🔑 Login
              </Link>
              <Link 
                to="/signup" 
                style={navStyles.signupBtn}
                onMouseOver={(e) => {
                  e.target.style.backgroundColor = '#047857'
                  e.target.style.transform = 'translateY(-1px)'
                }}
                onMouseOut={(e) => {
                  e.target.style.backgroundColor = '#059669'
                  e.target.style.transform = 'translateY(0)'
                }}
              >
                🌱 Join Terra Scope
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

function AppContent() {
  const { loading } = useAuth()

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        fontSize: '18px',
        color: '#059669',
        backgroundColor: '#f9fafb'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🌱</div>
          <div>Loading Terra Scope...</div>
        </div>
      </div>
    )
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb' }}>
      <Navigation />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/soil-input" element={<SoilInput />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/chatbot" element={<Chatbot />} />
          <Route path="/history" element={<History />} />
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
