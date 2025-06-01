import React, { useState } from 'react';
import './QueryInterface.css';

const QueryInterface = () => {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [answer, setAnswer] = useState('');
  const [showAnswer, setShowAnswer] = useState(false);

  // Actual API call
  const processQuery = async (queryText) => {
    const response = await fetch('http://localhost:8000/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: queryText }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();

    let formattedAnswer = data.answer || 'No answer returned.';
    if (data.top_results && data.top_results.length > 0) {
        formattedAnswer += '\n\nTop Results:\n'; // keep the text part

        // Instead of joining with newline, render links separately in JSX:
        // For example, inside your React component render method or return block:

        return (
            <div>
            <p>{formattedAnswer}</p>
            <ul>
                {data.top_results.map((link, index) => (
                <li key={index} style={{ marginBottom: '10px' }}>
                    <a href={link} target="_blank" rel="noopener noreferrer">
                    {link}
                    </a>
                </li>
                ))}
            </ul>
            </div>
        );
    }

    return formattedAnswer;
  };

  const handleSendQuery = async () => {
    const trimmedQuery = query.trim();

    if (!trimmedQuery) {
      return;
    }

    setIsLoading(true);
    setShowAnswer(false);

    try {
      const result = await processQuery(trimmedQuery);
      setAnswer(result);
      setShowAnswer(true);
    } catch (error) {
      setAnswer(`Error processing query: ${error.message}`);
      setShowAnswer(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !isLoading) {
      handleSendQuery();
    }
  };

  const clearResults = () => {
    setAnswer('');
    setShowAnswer(false);
    setQuery('');
  };

  return (
    <div className="query-interface">
      <div className="container">
        <div className="header">
          <h1>Query Interface</h1>
          <p>Enter your question and get instant answers</p>
        </div>

        <div className="query-form">
          <div className="input-group">
            <input 
              type="text" 
              className="query-input" 
              placeholder="Enter your query here..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
            />
            <button 
              className="send-btn" 
              onClick={handleSendQuery}
              disabled={!query.trim() || isLoading}
            >
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </div>
        </div>

        {isLoading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <div className="loading-text">Processing your query...</div>
          </div>
        )}

        {showAnswer && !isLoading && (
          <div className="answer-container">
            <div className="answer-label">Answer</div>
            <div className="answer-text">{answer}</div>
            <button className="clear-btn" onClick={clearResults}>
              Clear Results
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default QueryInterface;
