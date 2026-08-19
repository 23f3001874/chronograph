import React from 'react';

export default function BenchmarkChart() {
  return (
    <div style={{ width: '100%', height: '280px', background: '#05070B', border: '1px solid #1F2430', borderRadius: '12px', padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ fontSize: '0.75rem', fontFamily: 'monospace', color: '#94A3B8', fontWeight: '700', textTransform: 'uppercase' }}>
          ACCURACY % OVER TIMELINE STEPS & CONTEXT DRIFT
        </span>
        <div style={{ display: 'flex', gap: '1.25rem', fontSize: '0.75rem', fontFamily: 'monospace' }}>
          <span style={{ color: '#3B82F6', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
            <span style={{ width: '10px', height: '10px', background: '#3B82F6', borderRadius: '2px' }}></span>
            ChronoGraph (100.0%)
          </span>
          <span style={{ color: '#F87171', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
            <span style={{ width: '10px', height: '10px', background: '#F87171', borderRadius: '2px' }}></span>
            Naive Vector Retrieval (30.0%)
          </span>
        </div>
      </div>

      <svg width="100%" height="200" viewBox="0 0 600 200" fill="none" xmlns="http://www.w3.org/2000/svg">
        
        {/* Y Axis Grid Lines */}
        <line x1="40" y1="20" x2="580" y2="20" stroke="#1F2430" strokeWidth="1" strokeDasharray="3 3" />
        <text x="10" y="24" fill="#64748B" fontSize="10" fontFamily="monospace">100%</text>

        <line x1="40" y1="65" x2="580" y2="65" stroke="#1F2430" strokeWidth="1" strokeDasharray="3 3" />
        <text x="10" y="69" fill="#64748B" fontSize="10" fontFamily="monospace">75%</text>

        <line x1="40" y1="110" x2="580" y2="110" stroke="#1F2430" strokeWidth="1" strokeDasharray="3 3" />
        <text x="10" y="114" fill="#64748B" fontSize="10" fontFamily="monospace">50%</text>

        <line x1="40" y1="155" x2="580" y2="155" stroke="#1F2430" strokeWidth="1" strokeDasharray="3 3" />
        <text x="10" y="159" fill="#64748B" fontSize="10" fontFamily="monospace">25%</text>

        {/* X Axis Labels */}
        <text x="40" y="185" fill="#64748B" fontSize="10" fontFamily="monospace">Step 1</text>
        <text x="175" y="185" fill="#64748B" fontSize="10" fontFamily="monospace">Step 3 (Supersede)</text>
        <text x="330" y="185" fill="#64748B" fontSize="10" fontFamily="monospace">Step 6 (Conflict)</text>
        <text x="475" y="185" fill="#64748B" fontSize="10" fontFamily="monospace">Step 10 (Abstain)</text>

        {/* ChronoGraph Flat 100% Accuracy Line */}
        <path d="M40 20 L175 20 L330 20 L475 20 L570 20" stroke="#3B82F6" strokeWidth="3" fill="none" />
        <circle cx="175" cy="20" r="5" fill="#00F0FF" />
        <circle cx="330" cy="20" r="5" fill="#00F0FF" />
        <circle cx="475" cy="20" r="5" fill="#00F0FF" />
        <circle cx="570" cy="20" r="5" fill="#00F0FF" />
        <text x="530" y="14" fill="#00F0FF" fontSize="11" fontFamily="monospace" fontWeight="bold">100.0%</text>

        {/* Naive Baseline Degradation Curve (100% -> 70% -> 45% -> 30%) */}
        <path d="M40 20 C140 30 175 75 330 115 C420 135 475 145 570 146" stroke="#F87171" strokeWidth="3" strokeDasharray="4 4" fill="none" />
        <circle cx="570" cy="146" r="5" fill="#F87171" />
        <text x="530" y="165" fill="#F87171" fontSize="11" fontFamily="monospace" fontWeight="bold">30.0%</text>

      </svg>
    </div>
  );
}
