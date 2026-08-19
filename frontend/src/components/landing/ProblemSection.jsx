import React from 'react';
import { XCircle, CheckCircle2, ArrowRight, ShieldAlert } from 'lucide-react';

export default function ProblemSection() {
  return (
    <section id="how-it-works" style={{ padding: '6rem 0 4rem 0', borderTop: '1px solid #141822', background: '#020305' }}>
      <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
        
        {/* Section Header */}
        <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.875rem', alignItems: 'center' }}>
          <span className="mono-tag" style={{ color: '#00F0FF' }}>
            THE TEMPORAL MEMORY PARADOX
          </span>
          <h2 style={{ fontSize: '3rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
            Memory isn't truth.
          </h2>
          <p style={{ fontSize: '1.25rem', color: '#94A3B8', maxWidth: '750px', lineHeight: '1.6' }}>
            Knowing what was said in a chat transcript isn't the same as knowing what was true at a specific point in time.
          </p>
        </div>

        {/* Visual Transformation Workflow: Raw Memories → Naive vs ChronoGraph */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2.5rem', marginTop: '1rem' }}>
          
          {/* RAW MEMORY CHUNKS */}
          <div style={{ background: '#06080D', border: '1px solid #1F2430', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #1A1D24', paddingBottom: '1rem' }}>
              <span className="mono-tag" style={{ color: '#94A3B8' }}>RAW OBSERVATIONS (INGESTED CHUNKS)</span>
              <span style={{ fontSize: '0.75rem', color: '#64748B', fontFamily: "'JetBrains Mono', monospace" }}>CHRONOLOGICAL STREAM</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8125rem' }}>
              <div style={{ padding: '0.875rem 1.125rem', background: '#0B0E17', borderLeft: '3px solid #3B82F6', borderRadius: '6px', color: '#CBD5E1' }}>
                <span style={{ color: '#60A5FA', fontWeight: '700' }}>[t0: Jan 20]</span> "I use VS Code for all my frontend development."
              </div>
              <div style={{ padding: '0.875rem 1.125rem', background: '#0B0E17', borderLeft: '3px solid #00F0FF', borderRadius: '6px', color: '#CBD5E1' }}>
                <span style={{ color: '#00F0FF', fontWeight: '700' }}>[t1: Feb 20]</span> "I switched to Cursor today for AI features."
              </div>
              <div style={{ padding: '0.875rem 1.125rem', background: '#0B0E17', borderLeft: '3px solid #34D399', borderRadius: '6px', color: '#CBD5E1' }}>
                <span style={{ color: '#34D399', fontWeight: '700' }}>[t2: Mar 20]</span> "I switched back to VS Code. It is my favorite editor."
              </div>
            </div>

            <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.08)', border: '1px solid rgba(239, 68, 68, 0.25)', borderRadius: '10px', fontSize: '0.8125rem', color: '#F87171', lineHeight: '1.5' }}>
              <strong>NAIVE RAG FAILURE:</strong> Standard vector retrieval matches keywords across all chunks without evaluating temporal validity intervals. A query at Feb 20 will retrieve the March 20 memory ("VS Code") and leak future state.
            </div>
          </div>

          {/* CHRONOGRAPH TEMPORAL BELIEF ENGINE */}
          <div style={{ background: '#040710', border: '1px solid #1E3A8A', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem', boxShadow: '0 0 35px rgba(59, 130, 246, 0.12)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #1E3A8A', paddingBottom: '1rem' }}>
              <span className="mono-tag" style={{ color: '#00F0FF' }}>CHRONOGRAPH STATE MACHINE</span>
              <span style={{ fontSize: '0.75rem', color: '#34D399', fontFamily: "'JetBrains Mono', monospace", fontWeight: '700' }}>[valid_from, valid_until)</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8125rem' }}>
              <div style={{ padding: '0.875rem 1.125rem', background: '#081226', borderLeft: '3px solid #3B82F6', borderRadius: '6px', display: 'flex', justifyContent: 'space-between' }}>
                <div>
                  <span style={{ color: '#60A5FA', fontWeight: '700' }}>BELIEF: VS Code</span>
                  <div style={{ fontSize: '0.75rem', color: '#94A3B8', marginTop: '0.2rem' }}>Status: SUPERSEDED</div>
                </div>
                <span style={{ color: '#60A5FA' }}>[Jan 20, Feb 20)</span>
              </div>

              <div style={{ padding: '0.875rem 1.125rem', background: '#081226', borderLeft: '3px solid #00F0FF', borderRadius: '6px', display: 'flex', justifyContent: 'space-between' }}>
                <div>
                  <span style={{ color: '#00F0FF', fontWeight: '700' }}>BELIEF: Cursor</span>
                  <div style={{ fontSize: '0.75rem', color: '#94A3B8', marginTop: '0.2rem' }}>Status: SUPERSEDED</div>
                </div>
                <span style={{ color: '#00F0FF' }}>[Feb 20, Mar 20)</span>
              </div>

              <div style={{ padding: '0.875rem 1.125rem', background: '#081226', borderLeft: '3px solid #34D399', borderRadius: '6px', display: 'flex', justifyContent: 'space-between' }}>
                <div>
                  <span style={{ color: '#34D399', fontWeight: '700' }}>BELIEF: VS Code</span>
                  <div style={{ fontSize: '0.75rem', color: '#34D399', marginTop: '0.2rem' }}>Status: ACTIVE (v3)</div>
                </div>
                <span style={{ color: '#34D399' }}>[Mar 20, Present)</span>
              </div>
            </div>

            <div style={{ padding: '1rem', background: 'rgba(52, 211, 153, 0.08)', border: '1px solid rgba(52, 211, 153, 0.25)', borderRadius: '10px', fontSize: '0.8125rem', color: '#34D399', lineHeight: '1.5' }}>
              <strong>CHRONOGRAPH GUARANTEE:</strong> Evaluates exact point-in-time validity at target timestamp T. Prevents future knowledge leakage with 100% mathematical certainty.
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}
