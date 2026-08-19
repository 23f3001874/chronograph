import React from 'react';

export default function EditorialMetricsSection() {
  return (
    <section style={{ display: 'flex', flexDirection: 'column', gap: '2.5rem', width: '100%', maxWidth: '1200px', margin: '4rem auto 2rem auto', textAlign: 'center' }}>
      
      {/* Section Header */}
      <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.75rem', alignItems: 'center' }}>
        <span style={{ color: '#00F0FF', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8125rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
          QUANTITATIVE PROOF
        </span>
        <h2 style={{ fontSize: '2.75rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.04em', color: '#FFFFFF' }}>
          Empirical Benchmark Performance
        </h2>
        <p style={{ fontSize: '1.0625rem', color: '#94A3B8', maxWidth: '700px', lineHeight: '1.6' }}>
          ChronoGraph was falsification-audited across 10 controlled temporal scenarios and 104+ automated tests with 0 benchmark failures.
        </p>
      </div>

      {/* Massive Editorial Numbers Display */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '2rem', marginTop: '1rem' }}>
        
        {/* Metric 1: 100% Accuracy */}
        <div style={{ background: '#05070B', border: '1px solid #1F2430', borderRadius: '16px', padding: '2.5rem 1.5rem', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ fontSize: '5rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", color: '#3B82F6', lineHeight: '0.9', letterSpacing: '-0.05em' }}>
            100%
          </div>
          <div style={{ fontSize: '1.125rem', fontWeight: '700', color: '#FFFFFF', letterSpacing: '-0.01em', marginTop: '0.5rem' }}>
            CHRONOGRAPH ACCURACY
          </div>
          <p style={{ fontSize: '0.875rem', color: '#94A3B8', lineHeight: '1.5' }}>
            Resolved 10/10 temporal scenarios correctly without a single error.
          </p>
        </div>

        {/* Metric 2: 30% Naive Baseline */}
        <div style={{ background: '#05070B', border: '1px solid #1F2430', borderRadius: '16px', padding: '2.5rem 1.5rem', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ fontSize: '5rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", color: '#F87171', lineHeight: '0.9', letterSpacing: '-0.05em' }}>
            30%
          </div>
          <div style={{ fontSize: '1.125rem', fontWeight: '700', color: '#FFFFFF', letterSpacing: '-0.01em', marginTop: '0.5rem' }}>
            NAIVE MEMORY BASELINE
          </div>
          <p style={{ fontSize: '0.875rem', color: '#94A3B8', lineHeight: '1.5' }}>
            Conventional vector retrieval failed 7/10 scenarios due to recency bias.
          </p>
        </div>

        {/* Metric 3: 0% Future Leakage */}
        <div style={{ background: '#05070B', border: '1px solid #1F2430', borderRadius: '16px', padding: '2.5rem 1.5rem', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ fontSize: '5rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", color: '#00F0FF', lineHeight: '0.9', letterSpacing: '-0.05em' }}>
            0%
          </div>
          <div style={{ fontSize: '1.125rem', fontWeight: '700', color: '#FFFFFF', letterSpacing: '-0.01em', marginTop: '0.5rem' }}>
            FUTURE KNOWLEDGE LEAKAGE
          </div>
          <p style={{ fontSize: '0.875rem', color: '#94A3B8', lineHeight: '1.5' }}>
            Zero future facts leaked into past queries (vs 40% in naive vector retrieval).
          </p>
        </div>

        {/* Metric 4: 100% Contradiction Detection */}
        <div style={{ background: '#05070B', border: '1px solid #1F2430', borderRadius: '16px', padding: '2.5rem 1.5rem', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ fontSize: '5rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", color: '#F87171', lineHeight: '0.9', letterSpacing: '-0.05em' }}>
            100%
          </div>
          <div style={{ fontSize: '1.125rem', fontWeight: '700', color: '#FFFFFF', letterSpacing: '-0.01em', marginTop: '0.5rem' }}>
            CONTRADICTION DETECTION
          </div>
          <p style={{ fontSize: '0.875rem', color: '#94A3B8', lineHeight: '1.5' }}>
            Flags simultaneous active conflicts (CONFLICTED) without arbitrary picking.
          </p>
        </div>

        {/* Metric 5: 100% Unknown Abstention */}
        <div style={{ background: '#05070B', border: '1px solid #1F2430', borderRadius: '16px', padding: '2.5rem 1.5rem', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ fontSize: '5rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", color: '#FBBF24', lineHeight: '0.9', letterSpacing: '-0.05em' }}>
            100%
          </div>
          <div style={{ fontSize: '1.125rem', fontWeight: '700', color: '#FFFFFF', letterSpacing: '-0.01em', marginTop: '0.5rem' }}>
            UNKNOWN ABSTENTION
          </div>
          <p style={{ fontSize: '0.875rem', color: '#94A3B8', lineHeight: '1.5' }}>
            Refrains from hallucinating fallback values when evidence is absent (0.0 conf).
          </p>
        </div>

        {/* Metric 6: 100% Lineage Integrity */}
        <div style={{ background: '#05070B', border: '1px solid #1F2430', borderRadius: '16px', padding: '2.5rem 1.5rem', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ fontSize: '5rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", color: '#34D399', lineHeight: '0.9', letterSpacing: '-0.05em' }}>
            100%
          </div>
          <div style={{ fontSize: '1.125rem', fontWeight: '700', color: '#FFFFFF', letterSpacing: '-0.01em', marginTop: '0.5rem' }}>
            LINEAGE INTEGRITY
          </div>
          <p style={{ fontSize: '0.875rem', color: '#94A3B8', lineHeight: '1.5' }}>
            100% cycle-safe graph traversal for grounded evidence auditability.
          </p>
        </div>

      </div>
    </section>
  );
}
