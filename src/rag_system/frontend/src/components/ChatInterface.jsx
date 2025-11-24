import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatInterface.css';

// Determine API base URL based on environment
const API_BASE_URL = process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8001';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'Hello! I\'m your Domain Expert assistant. Ask me anything about history, science, literature, or any domain you\'ve trained me on. I\'ll provide answers based on verified sources with citations.',
      sources: []
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue
    };

    // Add user message to chat
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send request to API
      // In production (Docker), API is on the same host
      // In development, we use the configured API base URL
      const apiUrl = process.env.NODE_ENV === 'production' ? '/query' : `${API_BASE_URL}/query`;
      const response = await axios.post(apiUrl, {
        query: inputValue
      });

      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.data.answer,
        sources: response.data.sources
      };

      // Add assistant message to chat
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      let errorMessageContent = "Sorry, I encountered an error. Please try again later.";
      
      if (error.response) {
        // Server responded with error status
        errorMessageContent = `Server error: ${error.response.status} - ${error.response.statusText}`;
      } else if (error.request) {
        // Request was made but no response received
        errorMessageContent = "Network error: Could not connect to the server. Please make sure the RAG API is running.";
      } else {
        // Something else happened
        errorMessageContent = `Error: ${error.message}`;
      }
      
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: errorMessageContent,
        sources: []
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleExampleQuery = (query) => {
    setInputValue(query);
    setTimeout(() => {
      handleSendMessage();
    }, 100);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="header-content">
          <div className="logo">
            <i className="fas fa-robot"></i>
            <h1>RAG Domain Expert</h1>
          </div>
          <div className="header-info">
            <span className="status-indicator online"></span>
            <span className="status-text">Online</span>
          </div>
        </div>
      </div>

      <div className="chat-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.role}-message`}>
            <div className="message-header">
              {message.role === 'user' ? (
                <i className="fas fa-user"></i>
              ) : (
                <i className="fas fa-robot"></i>
              )}
              <span className="message-sender">
                {message.role === 'user' ? 'You' : 'Domain Expert'}
              </span>
            </div>
            <div className="message-content">
              {message.content}
            </div>
            {message.sources && message.sources.length > 0 && message.role === 'assistant' && (
              <div className="sources">
                <h4>Sources:</h4>
                <div className="source-list">
                  {message.sources.map((source, index) => (
                    <span key={index} className="source-tag">
                      {source.title}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="message assistant-message">
            <div className="message-header">
              <i className="fas fa-robot"></i>
              <span className="message-sender">Domain Expert</span>
            </div>
            <div className="typing-indicator">
              <span>Thinking</span>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
            </div>
          </div>
        )}

        {messages.length === 1 && (
          <div className="welcome-message">
            <h2><i className="fas fa-comments"></i> Domain Expert Chat</h2>
            <p>Ask me anything about history, science, literature, or any domain you've trained me on. I'll provide answers based on verified sources with citations.</p>
            <p>Try asking questions like:</p>
            <div className="example-queries">
              <div 
                className="example-query" 
                onClick={() => handleExampleQuery('Who led the Salt Satyagraha in 1930 and why was it important?')}
              >
                Who led the Salt Satyagraha in 1930?
              </div>
              <div 
                className="example-query" 
                onClick={() => handleExampleQuery('What was the purpose of the Salt March?')}
              >
                What was the purpose of the Salt March?
              </div>
              <div 
                className="example-query" 
                onClick={() => handleExampleQuery('When did India gain independence?')}
              >
                When did India gain independence?
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <div className="input-wrapper">
          <textarea
            className="chat-input"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about your domain..."
            disabled={isLoading}
            rows="1"
          />
          <button
            className="send-button"
            onClick={handleSendMessage}
            disabled={isLoading || !inputValue.trim()}
          >
            <i className={`fas ${isLoading ? 'fa-spinner fa-spin' : 'fa-paper-plane'}`}></i>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;