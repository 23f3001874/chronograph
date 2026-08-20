import React, { useState } from 'react';
import { ArrowRight, Clock, ArrowDown, ShieldCheck } from 'lucide-react';

export default function HeroSection({ onExploreGraph }) {
  const [sliderIndex, setSliderIndex] = useState(0); // 0: Jan 20, 1: Feb 20, 2: Mar 20

  const timeStates = [
    {
      date: 'Jan 20, 2025',
      value: 'VS Code',
      status: 'SUPPORTED',
      confidence: '0.90',
      nodes: [
        { id: 'B1', date: 'Jan 20', value: 'VS Code', status: 'SUPPORTED', conf: '0.90', active: true },
        { id: 'B2', date: 'Feb 20', value: 'Cursor', status: 'FUTURE FACT (LOCKED)', conf: '0.00', active: false },
        { id: 'B3', date: 'Mar 20', value: 'VS Code', status: 'FUTURE FACT (LOCKED)', conf: '0.00', active: false },
      ]
    },
    {
      date: 'Feb 20, 2025',
      value: 'Cursor',
      status: 'SUPPORTED',
      confidence: '0.90',
      nodes: [
        { id: 'B1', date: 'Jan 20', value: 'VS Code', status: 'SUPERSEDED', conf: '0.00', active: false },
        { id: 'B2', date: 'Feb 20', value: 'Cursor', status: 'SUPPORTED', conf: '0.90', active: true },
        { id: 'B3', date: 'Mar 20', value: 'VS Code', status: 'FUTURE FACT (LOCKED)', conf: '0.00', active: false },
      ]
    },
    {
      date: 'Mar 20, 2025',
      value: 'VS Code',
      status: 'ACTIVE',
      confidence: '0.95',
      nodes: [
        { id: 'B1', date: 'Jan 20', value: 'VS Code', status: 'SUPERSEDED', conf: '0.00', active: false },
        { id: 'B2', date: 'Feb 20', value: 'Cursor', status: 'SUPERSEDED', conf: '0.00', active: false },
        { id: 'B3', date: 'Mar 20', value: 'VS Code', status: 'ACTIVE', conf: '0.95', active: true },
      ]
    }
  ];

  const currentState = timeStates[sliderIndex];

  return (
    <section style={{ padding: '5.5rem 0 3.5rem 0', position: 'relative' }} className="bg-grid-pattern">
      
      {/* Background Radial Glow */}
      <div style={{
        position: 'absolute', top: '15%', right: '5%', width: '550px', height: '420px',
        background: 'radial-gradient(circle at 50% 50%, rgba(255, 122, 24, 0.12) 0%, transparent 70%)',
        pointerEvents: 'none', zIndex: 0
      }} />

      <div className="section-container" style={{ position: 'relative', zIndex: 1, display: 'grid', gridTemplateColumns: '1.15fr 1fr', gap: '3.5rem', alignItems: 'center' }}>
        
        {/* LEFT COLUMN: HERO HEADLINE & COPY */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem', textAlign: 'left' }}>
          
          {/* Status Line */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#8B95A5' }}>
            <span style={{ color: '#35D07F', display: 'flex', alignItems: 'center', gap: '0.35rem', fontWeight: '700' }}>
              <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#35D07F', boxShadow: '0 0 8px #35D07F' }}></span>
              LIVE
            </span>
            <span>|</span>
            <span>HydraDB Connected</span>
            <span>|</span>
            <span>Temporal Engine Ready</span>
          </div>

          <h1 style={{ fontSize: '4.25rem', fontWeight: '800', lineHeight: '1.05', letterSpacing: '-0.04em', fontFamily: "'Space Grotesk', sans-serif" }}>
            AI memory should <br />
            <span style={{ background: 'linear-gradient(135deg, #FFFFFF 0%, #FF9F43 60%, #FF7A18 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              know what was true.
            </span>
          </h1>

          <p style={{ fontSize: '1.125rem', color: '#8B95A5', lineHeight: '1.65', maxWidth: '580px' }}>
            ChronoGraph turns raw memories into temporally versioned beliefs — with evidence, lineage, contradiction detection, and explicit uncertainty.
          </p>

          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '0.5rem' }}>
            <button className="btn-infrastructure btn-infrastructure-primary" style={{ padding: '0.875rem 1.75rem', fontSize: '1rem' }} onClick={onExploreGraph}>
              Try Live Demo
              <ArrowRight size={18} />
            </button>
            <a href="https://github.com/23f3001874/chronograph" target="_blank" rel="noopener noreferrer" className="btn-infrastructure btn-infrastructure-secondary" style={{ padding: '0.875rem 1.5rem', fontSize: '1rem' }}>
              View on GitHub
            </a>
          </div>

          <div style={{ fontSize: '0.78125rem', fontFamily: "'JetBrains Mono', monospace", color: '#5A6474', display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem' }}>
            <span>Built for Hack Hydra 2026</span>
            <span>•</span>
            <span style={{ color: '#FF9F43' }}>Track 03 — Memory & Context Retrieval</span>
          </div>

        </div>

        {/* RIGHT COLUMN: TECHNICAL VISUALIZATION & TIME MACHINE SLIDER */}
        <div style={{ background: '#070A10', border: '1px solid #1F2838', borderRadius: '16px', padding: '1.75rem', display: 'flex', flexDirection: 'column', gap: '1.5rem', boxShadow: '0 20px 50px rgba(0,0,0,0.7)' }}>
          
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #141A24', paddingBottom: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Clock size={16} color="#FF7A18" />
              <span style={{ fontSize: '0.8125rem', fontFamily: "'JetBrains Mono', monospace", color: '#FF9F43', fontWeight: '700', textTransform: 'uppercase' }}>
                TEMPORAL STATE MACHINE VISUALIZATION
              </span>
            </div>
            <span style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#35D07F', background: 'rgba(53, 208, 127, 0.15)', padding: '0.15rem 0.5rem', borderRadius: '4px' }}>
              RESOLVED AT T
            </span>
          </div>

          {/* Observation Anchor */}
          <div style={{ background: '#0B0F18', border: '1px solid #1F2838', borderRadius: '8px', padding: '0.75rem 1rem', fontSize: '0.78125rem', fontFamily: "'JetBrains Mono', monospace" }}>
            <span style={{ color: '#8B95A5' }}>OBSERVATION: </span>
            <span style={{ color: '#F5F7FA', fontStyle: 'italic' }}>"I switched back to VS Code."</span>
          </div>

          {/* Animated Belief Stack */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
            {currentState.nodes.map((node, idx) => (
              <React.Fragment key={idx}>
                
                <div style={{
                  background: node.active ? 'rgba(255, 122, 24, 0.12)' : '#080C12',
                  border: node.active ? '1px solid #FF7A18' : '1px solid #141A24',
                  borderRadius: '10px', padding: '0.875rem 1rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                  transition: 'all 0.3s ease', opacity: node.status.includes('LOCKED') ? 0.4 : 1
                }}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.2rem' }}>
                    <div style={{ fontSize: '0.6875rem', fontFamily: "'JetBrains Mono', monospace", color: '#8B95A5' }}>
                      BELIEF {node.id} • {node.date}
                    </div>
                    <div style={{ fontSize: '1rem', fontWeight: '800', color: node.active ? '#FFFFFF' : '#5A6474' }}>
                      "{node.value}"
                    </div>
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.2rem' }}>
                    <span style={{
                      fontSize: '0.6875rem', fontFamily: "'JetBrains Mono', monospace", fontWeight: '700',
                      color: node.active ? '#35D07F' : (node.status === 'SUPERSEDED' ? '#FF9F43' : '#5A6474'),
                      background: node.active ? 'rgba(53, 208, 127, 0.15)' : 'rgba(255,255,255,0.04)',
                      padding: '0.15rem 0.5rem', borderRadius: '4px'
                    }}>
                      {node.status}
                    </span>
                    <span style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#00D9FF' }}>
                      CONF: {node.conf}
                    </span>
                  </div>
                </div>

                {idx < currentState.nodes.length - 1 && (
                  <div style={{ display: 'flex', justifyContent: 'center', opacity: 0.5 }}>
                    <ArrowDown size={14} color="#FF9F43" />
                  </div>
                )}

              </React.Fragment>
            ))}
          </div>

          {/* TIME MACHINE SLIDER MICRO-INTERACTION */}
          <div style={{ background: '#090E16', border: '1px solid rgba(255, 122, 24, 0.3)', borderRadius: '12px', padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#8B95A5' }}>
              <span>TIME SLIDER RESOLUTION:</span>
              <span style={{ color: '#FF7A18', fontWeight: '700' }}>T = {currentState.date}</span>
            </div>

            <input
              type="range"
              min="0"
              max="2"
              step="1"
              value={sliderIndex}
              onChange={(e) => setSliderIndex(parseInt(e.target.value))}
              style={{ width: '100%', cursor: 'pointer', accentColor: '#FF7A18' }}
            />

            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.6875rem', fontFamily: "'JetBrains Mono', monospace", color: '#5A6474' }}>
              <span style={{ color: sliderIndex === 0 ? '#FF7A18' : '#5A6474', fontWeight: sliderIndex === 0 ? '700' : '400' }}>JAN 20 (VS Code)</span>
              <span style={{ color: sliderIndex === 1 ? '#00D9FF' : '#5A6474', fontWeight: sliderIndex === 1 ? '700' : '400' }}>FEB 20 (Cursor)</span>
              <span style={{ color: sliderIndex === 2 ? '#35D07F' : '#5A6474', fontWeight: sliderIndex === 2 ? '700' : '400' }}>MAR 20 (VS Code)</span>
            </div>

            {/* Resolved Active State Output Box */}
            <div style={{ background: '#04060A', border: '1px solid #FF7A18', borderRadius: '8px', padding: '0.75rem 1rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <span style={{ fontSize: '0.6875rem', color: '#8B95A5', fontFamily: "'JetBrains Mono', monospace" }}>Resolved Answer at T:</span>
                <div style={{ fontSize: '1rem', fontWeight: '800', color: '#FFFFFF' }}>{currentState.value}</div>
              </div>
              <div style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#35D07F', fontWeight: '700' }}>
                {currentState.status} ({currentState.confidence})
              </div>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}
