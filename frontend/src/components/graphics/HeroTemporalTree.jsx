import React from 'react';

export default function HeroTemporalTree() {
  return (
    <div style={{ position: 'relative', width: '100%', maxWidth: '520px', height: '360px', background: '#000000', border: '1px solid #2E2E2E', borderRadius: '12px', overflow: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      
      {/* Background Radial Glow */}
      <div style={{
        position: 'absolute', inset: 0,
        background: 'radial-gradient(circle at 70% 70%, rgba(59, 130, 246, 0.12) 0%, transparent 60%)',
        pointerEvents: 'none'
      }} />

      {/* SVG Tree & Node Canvas */}
      <svg width="100%" height="100%" viewBox="0 0 500 340" fill="none" xmlns="http://www.w3.org/2000/svg">
        
        {/* Fine Dark Grid Lines */}
        <defs>
          <pattern id="cleanGrid" width="25" height="25" patternUnits="userSpaceOnUse">
            <path d="M 25 0 L 0 0 0 25" fill="none" stroke="#1A1D24" strokeWidth="0.75" />
          </pattern>
          <linearGradient id="cyberBlue" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#1D4ED8" />
            <stop offset="50%" stopColor="#3B82F6" />
            <stop offset="100%" stopColor="#00F0FF" />
          </linearGradient>
        </defs>
        <rect width="500" height="340" fill="url(#cleanGrid)" />

        {/* Crisp Tree Branches */}
        <path d="M250 320 L250 240 C250 200 170 170 120 140 C80 115 50 80 40 40" stroke="url(#cyberBlue)" strokeWidth="2.5" />
        <path d="M250 240 C250 180 330 150 380 120 C420 95 450 60 460 30" stroke="url(#cyberBlue)" strokeWidth="2.5" />
        <path d="M250 190 L250 110 C250 80 275 55 295 30" stroke="url(#cyberBlue)" strokeWidth="2" strokeDasharray="3 3" />

        {/* Node 1: Root Ingestion */}
        <rect x="244" y="312" width="12" height="12" fill="#3B82F6" rx="2" />
        <text x="265" y="322" fill="#94A3B8" fontSize="10" fontFamily="'JetBrains Mono', monospace">Ingestion (t0)</text>

        {/* Node 2: Active State */}
        <rect x="114" y="134" width="12" height="12" fill="#34D399" rx="2" />
        <text x="50" y="132" fill="#34D399" fontSize="10" fontFamily="'JetBrains Mono', monospace" fontWeight="700">ACTIVE</text>
        <text x="50" y="145" fill="#CBD5E1" fontSize="9" fontFamily="'JetBrains Mono', monospace">VS Code</text>

        {/* Node 3: Superseded State */}
        <rect x="374" y="114" width="12" height="12" fill="#FBBF24" rx="2" />
        <text x="395" y="112" fill="#FBBF24" fontSize="10" fontFamily="'JetBrains Mono', monospace" fontWeight="700">SUPERSEDED</text>
        <text x="395" y="125" fill="#CBD5E1" fontSize="9" fontFamily="'JetBrains Mono', monospace">Cursor</text>

        {/* Node 4: Conflicted State */}
        <rect x="244" y="104" width="12" height="12" fill="#F87171" rx="2" />
        <text x="265" y="98" fill="#F87171" fontSize="10" fontFamily="'JetBrains Mono', monospace" fontWeight="700">CONFLICTED</text>
        <text x="265" y="111" fill="#CBD5E1" fontSize="9" fontFamily="'JetBrains Mono', monospace">Location</text>

        {/* Node 5: Unknown Abstention */}
        <rect x="34" y="34" width="12" height="12" fill="#64748B" rx="2" />
        <text x="52" y="44" fill="#94A3B8" fontSize="10" fontFamily="'JetBrains Mono', monospace">UNKNOWN</text>

        {/* Minimal Bounding Crosshair (HydraDB Signature) */}
        <g stroke="#00F0FF" strokeWidth="0.75" opacity="0.6">
          <line x1="104" y1="124" x2="136" y2="156" />
          <line x1="136" y1="124" x2="104" y2="156" />
          <rect x="104" y="124" width="32" height="32" fill="none" stroke="#00F0FF" strokeDasharray="2 2" />
        </g>

        <g stroke="#FBBF24" strokeWidth="0.75" opacity="0.6">
          <line x1="364" y1="104" x2="396" y2="136" />
          <line x1="396" y1="104" x2="364" y2="136" />
          <rect x="364" y="104" width="32" height="32" fill="none" stroke="#FBBF24" strokeDasharray="2 2" />
        </g>

      </svg>
    </div>
  );
}
