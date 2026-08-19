import React, { useState } from 'react';
import { ArrowRight, Play, CheckCircle2, Clock, GitBranch, ArrowDown, ShieldCheck } from 'lucide-react';

export default function HeroSection({ onExploreGraph }) {
  const [sliderIndex, setSliderIndex] = useState(0); // 0: Jan 20, 1: Feb 20, 2: Mar 20

  const timeStates = [
    {
      date: 'Jan 20, 2025',
      isoDate: '2025-01-20T00:00:00Z',
      value: 'VS Code',
      status: 'SUPPORTED',
      confidence: '0.90',
      reason: 'Observed assertion "I use VS Code for development" is valid.',
      badgeColor: '#3B82F6',
      nodes: [
        { date: 'Jan 20', value: 'VS Code', status: 'SUPPORTED', conf: '0.90', active: true },
        { date: 'Feb 20', value: 'Cursor', status: 'FUTURE FACT (LOCKED)', conf: '0.00', active: false },
        { date: 'Mar 20', value: 'VS Code', status: 'FUTURE FACT (LOCKED)', conf: '0.00', active: false },
      ]
    },
    {
      date: 'Feb 20, 2025',
      isoDate: '2025-02-20T00:00:00Z',
      value: 'Cursor',
      status: 'SUPPORTED',
      confidence: '0.90',
      reason: 'Observed assertion "I switched to Cursor" supersedes prior VS Code belief.',
      badgeColor: '#00F0FF',
      nodes: [
        { date: 'Jan 20', value: 'VS Code', status: 'SUPERSEDED', conf: '0.00', active: false },
        { date: 'Feb 20', value: 'Cursor', status: 'SUPPORTED', conf: '0.90', active: true },
        { date: 'Mar 20', value: 'VS Code', status: 'FUTURE FACT (LOCKED)', conf: '0.00', active: false },
      ]
    },
    {
      date: 'Mar 20, 2025',
      isoDate: '2025-03-20T00:00:00Z',
      value: 'VS Code',
      status: 'SUPPORTED',
      confidence: '0.95',
      reason: 'Observed assertion "I switched back to VS Code" supersedes Cursor belief.',
      badgeColor: '#34D399',
      nodes: [
        { date: 'Jan 20', value: 'VS Code', status: 'SUPERSEDED', conf: '0.00', active: false },
        { date: 'Feb 20', value: 'Cursor', status: 'SUPERSEDED', conf: '0.00', active: false },
        { date: 'Mar 20', value: 'VS Code', status: 'ACTIVE', conf: '0.95', active: true },
      ]
    }
  ];

  const currentState = timeStates[sliderIndex];

  return (
    <section style={{ padding: '5rem 0 3rem 0', position: 'relative' }}>
      
      {/* Subtle Background Glow */}
      <div style={{
        position: 'absolute', top: '10%', right: '5%', width: '500px', height: '400px',
        background: 'radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.08) 0%, transparent 70%)',
        pointerEvents: 'none', zIndex: 0
      }} />

      <div className="section-container" style={{ position: 'relative', zIndex: 1, display: 'grid', gridTemplateColumns: '1.1fr 1fr', gap: '3.5rem', alignItems: 'center' }}>
        
        {/* LEFT COLUMN: EDITORIAL HEADLINE */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem', textAlign: 'left' }}>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
            <span className="mono-tag" style={{ color: '#00F0FF', background: 'rgba(0, 240, 255, 0.1)', padding: '0.2rem 0.6rem', borderRadius: '4px', border: '1px solid rgba(0, 240, 255, 0.25)' }}>
              TEMPORAL BELIEF INFRASTRUCTURE FOR AI
            </span>
          </div>

          <h1 style={{ fontSize: '4.25rem', fontWeight: '800', lineHeight: '1.02', letterSpacing: '-0.04em', fontFamily: "'Space Grotesk', sans-serif" }}>
            AI memory should know <br />
            <span style={{ background: 'linear-gradient(135deg, #FFFFFF 0%, #3B82F6 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              what was true.
            </span>
          </h1>

          <p style={{ fontSize: '1.125rem', color: '#94A3B8', lineHeight: '1.65', maxWidth: '580px' }}>
            ChronoGraph is a temporal belief engine built on <strong style={{ color: '#FFFFFF' }}>HydraDB Cloud</strong>. It reconstructs what an AI should believe at any point in time — without leaking future knowledge or inventing answers.
          </p>

          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '0.5rem' }}>
            <button className="btn-infrastructure btn-infrastructure-primary" style={{ padding: '0.875rem 1.75rem', fontSize: '1rem' }} onClick={onExploreGraph}>
              Explore the Graph
              <ArrowRight size={18} />
            </button>
            <a href="https://github.com/23f3001874/chronograph" target="_blank" rel="noopener noreferrer" className="btn-infrastructure btn-infrastructure-secondary" style={{ padding: '0.875rem 1.5rem', fontSize: '1rem' }}>
              View on GitHub
            </a>
          </div>

          {/* Substrate Tag */}
          <div style={{ fontSize: '0.78125rem', fontFamily: "'JetBrains Mono', monospace", color: '#64748B', display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem' }}>
            <span>Built for Hack Hydra 2026</span>
            <span>•</span>
            <span style={{ color: '#60A5FA' }}>HydraDB Cloud Substrate</span>
          </div>

        </div>

        {/* RIGHT COLUMN: LIVE ANIMATED BELIEF GRAPH & TIME MACHINE SLIDER */}
        <div style={{ background: '#05070B', border: '1px solid #1F2430', borderRadius: '16px', padding: '1.75rem', display: 'flex', flexDirection: 'column', gap: '1.5rem', boxShadow: '0 20px 50px rgba(0,0,0,0.6)' }}>
          
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #1A1D24', paddingBottom: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Clock size={16} color="#00F0FF" />
              <span style={{ fontSize: '0.8125rem', fontFamily: "'JetBrains Mono', monospace", color: '#00F0FF', fontWeight: '700', textTransform: 'uppercase' }}>
                LIVE TEMPORAL BELIEF RECONSTRUCTION
              </span>
            </div>
            <span style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#34D399', background: 'rgba(52, 211, 153, 0.15)', padding: '0.15rem 0.5rem', borderRadius: '4px' }}>
              POINT-IN-TIME RESOLVED
            </span>
          </div>

          {/* Animated Belief Stack */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {currentState.nodes.map((node, idx) => (
              <React.Fragment key={idx}>
                
                <div style={{
                  background: node.active ? 'rgba(59, 130, 246, 0.12)' : '#080A0F',
                  border: node.active ? '1px solid #3B82F6' : '1px solid #1A1D24',
                  borderRadius: '10px', padding: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                  transition: 'all 0.3s ease', opacity: node.status.includes('LOCKED') ? 0.4 : 1
                }}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                    <div style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#94A3B8' }}>
                      DATE: {node.date}
                    </div>
                    <div style={{ fontSize: '1.125rem', fontWeight: '800', color: node.active ? '#FFFFFF' : '#64748B' }}>
                      "{node.value}"
                    </div>
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.25rem' }}>
                    <span style={{
                      fontSize: '0.6875rem', fontFamily: "'JetBrains Mono', monospace", fontWeight: '700',
                      color: node.active ? '#34D399' : (node.status === 'SUPERSEDED' ? '#FBBF24' : '#64748B'),
                      background: node.active ? 'rgba(52, 211, 153, 0.15)' : 'rgba(255,255,255,0.05)',
                      padding: '0.15rem 0.5rem', borderRadius: '4px'
                    }}>
                      {node.status}
                    </span>
                    <span style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#60A5FA' }}>
                      CONF: {node.conf}
                    </span>
                  </div>
                </div>

                {idx < currentState.nodes.length - 1 && (
                  <div style={{ display: 'flex', justifyContent: 'center', opacity: 0.5 }}>
                    <ArrowDown size={14} color="#60A5FA" />
                  </div>
                )}

              </React.Fragment>
            ))}
          </div>

          {/* TIME MACHINE SLIDER MICRO-INTERACTION */}
          <div style={{ background: '#080C14', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: '12px', padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#94A3B8' }}>
              <span>TIME MACHINE SLIDER:</span>
              <span style={{ color: '#00F0FF', fontWeight: '700' }}>T = {currentState.date}</span>
            </div>

            <input
              type="range"
              min="0"
              max="2"
              step="1"
              value={sliderIndex}
              onChange={(e) => setSliderIndex(parseInt(e.target.value))}
              style={{ width: '100%', cursor: 'pointer', accentColor: '#00F0FF' }}
            />

            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.6875rem', fontFamily: "'JetBrains Mono', monospace", color: '#64748B' }}>
              <span style={{ color: sliderIndex === 0 ? '#3B82F6' : '#64748B', fontWeight: sliderIndex === 0 ? '700' : '400' }}>JAN 20 (VS Code)</span>
              <span style={{ color: sliderIndex === 1 ? '#00F0FF' : '#64748B', fontWeight: sliderIndex === 1 ? '700' : '400' }}>FEB 20 (Cursor)</span>
              <span style={{ color: sliderIndex === 2 ? '#34D399' : '#64748B', fontWeight: sliderIndex === 2 ? '700' : '400' }}>MAR 20 (VS Code)</span>
            </div>

            {/* Resolved Active State Output Box */}
            <div style={{ background: '#030509', border: '1px solid #1E3A8A', borderRadius: '8px', padding: '0.75rem 1rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <span style={{ fontSize: '0.6875rem', color: '#94A3B8', fontFamily: "'JetBrains Mono', monospace" }}>Resolved Value at T:</span>
                <div style={{ fontSize: '1rem', fontWeight: '800', color: '#FFFFFF' }}>{currentState.value}</div>
              </div>
              <div style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#34D399', fontWeight: '700' }}>
                Confidence {currentState.confidence}
              </div>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}
