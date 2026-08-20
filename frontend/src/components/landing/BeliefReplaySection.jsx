import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, Clock, ShieldCheck } from 'lucide-react';

export default function BeliefReplaySection() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [step, setStep] = useState(0);

  const replaySteps = [
    {
      date: 'JAN 20, 2025',
      timeLabel: 't0 (Jan 1 - Feb 1)',
      value: 'VS Code',
      status: 'SUPPORTED',
      confidence: '0.90',
      nodeState: { B1: 'ACTIVE', B2: 'INACTIVE', B3: 'INACTIVE' },
      explanation: 'User initial editor preference ingested and validated at t0.'
    },
    {
      date: 'FEB 20, 2025',
      timeLabel: 't1 (Feb 1 - Mar 1)',
      value: 'Cursor',
      status: 'SUPPORTED',
      confidence: '0.90',
      nodeState: { B1: 'SUPERSEDED', B2: 'ACTIVE', B3: 'INACTIVE' },
      explanation: 'User switched to Cursor. B2 supersedes B1 for interval [Feb 1, Mar 1).'
    },
    {
      date: 'MAR 20, 2025',
      timeLabel: 't2 (Mar 1 - ∞)',
      value: 'VS Code',
      status: 'ACTIVE',
      confidence: '0.95',
      nodeState: { B1: 'SUPERSEDED', B2: 'SUPERSEDED', B3: 'ACTIVE' },
      explanation: 'User switched back to VS Code. B3 supersedes B2 for interval [Mar 1, ∞).'
    }
  ];

  useEffect(() => {
    let timer;
    if (isPlaying) {
      timer = setInterval(() => {
        setStep((prev) => (prev + 1) % replaySteps.length);
      }, 2200);
    }
    return () => clearInterval(timer);
  }, [isPlaying]);

  const current = replaySteps[step];

  return (
    <section style={{ padding: '6rem 0 4rem 0', background: '#05070C', borderTop: '1px solid #141A24' }}>
      <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
        
        {/* Header */}
        <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.875rem', alignItems: 'center' }}>
          <span className="mono-tag" style={{ color: '#FF7A18' }}>
            CINEMATIC REPLAY CONTROLLER
          </span>
          <h2 style={{ fontSize: '3rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
            PLAY MEMORY
          </h2>
          <p style={{ fontSize: '1.125rem', color: '#8B95A5', maxWidth: '720px', lineHeight: '1.6' }}>
            Watch ChronoGraph reconstruct entity belief transitions chronologically across time.
          </p>
        </div>

        {/* Playback Console Container */}
        <div style={{ background: '#070A10', border: '1px solid #1F2838', borderRadius: '16px', padding: '2.5rem', display: 'flex', flexDirection: 'column', gap: '2rem', boxShadow: '0 20px 50px rgba(0,0,0,0.6)' }}>
          
          {/* Controls Header */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #141A24', paddingBottom: '1.25rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <button
                className="btn-infrastructure btn-infrastructure-primary"
                style={{ padding: '0.625rem 1.25rem' }}
                onClick={() => setIsPlaying(!isPlaying)}
              >
                {isPlaying ? <Pause size={16} /> : <Play size={16} />}
                {isPlaying ? 'Pause Memory Playback' : 'Play Memory Evolution'}
              </button>

              <button
                className="btn-infrastructure btn-infrastructure-secondary"
                style={{ padding: '0.625rem 1rem' }}
                onClick={() => { setStep(0); setIsPlaying(false); }}
              >
                <RotateCcw size={16} />
                Reset
              </button>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8125rem', color: '#FF9F43' }}>
              <Clock size={16} />
              <span>TIMESTAMP T: {current.date}</span>
            </div>
          </div>

          {/* Nodes Evolution Replay */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem' }}>
            
            {/* B1 NODE */}
            <div style={{
              background: current.nodeState.B1 === 'ACTIVE' ? 'rgba(53, 208, 127, 0.12)' : (current.nodeState.B1 === 'SUPERSEDED' ? '#080C12' : '#040508'),
              border: current.nodeState.B1 === 'ACTIVE' ? '1px solid #35D07F' : (current.nodeState.B1 === 'SUPERSEDED' ? '1px solid #FF9F43' : '1px solid #141A24'),
              borderRadius: '14px', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.75rem', transition: 'all 0.4s ease',
              opacity: current.nodeState.B1 === 'INACTIVE' ? 0.35 : 1
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace" }}>
                <span style={{ color: '#8B95A5' }}>BELIEF B1</span>
                <span style={{
                  color: current.nodeState.B1 === 'ACTIVE' ? '#35D07F' : (current.nodeState.B1 === 'SUPERSEDED' ? '#FF9F43' : '#5A6474'),
                  background: current.nodeState.B1 === 'ACTIVE' ? 'rgba(53, 208, 127, 0.15)' : 'rgba(255,255,255,0.04)',
                  padding: '0.15rem 0.5rem', borderRadius: '4px', fontWeight: '700'
                }}>
                  {current.nodeState.B1}
                </span>
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: '800', color: '#FFFFFF' }}>"VS Code"</div>
              <div style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#5A6474' }}>[Jan 1, 2025 - Feb 1, 2025)</div>
            </div>

            {/* B2 NODE */}
            <div style={{
              background: current.nodeState.B2 === 'ACTIVE' ? 'rgba(53, 208, 127, 0.12)' : (current.nodeState.B2 === 'SUPERSEDED' ? '#080C12' : '#040508'),
              border: current.nodeState.B2 === 'ACTIVE' ? '1px solid #35D07F' : (current.nodeState.B2 === 'SUPERSEDED' ? '1px solid #FF9F43' : '1px solid #141A24'),
              borderRadius: '14px', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.75rem', transition: 'all 0.4s ease',
              opacity: current.nodeState.B2 === 'INACTIVE' ? 0.35 : 1
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace" }}>
                <span style={{ color: '#8B95A5' }}>BELIEF B2</span>
                <span style={{
                  color: current.nodeState.B2 === 'ACTIVE' ? '#35D07F' : (current.nodeState.B2 === 'SUPERSEDED' ? '#FF9F43' : '#5A6474'),
                  background: current.nodeState.B2 === 'ACTIVE' ? 'rgba(53, 208, 127, 0.15)' : 'rgba(255,255,255,0.04)',
                  padding: '0.15rem 0.5rem', borderRadius: '4px', fontWeight: '700'
                }}>
                  {current.nodeState.B2}
                </span>
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: '800', color: '#FFFFFF' }}>"Cursor"</div>
              <div style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#5A6474' }}>[Feb 1, 2025 - Mar 1, 2025)</div>
            </div>

            {/* B3 NODE */}
            <div style={{
              background: current.nodeState.B3 === 'ACTIVE' ? 'rgba(53, 208, 127, 0.12)' : (current.nodeState.B3 === 'SUPERSEDED' ? '#080C12' : '#040508'),
              border: current.nodeState.B3 === 'ACTIVE' ? '1px solid #35D07F' : (current.nodeState.B3 === 'SUPERSEDED' ? '1px solid #FF9F43' : '1px solid #141A24'),
              borderRadius: '14px', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.75rem', transition: 'all 0.4s ease',
              opacity: current.nodeState.B3 === 'INACTIVE' ? 0.35 : 1
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace" }}>
                <span style={{ color: '#8B95A5' }}>BELIEF B3</span>
                <span style={{
                  color: current.nodeState.B3 === 'ACTIVE' ? '#35D07F' : (current.nodeState.B3 === 'SUPERSEDED' ? '#FF9F43' : '#5A6474'),
                  background: current.nodeState.B3 === 'ACTIVE' ? 'rgba(53, 208, 127, 0.15)' : 'rgba(255,255,255,0.04)',
                  padding: '0.15rem 0.5rem', borderRadius: '4px', fontWeight: '700'
                }}>
                  {current.nodeState.B3}
                </span>
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: '800', color: '#FFFFFF' }}>"VS Code"</div>
              <div style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#5A6474' }}>[Mar 1, 2025 - ∞)</div>
            </div>

          </div>

          {/* Current Step Explanation Box */}
          <div style={{ background: '#04060A', border: '1px solid #FF7A18', borderRadius: '12px', padding: '1.25rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <span style={{ fontSize: '0.6875rem', color: '#8B95A5', fontFamily: "'JetBrains Mono', monospace" }}>RESOLVED STATE AT {current.date}:</span>
              <div style={{ fontSize: '1.125rem', fontWeight: '800', color: '#FFFFFF', marginTop: '0.2rem' }}>
                Answer: "{current.value}" ({current.status})
              </div>
              <p style={{ fontSize: '0.8125rem', color: '#8B95A5', marginTop: '0.25rem' }}>{current.explanation}</p>
            </div>
            <div style={{ fontSize: '1rem', fontWeight: '800', fontFamily: "'JetBrains Mono', monospace", color: '#35D07F' }}>
              CONF: {current.confidence}
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}
