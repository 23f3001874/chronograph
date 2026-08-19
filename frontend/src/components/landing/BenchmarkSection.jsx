import React from 'react';
import BenchmarkChart from '../graphics/BenchmarkChart';

export default function BenchmarkSection() {
  const benchmarkStats = [
    { label: 'Overall Benchmark Accuracy', naive: '30%', chronograph: '100%', diff: '+70%' },
    { label: 'Future Knowledge Leakage', naive: '40% (LEAKED)', chronograph: '0% (SECURE)', diff: '-40%' },
    { label: 'Contradiction Detection', naive: '0%', chronograph: '100%', diff: '+100%' },
    { label: 'UNKNOWN Abstention Accuracy', naive: '0%', chronograph: '100%', diff: '+100%' },
    { label: 'Cancellation Accuracy', naive: '0%', chronograph: '100%', diff: '+100%' },
    { label: 'Lineage Graph Integrity', naive: '0%', chronograph: '100%', diff: '+100%' },
  ];

  return (
    <section id="benchmarks" style={{ padding: '6rem 0 4rem 0', background: '#020306', borderTop: '1px solid #141822' }}>
      <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '3.5rem' }}>
        
        {/* Section Header */}
        <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.875rem', alignItems: 'center' }}>
          <span className="mono-tag" style={{ color: '#00F0FF' }}>
            QUANTITATIVE EMPIRICAL AUDIT
          </span>
          <h2 style={{ fontSize: '3rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
            Temporal reasoning changes the answer.
          </h2>
          <p style={{ fontSize: '1.125rem', color: '#94A3B8', maxWidth: '720px', lineHeight: '1.6' }}>
            Audited across 10 controlled benchmark scenarios and 104+ automated tests. ChronoGraph achieved 100% accuracy while naive vector retrieval collapsed to 30%.
          </p>
        </div>

        {/* Big Comparison Table / Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem' }}>
          {benchmarkStats.map((stat, idx) => (
            <div key={idx} style={{ background: '#06080F', border: '1px solid #1F2430', borderRadius: '14px', padding: '1.75rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <span style={{ fontSize: '0.875rem', fontWeight: '700', color: '#FFFFFF' }}>{stat.label}</span>
              
              <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginTop: '0.5rem' }}>
                <div>
                  <span style={{ fontSize: '0.75rem', color: '#64748B', fontFamily: "'JetBrains Mono', monospace" }}>NAIVE:</span>
                  <div style={{ fontSize: '1.5rem', fontWeight: '800', color: '#F87171' }}>{stat.naive}</div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <span style={{ fontSize: '0.75rem', color: '#60A5FA', fontFamily: "'JetBrains Mono', monospace" }}>CHRONOGRAPH:</span>
                  <div style={{ fontSize: '2rem', fontWeight: '800', color: '#34D399' }}>{stat.chronograph}</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Visual Accuracy Curve Chart Component */}
        <div style={{ marginTop: '1rem' }}>
          <BenchmarkChart />
        </div>

        {/* TECHNICAL METRICS STRIP */}
        <div style={{ background: '#05070D', border: '1px solid #1F2430', borderRadius: '14px', padding: '1.5rem 2rem', display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '1.5rem', textAlign: 'center' }}>
          <div>
            <div style={{ fontSize: '1.75rem', fontWeight: '800', color: '#3B82F6', fontFamily: "'Space Grotesk', sans-serif" }}>104+</div>
            <div style={{ fontSize: '0.75rem', color: '#94A3B8', fontFamily: "'JetBrains Mono', monospace", marginTop: '0.2rem' }}>Pytest Tests Passed</div>
          </div>
          <div>
            <div style={{ fontSize: '1.75rem', fontWeight: '800', color: '#00F0FF', fontFamily: "'Space Grotesk', sans-serif" }}>0%</div>
            <div style={{ fontSize: '0.75rem', color: '#94A3B8', fontFamily: "'JetBrains Mono', monospace", marginTop: '0.2rem' }}>Future Leakage</div>
          </div>
          <div>
            <div style={{ fontSize: '1.75rem', fontWeight: '800', color: '#34D399', fontFamily: "'Space Grotesk', sans-serif" }}>10 / 10</div>
            <div style={{ fontSize: '0.75rem', color: '#94A3B8', fontFamily: "'JetBrains Mono', monospace", marginTop: '0.2rem' }}>Scenarios Passed</div>
          </div>
          <div>
            <div style={{ fontSize: '1.75rem', fontWeight: '800', color: '#FBBF24', fontFamily: "'Space Grotesk', sans-serif" }}>0</div>
            <div style={{ fontSize: '0.75rem', color: '#94A3B8', fontFamily: "'JetBrains Mono', monospace", marginTop: '0.2rem' }}>Secrets Exposed</div>
          </div>
          <div>
            <div style={{ fontSize: '1.75rem', fontWeight: '800', color: '#34D399', fontFamily: "'Space Grotesk', sans-serif" }}>~0.09 ms</div>
            <div style={{ fontSize: '0.75rem', color: '#94A3B8', fontFamily: "'JetBrains Mono', monospace", marginTop: '0.2rem' }}>Resolution Latency</div>
          </div>
        </div>

      </div>
    </section>
  );
}
