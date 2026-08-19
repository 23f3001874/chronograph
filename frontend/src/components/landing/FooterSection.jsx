import React from 'react';
import { Activity, ExternalLink } from 'lucide-react';

export default function FooterSection() {
  return (
    <footer style={{ background: '#000000', borderTop: '1px solid #141822', padding: '4rem 0 2rem 0' }}>
      <div className="section-container" style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr', gap: '3rem' }}>
        
        {/* BRAND COLUMN */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ background: '#3B82F6', padding: '0.5rem', borderRadius: '8px' }}>
              <Activity size={18} color="#FFFFFF" />
            </div>
            <span style={{ fontSize: '1.375rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif" }}>CHRONOGRAPH</span>
          </div>

          <p style={{ fontSize: '0.875rem', color: '#94A3B8', maxWidth: '360px', lineHeight: '1.6' }}>
            Temporal belief infrastructure for AI. Turning raw memories into versioned beliefs with evidence, lineage, contradiction detection, and explicit uncertainty.
          </p>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#34D399' }}>
            <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#34D399', boxShadow: '0 0 8px #34D399' }}></span>
            <span>SYSTEM OPERATIONAL • VERCEL DEPLOYED</span>
          </div>
        </div>

        {/* RESOURCE LINKS */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <span className="mono-tag" style={{ color: '#FFFFFF' }}>RESOURCES</span>
          <a href="https://github.com/23f3001874/chronograph" target="_blank" rel="noopener noreferrer" style={{ color: '#94A3B8', fontSize: '0.875rem', textDecoration: 'none', transition: 'color 0.2s' }}>
            GitHub Repository
          </a>
          <a href="https://hydradb.com/" target="_blank" rel="noopener noreferrer" style={{ color: '#94A3B8', fontSize: '0.875rem', textDecoration: 'none', transition: 'color 0.2s' }}>
            HydraDB Cloud
          </a>
          <a href="https://chronograph-seven.vercel.app/" target="_blank" rel="noopener noreferrer" style={{ color: '#94A3B8', fontSize: '0.875rem', textDecoration: 'none', transition: 'color 0.2s' }}>
            Vercel Production URL
          </a>
        </div>

        {/* PROJECT LINKS */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <span className="mono-tag" style={{ color: '#FFFFFF' }}>HACK HYDRA</span>
          <span style={{ color: '#94A3B8', fontSize: '0.875rem' }}>Track 3: Memory & Context</span>
          <span style={{ color: '#94A3B8', fontSize: '0.875rem' }}>Version v1.1.0</span>
          <span style={{ color: '#94A3B8', fontSize: '0.875rem' }}>104 Pytest Tests</span>
        </div>

        {/* COPYRIGHT */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <span className="mono-tag" style={{ color: '#FFFFFF' }}>LEGAL</span>
          <span style={{ color: '#64748B', fontSize: '0.8125rem' }}>
            © 2026 ChronoGraph Team. Released for Hack Hydra 2026.
          </span>
        </div>

      </div>
    </footer>
  );
}
