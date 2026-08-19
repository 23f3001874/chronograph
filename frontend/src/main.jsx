import React, { Component, StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Uncaught error in ChronoGraph:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '3rem', background: '#000000', color: '#FFFFFF', textAlign: 'center', fontFamily: 'sans-serif' }}>
          <h1 style={{ color: '#F87171' }}>ChronoGraph UI Initialization Error</h1>
          <pre style={{ color: '#94A3B8', marginTop: '1rem', background: '#0D1017', padding: '1rem', borderRadius: '8px', textAlign: 'left', overflow: 'auto' }}>
            {this.state.error?.toString()}
          </pre>
          <button style={{ marginTop: '1.5rem', padding: '0.5rem 1.5rem', background: '#3B82F6', color: '#FFF', border: 'none', borderRadius: '6px', cursor: 'pointer' }} onClick={() => window.location.reload()}>
            Reload Application
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
)
