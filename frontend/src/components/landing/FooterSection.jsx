import React from 'react';
import { Activity } from 'lucide-react';

export default function FooterSection() {
  return (
    <footer style={{ background: '#040508', borderTop: '1px solid #141A24', padding: '4rem 0 2rem 0' }}>
      <div className="section-container" style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr', gap: '3rem' }}>
        
        {/* BRAND COLUMN */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ background: '#FF7A18', padding: '0.5rem', borderRadius: '8px' }}>
              <Activity size={18} color="#FFFFFF" />
            </div>
            <span style={{ fontSize: '1.375rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif" }}>ChronoGraph</span>
          </div>

          <p style={{ fontSize: '0.875rem', color: '#8B95A5', maxWidth: '360px', lineHeight: '1.6' }}>
            Temporal intelligence for graph memory. Turning raw memories into versioned beliefs with evidence, lineage, contradiction detection, and explicit uncertainty.
          </p>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#35D07F' }}>
            <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#35D07F', boxShadow: '0 0 8px #35D07F' }}></span>
            <span>SYSTEM OPERATIONAL • VERCEL DEPLOYED</span>
          </div>
        </div>

        {/* RESOURCE LINKS */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <span className="mono-tag" style={{ color: '#FFFFFF' }}>RESOURCES</span>
          <a href="https://chronograph-seven.vercel.app/" target="_blank" rel="noopener noreferrer" style={{ color: '#8B95A5', fontSize: '0.875rem', textDecoration: 'none', transition: 'color 0.2s' }}>
            Live Demo
          </a>
          <a href="https://github.com/23f3001874/chronograph" target="_blank" rel="noopener noreferrer" style={{ color: '#8B95A5', fontSize: '0.875rem', textDecoration: 'none', transition: 'color 0.2s' }}>
            GitHub Repository
          </a>
          <a href="https://hydradb.com/" target="_blank" rel="noopener noreferrer" style={{ color: '#8B95A5', fontSize: '0.875rem', textDecoration: 'none', transition: 'color 0.2s' }}>
            HydraDB Cloud
          </a>
        </div>

        {/* PROJECT LINKS */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <span className="mono-tag" style={{ color: '#FFFFFF' }}>HACK HYDRA</span>
          <span style={{ color: '#8B95A5', fontSize: '0.875rem' }}>Track 03 — Memory & Context Retrieval</span>
          <span style={{ color: '#8B95A5', fontSize: '0.875rem' }}>Version v1.1.0</span>
          <span style={{ color: '#8B95A5', fontSize: '0.875rem' }}>104 Pytest Tests</span>
        </div>

        {/* LEGAL & LICENSE */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <span className="mono-tag" style={{ color: '#FFFFFF' }}>LICENSE</span>
          <span style={{ color: '#8B95A5', fontSize: '0.875rem' }}>
            MIT Licensed
          </span>
          <span style={{ color: '#5A6474', fontSize: '0.8125rem' }}>
            © 2026 ChronoGraph Team.
          </span>
        </div>

      </div>
    </footer>
  );
}
