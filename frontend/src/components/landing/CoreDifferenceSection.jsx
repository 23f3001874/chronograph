import React from 'react';
import { XCircle, CheckCircle2, ShieldAlert, Zap } from 'lucide-react';

export default function CoreDifferenceSection() {
  const comparisonRows = [
    {
      feature: 'Temporal Resolution Mechanism',
      naive: 'Recency Bias (Latest chunk wins)',
      chronograph: 'Point-in-Time Validity Intervals [valid_from, valid_until)',
      naiveSuccess: false,
    },
    {
      feature: 'Future Knowledge Leakage',
      naive: 'High Leakage Rate (40% leakage on historical queries)',
      chronograph: 'Zero Future Leakage (0% leakage guaranteed)',
      naiveSuccess: false,
    },
    {
      feature: 'Handling Missing Facts / Absent Evidence',
      naive: 'Fabricates / Guesses fallback values (0% UNKNOWN)',
      chronograph: 'Deterministic Epistemic Abstention (UNKNOWN, 0.0 confidence)',
      naiveSuccess: false,
    },
    {
      feature: 'Simultaneous Active Contradictions',
      naive: 'Silently picks an arbitrary winner',
      chronograph: 'Flags Active Contradiction State (CONFLICTED, 0.5 confidence)',
      naiveSuccess: false,
    },
    {
      feature: 'Belief Supersession & Reversion',
      naive: 'Overwrites past context or mixes historical states',
      chronograph: 'Formal Versioned State Machine (v1 → v2 → v3)',
      naiveSuccess: false,
    },
    {
      feature: 'Evidence Grounding & Lineage Traversal',
      naive: 'No grounded observation links or lineage history',
      chronograph: 'Full Cycle-Safe Evidence Graph (GROUNDED_IN, SUPERSEDES)',
      naiveSuccess: false,
    }
  ];

  return (
    <section style={{ padding: '6rem 0 4rem 0', background: '#000000', borderTop: '1px solid #141822' }}>
      <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
        
        {/* Section Header */}
        <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.875rem', alignItems: 'center' }}>
          <span className="mono-tag" style={{ color: '#00F0FF' }}>
            ARCHITECTURAL COMPARISON
          </span>
          <h2 style={{ fontSize: '3rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
            Naive Memory vs ChronoGraph Engine
          </h2>
          <p style={{ fontSize: '1.125rem', color: '#94A3B8', maxWidth: '720px', lineHeight: '1.6' }}>
            Why simple text retrieval fails when preferences shift, facts contradict, or temporal queries are requested.
          </p>
        </div>

        {/* High-Impact Comparison Table / Matrix */}
        <div style={{ border: '1px solid #1F2430', borderRadius: '16px', overflow: 'hidden', background: '#05070C' }}>
          
          {/* Table Header */}
          <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr 1fr', background: '#090C14', borderBottom: '1px solid #1F2430', padding: '1.25rem 1.75rem', fontSize: '0.8125rem', fontFamily: "'JetBrains Mono', monospace", fontWeight: '700', textTransform: 'uppercase' }}>
            <span style={{ color: '#94A3B8' }}>CAPABILITY</span>
            <span style={{ color: '#F87171', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <XCircle size={16} color="#F87171" />
              NAIVE MEMORY RAG
            </span>
            <span style={{ color: '#00F0FF', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <CheckCircle2 size={16} color="#00F0FF" />
              CHRONOGRAPH ENGINE
            </span>
          </div>

          {/* Table Rows */}
          {comparisonRows.map((row, idx) => (
            <div
              key={idx}
              style={{
                display: 'grid', gridTemplateColumns: '1.2fr 1fr 1fr', padding: '1.25rem 1.75rem',
                borderBottom: idx < comparisonRows.length - 1 ? '1px solid #141822' : 'none',
                alignItems: 'center', background: idx % 2 === 0 ? '#05070C' : '#030408'
              }}
            >
              <div style={{ fontSize: '0.9375rem', fontWeight: '700', color: '#FFFFFF', paddingRight: '1rem' }}>
                {row.feature}
              </div>

              <div style={{ fontSize: '0.875rem', color: '#F87171', paddingRight: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ opacity: 0.7 }}>•</span>
                {row.naive}
              </div>

              <div style={{ fontSize: '0.875rem', color: '#00F0FF', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <CheckCircle2 size={16} color="#34D399" style={{ flexShrink: 0 }} />
                {row.chronograph}
              </div>
            </div>
          ))}

        </div>

      </div>
    </section>
  );
}
