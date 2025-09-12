import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';

const Chatbot = () => {
  const { user } = useAuth();
  const [sessions, setSessions] = useState([]);
  const [currentSession, setCurrentSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load chat sessions on component mount
  useEffect(() => {
    loadChatSessions();
  }, []);

  // Focus input when session changes
  useEffect(() => {
    if (currentSession && inputRef.current) {
      inputRef.current.focus();
    }
  }, [currentSession]);

  const loadChatSessions = async () => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.warn('No auth token found');
        setIsLoading(false);
        return;
      }

      const response = await fetch('http://localhost:5000/api/chat/sessions', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setSessions(data.sessions || []);
        
        // Load first session if available
        if (data.sessions && data.sessions.length > 0) {
          loadChatMessages(data.sessions[0].id);
        }
      } else {
        const errorData = await response.json().catch(() => ({ message: 'Network error' }));
        console.error('Failed to load chat sessions:', errorData);
        if (response.status === 401) {
          alert('Your session has expired. Please log in again.');
        }
      }
    } catch (error) {
      console.error('Error loading chat sessions:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadChatMessages = async (sessionId) => {
    try {
      const token = localStorage.getItem('authToken');
      const response = await fetch(`http://localhost:5000/api/chat/sessions/${sessionId}/messages`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setCurrentSession(data.session);
        setMessages(data.messages || []);
      }
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const createNewSession = async () => {
    try {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('No auth token found when creating session');
        alert('You need to be logged in to use the chatbot.');
        return null;
      }

      const response = await fetch('http://localhost:5000/api/chat/sessions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: 'New Chat'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const newSession = data.session;
        setSessions(prev => [newSession, ...prev]);
        setCurrentSession(newSession);
        setMessages([]);
        setSuggestions([]);
        return newSession;
      } else {
        const errorData = await response.json().catch(() => ({ message: 'Network error' }));
        console.error('Failed to create chat session:', errorData);
        if (response.status === 401) {
          alert('Your session has expired. Please log in again.');
        } else {
          alert(`Failed to create chat session: ${errorData.message || 'Unknown error'}`);
        }
      }
    } catch (error) {
      console.error('Error creating new session:', error);
      alert('Network error. Please check your connection and try again.');
    }
    return null;
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || isSending) return;

    const message = inputMessage.trim();
    setInputMessage('');
    setIsSending(true);

    // If no current session, create one first
    let sessionToUse = currentSession;
    if (!sessionToUse) {
      sessionToUse = await createNewSession();
      if (!sessionToUse) {
        setIsSending(false);
        setInputMessage(message);
        alert('Failed to create chat session. Please try again.');
        return;
      }
    }

    try {
      const token = localStorage.getItem('authToken');
      const response = await fetch(`http://localhost:5000/api/chat/sessions/${sessionToUse.id}/messages`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          message_type: 'text'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        
        // Add user message and bot response to messages
        setMessages(prev => [...prev, data.chat_message]);
        setSuggestions(data.suggestions || []);
        
        // Update current session
        setCurrentSession(data.session);
        
        // Update session in sidebar
        setSessions(prev => 
          prev.map(s => s.id === data.session.id ? data.session : s)
        );
      } else {
        console.error('Failed to send message:', response.statusText);
        setInputMessage(message);
        alert('Failed to send message. Please try again.');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setInputMessage(message);
      alert('Error sending message. Please check your connection.');
    } finally {
      setIsSending(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion);
    inputRef.current?.focus();
  };

  const deleteSession = async (sessionId, e) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this chat session?')) return;

    try {
      const token = localStorage.getItem('authToken');
      const response = await fetch(`http://localhost:5000/api/chat/sessions/${sessionId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setSessions(prev => prev.filter(s => s.id !== sessionId));
        
        if (currentSession?.id === sessionId) {
          const remainingSessions = sessions.filter(s => s.id !== sessionId);
          if (remainingSessions.length > 0) {
            loadChatMessages(remainingSessions[0].id);
          } else {
            setCurrentSession(null);
            setMessages([]);
            setSuggestions([]);
          }
        }
      }
    } catch (error) {
      console.error('Error deleting session:', error);
    }
  };

  const formatMessage = (text) => {
    return text.split('\n').map((line, index) => (
      <React.Fragment key={index}>
        {line}
        {index < text.split('\n').length - 1 && <br />}
      </React.Fragment>
    ));
  };

  const styles = {
    container: {
      minHeight: '100vh',
      backgroundColor: '#f9fafb',
      display: 'flex'
    },
    sidebar: {
      width: sidebarOpen ? '320px' : '0',
      transition: 'all 0.3s',
      backgroundColor: 'white',
      borderRight: '1px solid #e5e7eb',
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden'
    },
    sidebarHeader: {
      padding: '1.5rem',
      borderBottom: '1px solid #e5e7eb'
    },
    sidebarTitle: {
      fontSize: '1.25rem',
      fontWeight: '600',
      color: '#111827',
      marginBottom: '1rem'
    },
    newChatBtn: {
      width: '100%',
      padding: '0.75rem 1rem',
      backgroundColor: '#059669',
      color: 'white',
      border: 'none',
      borderRadius: '0.375rem',
      fontSize: '0.875rem',
      fontWeight: '500',
      cursor: 'pointer',
      transition: 'all 0.2s'
    },
    sessionsList: {
      flex: 1,
      overflowY: 'auto',
      padding: '1rem'
    },
    sessionItem: {
      padding: '0.75rem',
      marginBottom: '0.5rem',
      backgroundColor: '#f9fafb',
      borderRadius: '0.5rem',
      cursor: 'pointer',
      transition: 'all 0.2s',
      border: '1px solid #e5e7eb'
    },
    activeSession: {
      backgroundColor: '#ecfdf5',
      borderColor: '#059669'
    },
    mainChat: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column'
    },
    chatHeader: {
      backgroundColor: 'white',
      borderBottom: '1px solid #e5e7eb',
      padding: '1rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    },
    toggleBtn: {
      padding: '0.5rem',
      backgroundColor: 'transparent',
      border: 'none',
      fontSize: '1.25rem',
      cursor: 'pointer'
    },
    botInfo: {
      display: 'flex',
      alignItems: 'center',
      gap: '0.75rem'
    },
    botAvatar: {
      width: '2.5rem',
      height: '2.5rem',
      backgroundColor: '#059669',
      borderRadius: '50%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: '1.25rem'
    },
    messagesArea: {
      flex: 1,
      overflowY: 'auto',
      padding: '1.5rem',
      display: 'flex',
      flexDirection: 'column',
      gap: '1.5rem'
    },
    welcomeScreen: {
      textAlign: 'center',
      padding: '3rem 1rem'
    },
    welcomeAvatar: {
      width: '5rem',
      height: '5rem',
      backgroundColor: '#059669',
      borderRadius: '50%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: '2rem',
      margin: '0 auto 1.5rem'
    },
    welcomeTitle: {
      fontSize: '1.5rem',
      fontWeight: '600',
      color: '#111827',
      marginBottom: '1rem'
    },
    welcomeText: {
      color: '#6b7280',
      marginBottom: '1.5rem',
      maxWidth: '28rem',
      margin: '0 auto 1.5rem'
    },
    suggestionBtns: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: '0.5rem',
      justifyContent: 'center'
    },
    suggestionBtn: {
      padding: '0.5rem 1rem',
      backgroundColor: 'transparent',
      color: '#059669',
      border: '1px solid #059669',
      borderRadius: '0.375rem',
      fontSize: '0.875rem',
      cursor: 'pointer',
      transition: 'all 0.2s'
    },
    userMessage: {
      display: 'flex',
      justifyContent: 'flex-end'
    },
    userBubble: {
      backgroundColor: '#059669',
      color: 'white',
      padding: '1rem',
      borderRadius: '1rem 1rem 0.25rem 1rem',
      maxWidth: '24rem',
      fontSize: '0.875rem'
    },
    botMessage: {
      display: 'flex',
      justifyContent: 'flex-start'
    },
    botBubbleContainer: {
      display: 'flex',
      gap: '0.75rem',
      maxWidth: '32rem'
    },
    botAvatar2: {
      width: '2rem',
      height: '2rem',
      backgroundColor: '#059669',
      borderRadius: '50%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: '0.875rem',
      flexShrink: 0
    },
    botBubble: {
      backgroundColor: 'white',
      padding: '1rem',
      borderRadius: '1rem 1rem 1rem 0.25rem',
      boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      border: '1px solid #e5e7eb',
      fontSize: '0.875rem',
      color: '#111827'
    },
    loadingIndicator: {
      display: 'flex',
      gap: '0.75rem'
    },
    loadingDots: {
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem'
    },
    loadingSpinner: {
      width: '1rem',
      height: '1rem',
      border: '2px solid #e5e7eb',
      borderRadius: '50%',
      borderTopColor: '#059669',
      animation: 'spin 1s linear infinite'
    },
    suggestionsArea: {
      padding: '0 1.5rem 1rem',
      display: 'flex',
      flexWrap: 'wrap',
      gap: '0.5rem'
    },
    inputArea: {
      backgroundColor: 'white',
      borderTop: '1px solid #e5e7eb',
      padding: '1.5rem'
    },
    inputForm: {
      display: 'flex',
      gap: '0.75rem'
    },
    messageInput: {
      flex: 1,
      padding: '0.75rem',
      border: '1px solid #d1d5db',
      borderRadius: '0.375rem',
      fontSize: '0.875rem',
      outline: 'none'
    },
    sendBtn: {
      padding: '0.75rem 1.5rem',
      backgroundColor: '#059669',
      color: 'white',
      border: 'none',
      borderRadius: '0.375rem',
      fontSize: '1.25rem',
      cursor: 'pointer',
      transition: 'all 0.2s'
    },
    disabledBtn: {
      backgroundColor: '#9ca3af',
      cursor: 'not-allowed'
    },
    disclaimer: {
      textAlign: 'center',
      color: '#6b7280',
      fontSize: '0.75rem',
      marginTop: '0.5rem'
    }
  };

  if (isLoading) {
    return (
      <div style={{
        minHeight: '100vh',
        backgroundColor: '#f9fafb',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={styles.loadingSpinner}></div>
          <p style={{ color: '#6b7280', marginTop: '1rem' }}>Loading Terra Bot...</p>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      {/* Sidebar */}
      <div style={styles.sidebar}>
        <div style={styles.sidebarHeader}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <h1 style={styles.sidebarTitle}>🤖 Terra Bot</h1>
          </div>
          <button
            onClick={createNewSession}
            style={styles.newChatBtn}
            onMouseOver={(e) => e.target.style.backgroundColor = '#047857'}
            onMouseOut={(e) => e.target.style.backgroundColor = '#059669'}
          >
            ➕ New Chat
          </button>
        </div>

        <div style={styles.sessionsList}>
          {sessions.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem 0', color: '#6b7280' }}>
              <p style={{ fontSize: '0.875rem' }}>No chat sessions yet</p>
              <p style={{ fontSize: '0.75rem', marginTop: '0.25rem' }}>Start a new conversation!</p>
            </div>
          ) : (
            sessions.map((session) => (
              <div
                key={session.id}
                onClick={() => loadChatMessages(session.id)}
                style={{
                  ...styles.sessionItem,
                  ...(currentSession?.id === session.id ? styles.activeSession : {})
                }}
                onMouseOver={(e) => {
                  if (currentSession?.id !== session.id) {
                    e.target.style.backgroundColor = '#f3f4f6';
                  }
                }}
                onMouseOut={(e) => {
                  if (currentSession?.id !== session.id) {
                    e.target.style.backgroundColor = '#f9fafb';
                  }
                }}
              >
                <div style={{ display: 'flex', alignItems: 'start', justifyContent: 'space-between' }}>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <h3 style={{ fontSize: '0.875rem', fontWeight: '500', color: '#111827', margin: 0, marginBottom: '0.25rem' }}>
                      {session.title}
                    </h3>
                    <p style={{ fontSize: '0.75rem', color: '#6b7280', margin: 0 }}>
                      {session.messageCount} messages
                    </p>
                    <p style={{ fontSize: '0.75rem', color: '#9ca3af', margin: 0 }}>
                      {new Date(session.updatedAt).toLocaleDateString()}
                    </p>
                  </div>
                  <button
                    onClick={(e) => deleteSession(session.id, e)}
                    style={{
                      background: 'none',
                      border: 'none',
                      cursor: 'pointer',
                      fontSize: '1rem',
                      color: '#ef4444',
                      opacity: 0.7,
                      padding: '0.25rem'
                    }}
                    onMouseOver={(e) => e.target.style.opacity = 1}
                    onMouseOut={(e) => e.target.style.opacity = 0.7}
                  >
                    🗑️
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Main Chat Area */}
      <div style={styles.mainChat}>
        {/* Header */}
        <div style={styles.chatHeader}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            {!sidebarOpen && (
              <button
                onClick={() => setSidebarOpen(true)}
                style={styles.toggleBtn}
              >
                ☰
              </button>
            )}
            <div style={styles.botInfo}>
              <div style={styles.botAvatar}>🌱</div>
              <div>
                <h2 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#111827', margin: 0 }}>
                  {currentSession?.title || 'Terra Bot Assistant'}
                </h2>
                <p style={{ fontSize: '0.875rem', color: '#6b7280', margin: 0 }}>Your AI Agricultural Expert</p>
              </div>
            </div>
          </div>
          <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>
            Welcome, {user?.firstName}! 👋
          </div>
        </div>

        {/* Messages Area */}
        <div style={styles.messagesArea}>
          {messages.length === 0 ? (
            <div style={styles.welcomeScreen}>
              <div style={styles.welcomeAvatar}>🤖</div>
              <h2 style={styles.welcomeTitle}>
                Hello! I'm Terra Bot 🌱
              </h2>
              <p style={styles.welcomeText}>
                I'm your AI agricultural assistant. Ask me anything about soil analysis, 
                crop recommendations, fertilizers, or farming tips!
              </p>
              <div style={styles.suggestionBtns}>
                {[
                  "What crops should I plant?",
                  "How can I improve my soil?",
                  "Analyze my soil pH",
                  "Seasonal farming tips"
                ].map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => handleSuggestionClick(suggestion)}
                    style={styles.suggestionBtn}
                    onMouseOver={(e) => {
                      e.target.style.backgroundColor = '#059669';
                      e.target.style.color = 'white';
                    }}
                    onMouseOut={(e) => {
                      e.target.style.backgroundColor = 'transparent';
                      e.target.style.color = '#059669';
                    }}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <>
              {messages.map((msg, index) => (
                <div key={index}>
                  {/* User Message */}
                  <div style={styles.userMessage}>
                    <div style={styles.userBubble}>
                      <p style={{ margin: 0 }}>{formatMessage(msg.message)}</p>
                      <p style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.7)', margin: '0.5rem 0 0 0' }}>
                        {new Date(msg.createdAt).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>

                  {/* Bot Response */}
                  {msg.response && (
                    <div style={styles.botMessage}>
                      <div style={styles.botBubbleContainer}>
                        <div style={styles.botAvatar2}>🌱</div>
                        <div style={styles.botBubble}>
                          <p style={{ margin: 0, marginBottom: '0.5rem' }}>{formatMessage(msg.response)}</p>
                          <p style={{ fontSize: '0.75rem', color: '#6b7280', margin: 0 }}>
                            Terra Bot • {new Date(msg.createdAt).toLocaleTimeString()}
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}

              {/* Loading indicator */}
              {isSending && (
                <div style={styles.botMessage}>
                  <div style={styles.loadingIndicator}>
                    <div style={styles.botAvatar2}>🌱</div>
                    <div style={styles.botBubble}>
                      <div style={styles.loadingDots}>
                        <div style={styles.loadingSpinner}></div>
                        <span style={{ fontSize: '0.875rem', color: '#6b7280' }}>Thinking...</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Suggestions */}
        {suggestions.length > 0 && (
          <div style={styles.suggestionsArea}>
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                style={{
                  padding: '0.5rem 0.75rem',
                  backgroundColor: '#f3f4f6',
                  color: '#374151',
                  border: 'none',
                  borderRadius: '0.375rem',
                  fontSize: '0.75rem',
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
                onMouseOver={(e) => e.target.style.backgroundColor = '#e5e7eb'}
                onMouseOut={(e) => e.target.style.backgroundColor = '#f3f4f6'}
              >
                💡 {suggestion}
              </button>
            ))}
          </div>
        )}

        {/* Input Area */}
        <div style={styles.inputArea}>
          <form onSubmit={sendMessage} style={styles.inputForm}>
            <input
              ref={inputRef}
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask me anything about farming, soil, or crops..."
              style={{
                ...styles.messageInput,
                ...(isSending ? { opacity: 0.7 } : {})
              }}
              disabled={isSending}
              onFocus={(e) => e.target.style.borderColor = '#059669'}
              onBlur={(e) => e.target.style.borderColor = '#d1d5db'}
            />
            <button
              type="submit"
              disabled={!inputMessage.trim() || isSending}
              style={{
                ...styles.sendBtn,
                ...(!inputMessage.trim() || isSending ? styles.disabledBtn : {})
              }}
              onMouseOver={(e) => {
                if (!e.target.disabled) {
                  e.target.style.backgroundColor = '#047857';
                }
              }}
              onMouseOut={(e) => {
                if (!e.target.disabled) {
                  e.target.style.backgroundColor = '#059669';
                }
              }}
            >
              {isSending ? (
                <div style={styles.loadingSpinner}></div>
              ) : (
                '🚀'
              )}
            </button>
          </form>
          <p style={styles.disclaimer}>
            Terra Bot can make mistakes. Verify important farming decisions with local experts.
          </p>
        </div>
      </div>

      <style>
        {`
          @keyframes spin {
            to { transform: rotate(360deg); }
          }
        `}
      </style>
    </div>
  );
};

export default Chatbot;
