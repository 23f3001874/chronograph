import React from 'react';
import { Activity, GitFork, ExternalLink } from 'lucide-react';

export default function HeaderNav({ healthStatus, onLaunchDemo }) {
  const scrollTo = (id) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <header style={{
      position: 'sticky', top: 0, zIndex: 100,
      background: 'rgba(0, 0, 0, 0.85)',
      backdropFilter: 'blur(12px)',
      borderBottom: '1px solid #141822',
      padding: '0.875rem 2rem'
    }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        
        {/* BRAND LOGO */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem', cursor: 'pointer' }} onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
          <div style={{ background: '#3B82F6', padding: '0.45rem', borderRadius: '8px', display: 'flex', boxShadow: '0 0 16px rgba(59, 130, 246, 0.5)' }}>
            <Activity size={18} color="#FFFFFF" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
              <span style={{ fontSize: '1.25rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.02em', color: '#FFFFFF' }}>
                CHRONOGRAPH
              </span>
              <span style={{ fontSize: '0.6875rem', fontFamily: "'JetBrains Mono', monospace", background: 'rgba(59, 130, 246, 0.15)', color: '#60A5FA', padding: '0.125rem 0.5rem', borderRadius: '4px', border: '1px solid rgba(59, 130, 246, 0.3)' }}>
                v1.1.0
              </span>
            </div>
            <p style={{ fontSize: '0.6875rem', fontFamily: "'JetBrains Mono', monospace", color: '#64748B', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              TEMPORAL BELIEF ENGINE
            </p>
          </div>
        </div>

        {/* NAVIGATION LINKS */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
          <button style={{ background: 'none', border: 'none', color: '#94A3B8', fontSize: '0.875rem', fontWeight: '500', cursor: 'pointer', transition: 'color 0.2s' }} onClick={() => scrollTo('how-it-works')}>
            How it works
          </button>
          <button style={{ background: 'none', border: 'none', color: '#94A3B8', fontSize: '0.875rem', fontWeight: '500', cursor: 'pointer', transition: 'color 0.2s' }} onClick={() => scrollTo('belief-graph')}>
            Graph
          </button>
          <button style={{ background: 'none', border: 'none', color: '#94A3B8', fontSize: '0.875rem', fontWeight: '500', cursor: 'pointer', transition: 'color 0.2s' }} onClick={() => scrollTo('benchmarks')}>
            Benchmarks
          </button>
          <button style={{ background: 'none', border: 'none', color: '#94A3B8', fontSize: '0.875rem', fontWeight: '500', cursor: 'pointer', transition: 'color 0.2s' }} onClick={() => scrollTo('architecture')}>
            Architecture
          </button>
          <a href="https://github.com/23f3001874/chronograph" target="_blank" rel="noopener noreferrer" style={{ color: '#94A3B8', fontSize: '0.875rem', fontWeight: '500', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <GitFork size={14} />
            GitHub
          </a>
        </nav>

        {/* STATUS & CTA */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: healthStatus === 'ok' ? '#34D399' : '#F87171' }}>
            <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: healthStatus === 'ok' ? '#34D399' : '#F87171', boxShadow: healthStatus === 'ok' ? '0 0 8px #34D399' : '0 0 8px #F87171' }}></span>
            <span>{healthStatus === 'ok' ? 'OPERATIONAL' : 'OFFLINE'}</span>
          </div>

          <button className="btn-infrastructure btn-infrastructure-primary" style={{ padding: '0.5rem 1.125rem', fontSize: '0.8125rem' }} onClick={onLaunchDemo}>
            Launch Demo
          </button>
        </div>

      </div>
    </header>
  );
}
