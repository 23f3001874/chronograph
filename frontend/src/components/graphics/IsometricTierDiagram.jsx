import React from 'react';

export default function IsometricTierDiagram() {
  return (
    <div style={{ width: '100%', height: '180px', background: '#05070B', border: '1px solid #1F2430', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative', overflow: 'hidden' }}>
      
      {/* Background Iso Grid */}
      <svg width="100%" height="100%" viewBox="0 0 400 180" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g opacity="0.3">
          <path d="M 0 90 L 200 0 L 400 90 L 200 180 Z" stroke="#1F2430" strokeWidth="1" fill="none" />
          <path d="M 50 90 L 200 25 L 350 90 L 200 155 Z" stroke="#1F2430" strokeWidth="1" fill="none" />
          <path d="M 100 90 L 200 45 L 300 90 L 200 135 Z" stroke="#1F2430" strokeWidth="1" fill="none" />
        </g>

        {/* Isometric Diamond Cards */}
        {/* Tier 1: In Memory */}
        <g transform="translate(60, 60)">
          <polygon points="40,0 80,20 40,40 0,20" fill="#0B0F19" stroke="#3B82F6" strokeWidth="1.5" />
          <text x="40" y="24" fill="#FFFFFF" fontSize="10" fontFamily="monospace" textAnchor="middle" fontWeight="bold">Memory Chunk</text>
        </g>

        <line x1="140" y1="80" x2="170" y2="80" stroke="#3B82F6" strokeWidth="2" strokeDasharray="3 3" />

        {/* Tier 2: Validity Interval [valid_from, valid_until) */}
        <g transform="translate(170, 60)">
          <polygon points="40,0 80,20 40,40 0,20" fill="rgba(59, 130, 246, 0.25)" stroke="#00F0FF" strokeWidth="2" />
          <text x="40" y="24" fill="#00F0FF" fontSize="10" fontFamily="monospace" textAnchor="middle" fontWeight="bold">[valid_from, valid_until)</text>
        </g>

        <line x1="250" y1="80" x2="280" y2="80" stroke="#00F0FF" strokeWidth="2" strokeDasharray="3 3" />

        {/* Tier 3: Point-in-Time Resolution (T) */}
        <g transform="translate(280, 60)">
          <polygon points="40,0 80,20 40,40 0,20" fill="#0B0F19" stroke="#34D399" strokeWidth="1.5" />
          <text x="40" y="24" fill="#34D399" fontSize="10" fontFamily="monospace" textAnchor="middle" fontWeight="bold">Resolved (T)</text>
        </g>
      </svg>
    </div>
  );
}
