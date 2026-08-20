import React from 'react';
import { GitFork } from 'lucide-react';

// Custom Sleek ChronoGraph Node/Graph Logo Icon
function ChronoGraphLogoIcon() {
  return (
    <svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="26" height="26" rx="7" fill="url(#logoGlow)" />
      <path d="M6 13C6 9.13401 9.13401 6 13 6C16.866 6 20 9.13401 20 13" stroke="#FFFFFF" strokeWidth="1.5" strokeDasharray="2 2" opacity="0.6" />
      <path d="M7 16L11 11L15 15L19 9" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="7" cy="16" r="2" fill="#FF7A18" stroke="#FFFFFF" strokeWidth="1.5" />
      <circle cx="11" cy="11" r="2" fill="#00D9FF" stroke="#FFFFFF" strokeWidth="1.5" />
      <circle cx="15" cy="15" r="2" fill="#FF9F43" stroke="#FFFFFF" strokeWidth="1.5" />
      <circle cx="19" cy="9" r="2" fill="#35D07F" stroke="#FFFFFF" strokeWidth="1.5" />
      <defs>
        <linearGradient id="logoGlow" x1="0" y1="0" x2="26" y2="26" gradientUnits="userSpaceOnUse">
          <stop stopColor="#FF7A18" />
          <stop offset="1" stopColor="#E66000" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export default function HeaderNav({ healthStatus, onLaunchDemo }) {
  const scrollTo = (id) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <header style={{
      position: 'sticky', top: 0, zIndex: 100,
      background: 'rgba(4, 5, 8, 0.92)',
      backdropFilter: 'blur(16px)',
      borderBottom: '1px solid #141A24',
      padding: '0.75rem 2rem'
    }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        
        {/* BRAND LOGO WITHOUT VERSION BADGE */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem', cursor: 'pointer' }} onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
          <div style={{ display: 'flex', filter: 'drop-shadow(0 0 10px rgba(255, 122, 24, 0.6))' }}>
            <ChronoGraphLogoIcon />
          </div>
          <div>
            <span style={{ fontSize: '1.25rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.02em', color: '#FFFFFF', display: 'block' }}>
              ChronoGraph
            </span>
            <p style={{ fontSize: '0.625rem', fontFamily: "'JetBrains Mono', monospace", color: '#8B95A5', textTransform: 'uppercase', letterSpacing: '0.06em', marginTop: '-1px' }}>
              TEMPORAL INTELLIGENCE INFRASTRUCTURE
            </p>
          </div>
        </div>

        {/* DYNAMIC DYNAMIC HOVER NAVIGATION BUTTONS */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <button className="nav-link-item" onClick={() => scrollTo('why-chronograph')}>
            Product
          </button>
          <button className="nav-link-item" onClick={() => scrollTo('how-it-works')}>
            How It Works
          </button>
          <button className="nav-link-item" onClick={() => scrollTo('temporal-engine')}>
            Temporal Engine
          </button>
          <button className="nav-link-item" onClick={() => scrollTo('benchmarks')}>
            Benchmarks
          </button>
          <button className="nav-link-item" onClick={() => scrollTo('interactive-studio')}>
            Demo
          </button>
          <a href="https://github.com/23f3001874/chronograph" target="_blank" rel="noopener noreferrer" className="nav-link-item">
            <GitFork size={14} color="#FF9F43" />
            GitHub
          </a>
        </nav>

        {/* STATUS & GLOWING CTA */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: healthStatus === 'ok' ? '#35D07F' : '#FF4D5E' }}>
            <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: healthStatus === 'ok' ? '#35D07F' : '#FF4D5E', boxShadow: healthStatus === 'ok' ? '0 0 8px #35D07F' : '0 0 8px #FF4D5E' }}></span>
            <span>{healthStatus === 'ok' ? 'LIVE' : 'OFFLINE'}</span>
          </div>

          <button
            className="btn-infrastructure btn-infrastructure-primary"
            style={{
              padding: '0.55rem 1.25rem', fontSize: '0.8125rem',
              boxShadow: '0 0 20px rgba(255, 122, 24, 0.4), inset 0 0 10px rgba(255, 255, 255, 0.2)'
            }}
            onClick={onLaunchDemo}
          >
            Try Live Demo
          </button>
        </div>

      </div>
    </header>
  );
}
