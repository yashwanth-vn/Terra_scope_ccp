import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import '../styles/modern.css';

const History = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');
  const [isLoading, setIsLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [analysisHistory, setAnalysisHistory] = useState([]);
  const [chatSessions, setChatSessions] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    if (activeTab === 'overview') {
      loadDashboardStats();
    } else if (activeTab === 'analyses') {
      loadAnalysisHistory();
    } else if (activeTab === 'chats') {
      loadChatHistory();
    }
  }, [activeTab, currentPage]);

  const loadDashboardStats = async () => {
    setIsLoading(true);
    try {
        const token = localStorage.getItem('authToken');
      const response = await fetch('http://localhost:5000/api/history/dashboard', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setStats(data.stats);
        setAnalysisHistory(data.recent_activity.analysis_history || []);
        setChatSessions(data.recent_activity.chat_sessions || []);
      } else {
        console.error('Failed to load dashboard stats:', response.status);
        // Set default empty data if API fails
        setStats({
          total_analyses: 0,
          recent_analyses: 0,
          total_chats: 0,
          recent_chats: 0,
          fertility_distribution: {}
        });
      }
    } catch (error) {
      console.error('Error loading dashboard stats:', error);
      // Set default empty data if API fails
      setStats({
        total_analyses: 0,
        recent_analyses: 0,
        total_chats: 0,
        recent_chats: 0,
        fertility_distribution: {}
      });
    } finally {
      setIsLoading(false);
    }
  };

  const loadAnalysisHistory = async (page = 1) => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem('authToken');
      const response = await fetch(`http://localhost:5000/api/history/analysis?page=${page}&per_page=10`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setAnalysisHistory(data.history || []);
        setTotalPages(data.pagination?.pages || 1);
        setCurrentPage(page);
      }
    } catch (error) {
      console.error('Error loading analysis history:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadChatHistory = async (page = 1) => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem('authToken');
      const response = await fetch('http://localhost:5000/api/chat/sessions', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setChatSessions(data.sessions || []);
      }
    } catch (error) {
      console.error('Error loading chat history:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const exportHistory = async (exportType = 'all') => {
    try {
        const token = localStorage.getItem('authToken');
      const response = await fetch('http://localhost:5000/api/history/export', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          type: exportType,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        
        // Create and download the file
        const blob = new Blob([JSON.stringify(data.export_data, null, 2)], {
          type: 'application/json'
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `terra-scope-history-${exportType}-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Error exporting history:', error);
    }
  };

  const getFertilityColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'high': return 'bg-primary-100 text-primary-800 border-primary-200';
      case 'medium': return 'bg-secondary-100 text-secondary-800 border-secondary-200';
      case 'low': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const StatCard = ({ title, value, subtitle, icon, color = 'primary' }) => (
    <div className="card">
      <div className="card-body">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-600 text-sm">{title}</p>
            <p className={`text-2xl font-bold text-${color}-600`}>{value}</p>
            {subtitle && (
              <p className="text-gray-500 text-xs mt-1">{subtitle}</p>
            )}
          </div>
          <div className={`w-12 h-12 bg-${color}-100 rounded-lg flex items-center justify-center text-2xl`}>
            {icon}
          </div>
        </div>
      </div>
    </div>
  );

  if (isLoading && !stats) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">📊 History & Analytics</h1>
          <p className="text-gray-600">Track your farming journey and insights over time</p>
        </div>

        {/* Tabs */}
        <div className="mb-8">
          <div className="border-b border-gray-200 bg-white rounded-t-lg">
            <nav className="flex space-x-8 px-6">
              {[
                { id: 'overview', label: '📈 Overview', count: null },
                { id: 'analyses', label: '🧪 Soil Analyses', count: stats?.total_analyses },
                { id: 'chats', label: '💬 Chat History', count: stats?.total_chats },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id);
                    setCurrentPage(1);
                  }}
                  className={`py-4 px-2 text-sm font-medium border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  {tab.label}
                  {tab.count !== null && (
                    <span className="ml-2 bg-gray-100 text-gray-600 py-1 px-2 rounded-full text-xs">
                      {tab.count}
                    </span>
                  )}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Content */}
        <div className="bg-white rounded-b-lg shadow-sm">
          {activeTab === 'overview' && (
            <div className="p-6">
              {/* Stats Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <StatCard
                  title="Total Analyses"
                  value={stats?.total_analyses || 0}
                  subtitle={`${stats?.recent_analyses || 0} this week`}
                  icon="🧪"
                  color="primary"
                />
                <StatCard
                  title="Chat Sessions"
                  value={stats?.total_chats || 0}
                  subtitle={`${stats?.recent_chats || 0} recent`}
                  icon="💬"
                  color="blue"
                />
                <StatCard
                  title="High Fertility"
                  value={stats?.fertility_distribution?.High || 0}
                  subtitle="Soil samples"
                  icon="🌱"
                  color="primary"
                />
                <StatCard
                  title="Improvements"
                  value={stats?.fertility_distribution?.Medium || 0}
                  subtitle="Medium fertility"
                  icon="⚡"
                  color="secondary"
                />
              </div>

              {/* Recent Activity */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Recent Soil Analyses */}
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">🧪 Recent Soil Analyses</h3>
                    <button
                      onClick={() => setActiveTab('analyses')}
                      className="text-primary-600 hover:text-primary-700 text-sm"
                    >
                      View all →
                    </button>
                  </div>
                  <div className="space-y-3">
                    {analysisHistory.slice(0, 5).map((analysis, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex-1">
                          <p className="font-medium text-gray-900">{analysis.title}</p>
                          <p className="text-sm text-gray-500">{formatDate(analysis.createdAt)}</p>
                        </div>
                        <span className={`px-2 py-1 rounded-full text-xs border ${getFertilityColor(analysis.status)}`}>
                          {analysis.status}
                        </span>
                      </div>
                    ))}
                    {analysisHistory.length === 0 && (
                      <div className="text-center py-8 text-gray-500">
                        <p>No soil analyses yet</p>
                        <button
                          onClick={() => navigate('/soil-input')}
                          className="btn btn-primary btn-sm mt-2"
                        >
                          Start First Analysis
                        </button>
                      </div>
                    )}
                  </div>
                </div>

                {/* Recent Chat Sessions */}
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">💬 Recent Chat Sessions</h3>
                    <button
                      onClick={() => setActiveTab('chats')}
                      className="text-primary-600 hover:text-primary-700 text-sm"
                    >
                      View all →
                    </button>
                  </div>
                  <div className="space-y-3">
                    {chatSessions.slice(0, 5).map((session, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex-1">
                          <p className="font-medium text-gray-900">{session.title}</p>
                          <p className="text-sm text-gray-500">
                            {session.messageCount} messages • {formatDate(session.updatedAt)}
                          </p>
                        </div>
                        <button
                          onClick={() => navigate('/chatbot')}
                          className="btn-ghost btn-sm"
                        >
                          Open
                        </button>
                      </div>
                    ))}
                    {chatSessions.length === 0 && (
                      <div className="text-center py-8 text-gray-500">
                        <p>No chat sessions yet</p>
                        <button
                          onClick={() => navigate('/chatbot')}
                          className="btn btn-primary btn-sm mt-2"
                        >
                          Start Chatting
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Export Options */}
              <div className="mt-8 pt-6 border-t border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">📁 Export Data</h3>
                <div className="flex flex-wrap gap-3">
                  <button
                    onClick={() => exportHistory('all')}
                    className="btn btn-outline btn-sm"
                  >
                    📋 Export All Data
                  </button>
                  <button
                    onClick={() => exportHistory('soil_analyses')}
                    className="btn btn-outline btn-sm"
                  >
                    🧪 Export Soil Analyses
                  </button>
                  <button
                    onClick={() => exportHistory('chat_history')}
                    className="btn btn-outline btn-sm"
                  >
                    💬 Export Chat History
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'analyses' && (
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-semibold text-gray-900">🧪 Soil Analysis History</h3>
                <button
                  onClick={() => navigate('/soil-input')}
                  className="btn btn-primary"
                >
                  ➕ New Analysis
                </button>
              </div>

              {analysisHistory.length === 0 ? (
                <div className="text-center py-12">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center text-2xl mx-auto mb-4">
                    🧪
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No soil analyses yet</h3>
                  <p className="text-gray-500 mb-4">Start analyzing your soil to track your farming progress</p>
                  <button
                    onClick={() => navigate('/soil-input')}
                    className="btn btn-primary"
                  >
                    Start First Analysis
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  {analysisHistory.map((analysis, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <h4 className="text-lg font-medium text-gray-900">{analysis.title}</h4>
                          <p className="text-gray-600 text-sm mt-1">{analysis.description}</p>
                        </div>
                        <span className={`px-3 py-1 rounded-full text-sm border ${getFertilityColor(analysis.status)}`}>
                          {analysis.status}
                        </span>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                        <div>
                          <p className="text-sm text-gray-500">Analysis Type</p>
                          <p className="font-medium text-gray-900">{analysis.analysisType}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Location</p>
                          <p className="font-medium text-gray-900">{analysis.location || 'Not specified'}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Date</p>
                          <p className="font-medium text-gray-900">{formatDate(analysis.createdAt)}</p>
                        </div>
                      </div>

                      {analysis.cropType && (
                        <div className="flex flex-wrap gap-2 mb-4">
                          <span className="bg-primary-100 text-primary-800 px-2 py-1 rounded-full text-sm">
                            🌾 {analysis.cropType}
                          </span>
                          {analysis.season && (
                            <span className="bg-secondary-100 text-secondary-800 px-2 py-1 rounded-full text-sm">
                              🗓️ {analysis.season}
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  ))}

                  {/* Pagination */}
                  {totalPages > 1 && (
                    <div className="flex items-center justify-center gap-2 mt-8">
                      <button
                        onClick={() => loadAnalysisHistory(currentPage - 1)}
                        disabled={currentPage <= 1}
                        className="btn btn-secondary btn-sm"
                      >
                        Previous
                      </button>
                      <span className="px-4 py-2 text-sm text-gray-600">
                        Page {currentPage} of {totalPages}
                      </span>
                      <button
                        onClick={() => loadAnalysisHistory(currentPage + 1)}
                        disabled={currentPage >= totalPages}
                        className="btn btn-secondary btn-sm"
                      >
                        Next
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {activeTab === 'chats' && (
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-semibold text-gray-900">💬 Chat History</h3>
                <button
                  onClick={() => navigate('/chatbot')}
                  className="btn btn-primary"
                >
                  ➕ New Chat
                </button>
              </div>

              {chatSessions.length === 0 ? (
                <div className="text-center py-12">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center text-2xl mx-auto mb-4">
                    💬
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No chat sessions yet</h3>
                  <p className="text-gray-500 mb-4">Start chatting with Terra Bot to get farming advice</p>
                  <button
                    onClick={() => navigate('/chatbot')}
                    className="btn btn-primary"
                  >
                    Start Chatting
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {chatSessions.map((session, index) => (
                    <div key={index} className="card cursor-pointer" onClick={() => navigate('/chatbot')}>
                      <div className="card-body">
                        <div className="flex items-start justify-between mb-3">
                          <h4 className="font-medium text-gray-900 truncate flex-1">
                            {session.title}
                          </h4>
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            session.isActive ? 'bg-primary-100 text-primary-800' : 'bg-gray-100 text-gray-600'
                          }`}>
                            {session.isActive ? 'Active' : 'Archived'}
                          </span>
                        </div>
                        
                        <div className="space-y-2 text-sm text-gray-600">
                          <div className="flex items-center gap-2">
                            <span>💬</span>
                            <span>{session.messageCount} messages</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <span>📅</span>
                            <span>{formatDate(session.updatedAt)}</span>
                          </div>
                          {session.lastMessage && (
                            <div className="flex items-start gap-2 mt-3 p-2 bg-gray-50 rounded">
                              <span className="text-xs">💭</span>
                              <p className="text-xs text-gray-600 truncate">
                                {session.lastMessage.message?.substring(0, 100)}...
                              </p>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default History;
