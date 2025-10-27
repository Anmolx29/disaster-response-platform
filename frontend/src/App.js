import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>🚨 Disaster Response Platform</h1>
        <p>AI-Powered Emergency Management System</p>
        <div style={{ marginTop: '2rem' }}>
          <button style={{ margin: '0.5rem', padding: '1rem 2rem', fontSize: '1rem' }}>
            View Incidents
          </button>
          <button style={{ margin: '0.5rem', padding: '1rem 2rem', fontSize: '1rem' }}>
            AI Predictions
          </button>
          <button style={{ margin: '0.5rem', padding: '1rem 2rem', fontSize: '1rem' }}>
            Send Alerts
          </button>
        </div>
      </header>
    </div>
  );
}

export default App;
