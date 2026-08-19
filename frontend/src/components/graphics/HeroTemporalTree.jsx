import React from 'react';

export default function HeroTemporalTree() {
  return (
    <div style={{ position: 'relative', width: '100%', maxWidth: '540px', height: '380px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      
      {/* Radial Background Blue Glow */}
      <div style={{
        position: 'absolute', inset: 0,
        background: 'radial-gradient(circle at 60% 60%, rgba(0, 240, 255, 0.15) 0%, rgba(59, 130, 246, 0.1) 40%, transparent 75%)',
        borderRadius: '20px', pointerEvents: 'none'
      }} />

      {/* SVG Canvas for Tree & Network Nodes */}
      <svg width="100%" height="100%" viewBox="0 0 500 360" fill="none" xmlns="http://www.w3.org/2000/svg">
        
        {/* Subtle Grid Lines */}
        <defs>
          <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(59, 130, 246, 0.08)" strokeWidth="1" />
          </pattern>
          <linearGradient id="blueGlow" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#2563EB" />
            <stop offset="50%" stopColor="#3B82F6" />
            <stop offset="100%" stopColor="#00F0FF" />
          </linearGradient>
        </defs>
        <rect width="500" height="360" fill="url(#grid)" />

        {/* Tree Trunk & Main Branches */}
        <path d="M250 340 L250 260 C250 220 180 190 140 160 C110 138 80 110 60 70" stroke="url(#blueGlow)" strokeWidth="3" strokeDasharray="4 4" />
        <path d="M250 260 C250 200 320 170 370 140 C410 115 440 90 460 50" stroke="url(#blueGlow)" strokeWidth="3" />
        <path d="M250 210 L250 120 C250 90 280 60 300 40" stroke="url(#blueGlow)" strokeWidth="2.5" />
        <path d="M180 190 L180 130 C180 100 140 80 120 50" stroke="url(#blueGlow)" strokeWidth="2" />
        <path d="M370 140 L370 80 C370 60 400 40 420 20" stroke="url(#blueGlow)" strokeWidth="2" />

        {/* Temporal State Nodes (Pixel Dots) */}
        {/* Node 1: Root Ingestion */}
        <rect x="242" y="328" width="16" height="16" fill="#2563EB" rx="3" />
        <text x="265" y="340" fill="#94A3B8" fontSize="10" fontFamily="monospace">Raw Ingestion (t0)</text>

        {/* Node 2: VS Code Initial */}
        <rect x="132" y="152" width="16" height="16" fill="#3B82F6" rx="3" />
        <circle cx="140" cy="160" r="12" stroke="#00F0FF" strokeWidth="1.5" strokeDasharray="3 3" />
        <text x="75" y="164" fill="#34D399" fontSize="11" fontFamily="monospace" fontWeight="bold">ACTIVE (VS Code)</text>

        {/* Node 3: Cursor Supersession */}
        <rect x="362" y="132" width="16" height="16" fill="#FBBF24" rx="3" />
        <circle cx="370" cy="140" r="14" stroke="#FBBF24" strokeWidth="1.5" />
        <text x="395" y="144" fill="#FBBF24" fontSize="11" fontFamily="monospace" fontWeight="bold">SUPERSEDED (Cursor)</text>

        {/* Node 4: Delhi vs Bangalore Contradiction */}
        <rect x="242" y="112" width="16" height="16" fill="#F87171" rx="3" />
        <circle cx="250" cy="120" r="16" stroke="#F87171" strokeWidth="2" />
        <text x="272" y="124" fill="#F87171" fontSize="11" fontFamily="monospace" fontWeight="bold">CONFLICTED (Location)</text>

        {/* Node 5: Unknown Abstention */}
        <rect x="52" y="62" width="16" height="16" fill="#64748B" rx="3" />
        <text x="15" y="55" fill="#CBD5E1" fontSize="10" fontFamily="monospace">UNKNOWN (Lang)</text>

        {/* Bounding Crosshairs (HydraDB Signatures) */}
        <g stroke="#00F0FF" strokeWidth="1" opacity="0.8">
          <line x1="120" y1="140" x2="160" y2="180" />
          <line x1="160" y1="140" x2="120" y2="180" />
          <rect x="120" y="140" width="40" height="40" fill="none" stroke="#00F0FF" strokeWidth="1" strokeDasharray="2 2" />
          <text x="123" y="135" fill="#00F0FF" fontSize="9" fontFamily="monospace">T=2025-01-20Z</text>
        </g>

        <g stroke="#FBBF24" strokeWidth="1" opacity="0.8">
          <line x1="350" y1="120" x2="390" y2="160" />
          <line x1="390" y1="120" x2="350" y2="160" />
          <rect x="350" y="120" width="40" height="40" fill="none" stroke="#FBBF24" strokeWidth="1" strokeDasharray="2 2" />
          <text x="353" y="115" fill="#FBBF24" fontSize="9" fontFamily="monospace">v2.0 (SUPERSEDED)</text>
        </g>

      </svg>
    </div>
  );
}
