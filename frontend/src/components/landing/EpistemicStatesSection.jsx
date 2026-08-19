import React, { useState } from 'react';
import { HelpCircle, AlertTriangle, CheckCircle2, Clock, ShieldAlert, Cpu } from 'lucide-react';

export default function EpistemicStatesSection() {
  const [activeTab, setActiveTab] = useState('unknown');

  return (
    <section style={{ padding: '6rem 0 4rem 0', background: '#000000', borderTop: '1px solid #141822' }}>
      <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
        
        {/* Section Header */}
        <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.875rem', alignItems: 'center' }}>
          <span className="mono-tag" style={{ color: '#00F0FF' }}>
            FORMAL EPISTEMIC SEMANTICS
          </span>
          <h2 style={{ fontSize: '3rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
            An AI that knows when it doesn't know.
          </h2>
          <p style={{ fontSize: '1.125rem', color: '#94A3B8', maxWidth: '750px', lineHeight: '1.6' }}>
            Traditional RAG forces binary true/false guesses. ChronoGraph models formal epistemic states, explicitly declaring uncertainty and flagging simultaneous conflicts.
          </p>
        </div>

        {/* 5 EPISTEMIC STATES CARDS STRIP */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '1rem' }}>
          
          <div style={{ background: '#05070C', border: '1px solid rgba(52, 211, 153, 0.3)', borderRadius: '12px', padding: '1.25rem', textAlign: 'center' }}>
            <span className="mono-tag" style={{ color: '#34D399' }}>SUPPORTED</span>
            <p style={{ fontSize: '0.78125rem', color: '#94A3B8', marginTop: '0.5rem' }}>Active truth at target timestamp T</p>
          </div>

          <div style={{ background: '#05070C', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: '12px', padding: '1.25rem', textAlign: 'center' }}>
            <span className="mono-tag" style={{ color: '#3B82F6' }}>ACTIVE</span>
            <p style={{ fontSize: '0.78125rem', color: '#94A3B8', marginTop: '0.5rem' }}>Currently valid active belief</p>
          </div>

          <div style={{ background: '#05070C', border: '1px solid rgba(251, 191, 36, 0.3)', borderRadius: '12px', padding: '1.25rem', textAlign: 'center' }}>
            <span className="mono-tag" style={{ color: '#FBBF24' }}>SUPERSEDED</span>
            <p style={{ fontSize: '0.78125rem', color: '#94A3B8', marginTop: '0.5rem' }}>Replaced by newer valid belief</p>
          </div>

          <div style={{ background: '#05070C', border: '1px solid rgba(248, 113, 113, 0.35)', borderRadius: '12px', padding: '1.25rem', textAlign: 'center', boxShadow: '0 0 20px rgba(248, 113, 113, 0.15)' }}>
            <span className="mono-tag" style={{ color: '#F87171' }}>CONFLICTED</span>
            <p style={{ fontSize: '0.78125rem', color: '#94A3B8', marginTop: '0.5rem' }}>Active overlapping disagreement</p>
          </div>

          <div style={{ background: '#05070C', border: '1px solid rgba(251, 191, 36, 0.35)', borderRadius: '12px', padding: '1.25rem', textAlign: 'center', boxShadow: '0 0 20px rgba(251, 191, 36, 0.15)' }}>
            <span className="mono-tag" style={{ color: '#FBBF24' }}>UNKNOWN</span>
            <p style={{ fontSize: '0.78125rem', color: '#94A3B8', marginTop: '0.5rem' }}>Deterministic epistemic abstention</p>
          </div>

        </div>

        {/* INTERACTIVE DEMOS SWITCHER FOR UNKNOWN AND CONFLICTED */}
        <div style={{ background: '#04060A', border: '1px solid #1F2430', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          <div style={{ display: 'flex', gap: '1rem', borderBottom: '1px solid #1A1D24', paddingBottom: '1rem' }}>
            <button
              className={`btn-infrastructure ${activeTab === 'unknown' ? 'btn-infrastructure-primary' : 'btn-infrastructure-secondary'}`}
              onClick={() => setActiveTab('unknown')}
            >
              <HelpCircle size={16} color="#FBBF24" />
              1. Interactive UNKNOWN Demonstration
            </button>
            <button
              className={`btn-infrastructure ${activeTab === 'conflicted' ? 'btn-infrastructure-primary' : 'btn-infrastructure-secondary'}`}
              onClick={() => setActiveTab('conflicted')}
            >
              <AlertTriangle size={16} color="#F87171" />
              2. Interactive CONFLICTED Demonstration
            </button>
          </div>

          {/* DEMO 1: UNKNOWN ABSTENTION */}
          {activeTab === 'unknown' && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr', gap: '2rem', alignItems: 'center' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <span className="mono-tag" style={{ color: '#FBBF24' }}>ABSENT FACT ABSTENTION</span>
                <h3 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#FFFFFF' }}>Refusing to Fabricate Answers</h3>
                <p style={{ fontSize: '0.9375rem', color: '#94A3B8', lineHeight: '1.6' }}>
                  When no recorded evidence exists for a predicate (e.g. favorite_language), naive AI invents a plausible lie. ChronoGraph halts deterministically with Confidence = 0.00.
                </p>
                <div style={{ background: '#090C14', border: '1px solid #1F2430', padding: '1rem', borderRadius: '8px', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8125rem', color: '#CBD5E1' }}>
                  QUERY: "What is the user's favorite programming language?"
                </div>
              </div>

              {/* Visual Flow: NO EVIDENCE → NO VALID BELIEF → NO FABRICATION → UNKNOWN */}
              <div style={{ background: '#080A10', border: '1px solid rgba(251, 191, 36, 0.3)', borderRadius: '12px', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#FBBF24', fontWeight: '700' }}>
                  EPISTEMIC PIPELINE EXECUTION:
                </div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace" }}>
                  <span style={{ color: '#64748B' }}>NO EVIDENCE</span>
                  <span>→</span>
                  <span style={{ color: '#64748B' }}>NO VALID BELIEFS</span>
                  <span>→</span>
                  <span style={{ color: '#64748B' }}>NO FABRICATION</span>
                  <span>→</span>
                  <span style={{ color: '#FBBF24', fontWeight: '700' }}>UNKNOWN</span>
                </div>

                <div style={{ background: '#020305', border: '1px solid #FBBF24', borderRadius: '8px', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontSize: '0.75rem', color: '#94A3B8', fontFamily: "'JetBrains Mono', monospace" }}>EPISTEMIC STATUS</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#FBBF24' }}>UNKNOWN</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '0.75rem', color: '#94A3B8', fontFamily: "'JetBrains Mono', monospace" }}>CONFIDENCE</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#FBBF24' }}>0.00</div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* DEMO 2: CONFLICTED DISAGREEMENT */}
          {activeTab === 'conflicted' && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr', gap: '2rem', alignItems: 'center' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <span className="mono-tag" style={{ color: '#F87171' }}>ACTIVE DISAGREEMENT DETECTOR</span>
                <h3 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#FFFFFF' }}>Flagging Overlapping Conflicts</h3>
                <p style={{ fontSize: '0.9375rem', color: '#94A3B8', lineHeight: '1.6' }}>
                  When two active assertions overlap in time without explicit supersession ("Delhi" vs "Bangalore"), ChronoGraph flags CONFLICTED with Confidence = 0.50 rather than silently guessing.
                </p>
                <div style={{ background: '#090C14', border: '1px solid #1F2430', padding: '1rem', borderRadius: '8px', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8125rem', color: '#CBD5E1' }}>
                  QUERY AT FEB 15: "Where is the user located?"
                </div>
              </div>

              {/* Visual Flow: Overlapping Interval Bars */}
              <div style={{ background: '#080A10', border: '1px solid rgba(248, 113, 113, 0.3)', borderRadius: '12px', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                <div style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#F87171', fontWeight: '700' }}>
                  OVERLAPPING ACTIVE INTERVALS:
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.75rem' }}>
                  <div style={{ background: 'rgba(248, 113, 113, 0.15)', border: '1px solid #F87171', padding: '0.625rem 1rem', borderRadius: '6px', color: '#F87171', display: 'flex', justifyContent: 'space-between' }}>
                    <span>BELIEF A: "Delhi"</span>
                    <span>[Jan 1, Mar 1)</span>
                  </div>
                  <div style={{ background: 'rgba(248, 113, 113, 0.15)', border: '1px solid #F87171', padding: '0.625rem 1rem', borderRadius: '6px', color: '#F87171', display: 'flex', justifyContent: 'space-between' }}>
                    <span>BELIEF B: "Bangalore"</span>
                    <span>[Feb 1, Apr 1)</span>
                  </div>
                </div>

                <div style={{ background: '#020305', border: '1px solid #F87171', borderRadius: '8px', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontSize: '0.75rem', color: '#94A3B8', fontFamily: "'JetBrains Mono', monospace" }}>EPISTEMIC STATUS</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#F87171' }}>CONFLICTED</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '0.75rem', color: '#94A3B8', fontFamily: "'JetBrains Mono', monospace" }}>CONFIDENCE</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#F87171' }}>0.50</div>
                  </div>
                </div>
              </div>
            </div>
          )}

        </div>

      </div>
    </section>
  );
}
