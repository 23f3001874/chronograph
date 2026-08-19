import React from 'react';
import { XCircle, CheckCircle2, ArrowRight, ShieldAlert, Clock, AlertTriangle, AlertCircle } from 'lucide-react';

export default function SplitScreenComparison() {
  return (
    <section style={{ display: 'flex', flexDirection: 'column', gap: '2rem', width: '100%', maxWidth: '1200px', margin: '0 auto' }}>
      
      {/* Section Header */}
      <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.75rem', alignItems: 'center' }}>
        <span style={{ color: '#00F0FF', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8125rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
          PARADIGM SHIFT
        </span>
        <h2 style={{ fontSize: '2.5rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em', color: '#FFFFFF' }}>
          Naive Memory Retrieval vs ChronoGraph
        </h2>
        <p style={{ fontSize: '1.0625rem', color: '#94A3B8', maxWidth: '700px', lineHeight: '1.6' }}>
          How conventional memory systems leak future knowledge, hallucinate fallback facts, and fail when preferences change over time.
        </p>
      </div>

      {/* Split Screen Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginTop: '1rem' }}>
        
        {/* LEFT COLUMN: WITHOUT TEMPORAL REASONING */}
        <div style={{ background: '#05060A', border: '1px solid #291B1B', borderRadius: '14px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          
          <div style={{ display: 'flex', alignItems: 'center', justifyBetween: 'space-between', borderBottom: '1px solid #291B1B', paddingBottom: '1rem' }}>
            <div>
              <span style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#F87171', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                CONVENTIONAL MEMORY
              </span>
              <h3 style={{ fontSize: '1.375rem', fontWeight: '800', color: '#FFFFFF', marginTop: '0.25rem' }}>
                Without Temporal Reasoning
              </h3>
            </div>
            <XCircle size={28} color="#F87171" />
          </div>

          {/* Sequential Memory Ingestion Example */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', background: '#0A0000', border: '1px solid #331515', borderRadius: '10px', padding: '1.25rem' }}>
            <span style={{ fontSize: '0.75rem', color: '#64748B', fontFamily: "'JetBrains Mono', monospace", fontWeight: '700' }}>MEMORIES INGESTED OVER TIME:</span>
            <div style={{ fontSize: '0.875rem', color: '#CBD5E1', fontFamily: "'JetBrains Mono', monospace", display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <div style={{ padding: '0.5rem', background: '#140808', borderRadius: '6px' }}>Jan 20: "I use VS Code for development."</div>
              <div style={{ padding: '0.5rem', background: '#140808', borderRadius: '6px' }}>Feb 20: "I switched to Cursor for AI features."</div>
              <div style={{ padding: '0.5rem', background: '#140808', borderRadius: '6px' }}>Mar 20: "I switched back to VS Code."</div>
            </div>
          </div>

          {/* Naive Retrieval Execution & Failure */}
          <div style={{ background: '#0E0505', border: '1px solid #421C1C', borderRadius: '10px', padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div style={{ fontSize: '0.8125rem', color: '#F87171', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              QUERY AT FEB 20: "What editor was the user using?"
            </div>
            <div style={{ fontSize: '1.125rem', fontWeight: '700', color: '#F87171' }}>
              → Returns "VS Code" (MARCH STATEMENT LEAKED)
            </div>
            <p style={{ fontSize: '0.8125rem', color: '#FCA5A5', lineHeight: '1.5' }}>
              Vector similarity retrieves the March 20 memory ("VS Code") into a February 20 query context. The agent acts on future knowledge it should not know yet.
            </p>
          </div>

          {/* Failure Summary Bullets */}
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.875rem', color: '#FCA5A5' }}>
            <li style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
              <AlertTriangle size={16} color="#F87171" />
              Future Knowledge Leakage (40% leakage rate)
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
              <AlertTriangle size={16} color="#F87171" />
              No concept of validity intervals [v_from, v_until)
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
              <AlertTriangle size={16} color="#F87171" />
              Hallucinates fallbacks instead of abstaining (0% UNKNOWN)
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
              <AlertTriangle size={16} color="#F87171" />
              Picks arbitrary winner on conflicts (0% CONFLICTED)
            </li>
          </ul>

        </div>

        {/* RIGHT COLUMN: WITH CHRONOGRAPH */}
        <div style={{ background: '#030812', border: '1px solid #1D3B7A', borderRadius: '14px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem', boxShadow: '0 0 40px rgba(59, 130, 246, 0.15)' }}>
          
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #1D3B7A', paddingBottom: '1rem' }}>
            <div>
              <span style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#00F0FF', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                TEMPORAL BELIEF ENGINE
              </span>
              <h3 style={{ fontSize: '1.375rem', fontWeight: '800', color: '#FFFFFF', marginTop: '0.25rem' }}>
                With ChronoGraph
              </h3>
            </div>
            <CheckCircle2 size={28} color="#00F0FF" />
          </div>

          {/* ChronoGraph Structured Validity Intervals */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', background: '#061024', border: '1px solid #1E40AF', borderRadius: '10px', padding: '1.25rem' }}>
            <span style={{ fontSize: '0.75rem', color: '#60A5FA', fontFamily: "'JetBrains Mono', monospace", fontWeight: '700' }}>TEMPORAL BELIEF STATE MACHINE:</span>
            <div style={{ fontSize: '0.8125rem', color: '#F8FAFC', fontFamily: "'JetBrains Mono', monospace", display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <div style={{ padding: '0.5rem', background: 'rgba(59, 130, 246, 0.15)', borderLeft: '3px solid #3B82F6', borderRadius: '4px', display: 'flex', justifyContent: 'space-between' }}>
                <span>JAN 20 → VS Code</span>
                <span style={{ color: '#60A5FA' }}>[Jan 20, Feb 20)</span>
              </div>
              <div style={{ padding: '0.5rem', background: 'rgba(59, 130, 246, 0.15)', borderLeft: '3px solid #00F0FF', borderRadius: '4px', display: 'flex', justifyContent: 'space-between' }}>
                <span>FEB 20 → Cursor</span>
                <span style={{ color: '#00F0FF' }}>[Feb 20, Mar 20)</span>
              </div>
              <div style={{ padding: '0.5rem', background: 'rgba(59, 130, 246, 0.15)', borderLeft: '3px solid #34D399', borderRadius: '4px', display: 'flex', justifyContent: 'space-between' }}>
                <span>MAR 20 → VS Code</span>
                <span style={{ color: '#34D399' }}>[Mar 20, Present)</span>
              </div>
            </div>
          </div>

          {/* Point-in-Time Resolution Result */}
          <div style={{ background: '#051838', border: '1px solid #2563EB', borderRadius: '10px', padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div style={{ fontSize: '0.8125rem', color: '#00F0FF', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              QUERY AT FEB 20: "What editor was the user using?"
            </div>
            <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#34D399' }}>
              → Returns "Cursor" (CONFIDENCE: 90.0%)
            </div>
            <p style={{ fontSize: '0.8125rem', color: '#93C5FD', lineHeight: '1.5' }}>
              ChronoGraph evaluates validity at timestamp T=Feb 20. It returns "Cursor", correctly ignoring future March events. Zero future leakage.
            </p>
          </div>

          {/* Feature Success Bullets */}
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.875rem', color: '#93C5FD' }}>
            <li style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
              <CheckCircle2 size={16} color="#00F0FF" />
              Strict Validity Intervals [valid_from, valid_until)
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
              <CheckCircle2 size={16} color="#00F0FF" />
              100% Deterministic Abstention (UNKNOWN)
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
              <CheckCircle2 size={16} color="#00F0FF" />
              100% Contradiction Detection (CONFLICTED)
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
              <CheckCircle2 size={16} color="#00F0FF" />
              Full Evidence & Lineage Graph (B3 → B2 → B1)
            </li>
          </ul>

        </div>

      </div>
    </section>
  );
}
