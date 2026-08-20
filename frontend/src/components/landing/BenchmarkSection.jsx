import React from 'react';
import BenchmarkChart from '../graphics/BenchmarkChart';

export default function BenchmarkSection() {
  const benchmarkStats = [
    { label: 'Overall Benchmark Accuracy', naive: '30%', chronograph: '100%', diff: '+70%' },
    { label: 'Future Knowledge Leakage', naive: '40% (LEAKED)', chronograph: '0% (SECURE)', diff: '-40%' },
    { label: 'Contradiction Detection', naive: '0%', chronograph: '100%', diff: '+100%' },
    { label: 'UNKNOWN Abstention Acc.', naive: '0%', chronograph: '100%', diff: '+100%' },
    { label: 'Cancellation Accuracy', naive: '0%', chronograph: '100%', diff: '+100%' },
    { label: 'Lineage Graph Integrity', naive: '0%', chronograph: '100%', diff: '+100%' },
  ];

  return (
    <section id="benchmarks" style={{ padding: '6rem 0 4rem 0', background: '#05070C', borderTop: '1px solid #141A24' }}>
      <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '3.5rem' }}>
        
        {/* Section Header */}
        <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.875rem', alignItems: 'center' }}>
          <span className="mono-tag" style={{ color: '#FF7A18' }}>
            QUANTITATIVE BENCHMARK AUDIT
          </span>
          <h2 style={{ fontSize: '3rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
            Temporal reasoning changes the answer.
          </h2>
          <p style={{ fontSize: '1.125rem', color: '#8B95A5', maxWidth: '720px', lineHeight: '1.6' }}>
            Audited across 10 controlled benchmark scenarios and 104+ automated tests. ChronoGraph achieved 100% accuracy while naive vector retrieval collapsed to 30%.
          </p>
        </div>

        {/* Clean Visual Comparison Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem' }}>
          {benchmarkStats.map((stat, idx) => (
            <div key={idx} style={{ background: '#080C12', border: '1px solid #1F2838', borderRadius: '14px', padding: '1.75rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <span style={{ fontSize: '0.875rem', fontWeight: '700', color: '#FFFFFF' }}>{stat.label}</span>
              
              <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginTop: '0.5rem' }}>
                <div>
                  <span style={{ fontSize: '0.75rem', color: '#5A6474', fontFamily: "'JetBrains Mono', monospace" }}>NAIVE:</span>
                  <div style={{ fontSize: '1.5rem', fontWeight: '800', color: '#FF4D5E' }}>{stat.naive}</div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <span style={{ fontSize: '0.75rem', color: '#FF9F43', fontFamily: "'JetBrains Mono', monospace" }}>CHRONOGRAPH:</span>
                  <div style={{ fontSize: '2rem', fontWeight: '800', color: '#35D07F' }}>{stat.chronograph}</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Benchmark Accuracy Curve Chart */}
        <div style={{ marginTop: '1rem' }}>
          <BenchmarkChart />
        </div>

        {/* Technical Benchmark Qualification Banner */}
        <div style={{ background: '#070A10', border: '1px solid #1F2838', borderRadius: '12px', padding: '1.25rem', textAlign: 'center', fontSize: '0.8125rem', fontFamily: "'JetBrains Mono', monospace", color: '#8B95A5' }}>
          * Evaluated on 10 controlled synthetic benchmark scenarios created specifically to audit point-in-time resolution, future leakage, contradiction detection, and epistemic abstention.
        </div>

      </div>
    </section>
  );
}
