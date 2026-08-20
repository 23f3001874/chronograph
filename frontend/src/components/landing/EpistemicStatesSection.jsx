import React, { useState } from 'react';
import { HelpCircle, AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';

export default function EpistemicStatesSection() {
  const [activeTab, setActiveTab] = useState('unknown');

  return (
    <section id="temporal-engine" style={{ padding: '6rem 0 4rem 0', background: '#040508', borderTop: '1px solid #141A24' }}>
      <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '3.5rem' }}>
        
        {/* Section Header */}
        <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.875rem', alignItems: 'center' }}>
          <span className="mono-tag" style={{ color: '#FF7A18' }}>
            FORMAL EPISTEMIC SEMANTICS
          </span>
          <h2 style={{ fontSize: '3rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
            An AI that knows when it doesn't know.
          </h2>
          <p style={{ fontSize: '1.125rem', color: '#8B95A5', maxWidth: '750px', lineHeight: '1.6' }}>
            Traditional RAG forces binary true/false guesses. ChronoGraph models formal epistemic states, explicitly declaring uncertainty and flagging simultaneous conflicts.
          </p>
        </div>

        {/* 4 EPISTEMIC STATES CARDS STRIP: ACTIVE, SUPERSEDED, CONFLICTED, UNKNOWN */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.25rem' }}>
          
          <div style={{ background: '#080C12', border: '1px solid rgba(53, 208, 127, 0.35)', borderRadius: '14px', padding: '1.5rem', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <span className="mono-tag" style={{ color: '#35D07F' }}>ACTIVE</span>
            <h4 style={{ fontSize: '1.125rem', fontWeight: '700', color: '#FFFFFF' }}>Current Truth</h4>
            <p style={{ fontSize: '0.8125rem', color: '#8B95A5', lineHeight: '1.4' }}>What the system currently believes to be true.</p>
          </div>

          <div style={{ background: '#080C12', border: '1px solid rgba(255, 159, 67, 0.35)', borderRadius: '14px', padding: '1.5rem', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <span className="mono-tag" style={{ color: '#FF9F43' }}>SUPERSEDED</span>
            <h4 style={{ fontSize: '1.125rem', fontWeight: '700', color: '#FFFFFF' }}>Historical Fact</h4>
            <p style={{ fontSize: '0.8125rem', color: '#8B95A5', lineHeight: '1.4' }}>A newer valid belief replaced it at timestamp T.</p>
          </div>

          <div style={{ background: '#080C12', border: '1px solid rgba(255, 77, 94, 0.4)', borderRadius: '14px', padding: '1.5rem', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '0.5rem', boxShadow: '0 0 25px rgba(255, 77, 94, 0.15)' }}>
            <span className="mono-tag" style={{ color: '#FF4D5E' }}>CONFLICTED</span>
            <h4 style={{ fontSize: '1.125rem', fontWeight: '700', color: '#FFFFFF' }}>Active Disagreement</h4>
            <p style={{ fontSize: '0.8125rem', color: '#8B95A5', lineHeight: '1.4' }}>Competing active evidence exists. Refuses to pick a guess.</p>
          </div>

          {/* UNKNOWN REFUSAL CARD */}
          <div style={{ background: '#080C12', border: '1px solid rgba(0, 217, 255, 0.4)', borderRadius: '14px', padding: '1.5rem', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '0.5rem', boxShadow: '0 0 25px rgba(0, 217, 255, 0.15)' }}>
            <span className="mono-tag" style={{ color: '#00D9FF' }}>UNKNOWN</span>
            <h4 style={{ fontSize: '1.125rem', fontWeight: '700', color: '#FFFFFF' }}>Epistemic Abstention</h4>
            <p style={{ fontSize: '0.8125rem', color: '#8B95A5', lineHeight: '1.4' }}>No supporting evidence found. ChronoGraph refuses to fabricate an answer.</p>
          </div>

        </div>

        {/* INTERACTIVE DEMOS SWITCHER FOR UNKNOWN AND CONFLICTED */}
        <div style={{ background: '#070A10', border: '1px solid #1F2838', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          <div style={{ display: 'flex', gap: '1rem', borderBottom: '1px solid #141A24', paddingBottom: '1rem' }}>
            <button
              className={`btn-infrastructure ${activeTab === 'unknown' ? 'btn-infrastructure-primary' : 'btn-infrastructure-secondary'}`}
              onClick={() => setActiveTab('unknown')}
            >
              <HelpCircle size={16} color="#00D9FF" />
              1. Interactive UNKNOWN Demonstration
            </button>
            <button
              className={`btn-infrastructure ${activeTab === 'conflicted' ? 'btn-infrastructure-primary' : 'btn-infrastructure-secondary'}`}
              onClick={() => setActiveTab('conflicted')}
            >
              <AlertTriangle size={16} color="#FF4D5E" />
              2. Interactive CONFLICTED Demonstration
            </button>
          </div>

          {/* DEMO 1: UNKNOWN ABSTENTION */}
          {activeTab === 'unknown' && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr', gap: '2rem', alignItems: 'center' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <span className="mono-tag" style={{ color: '#00D9FF' }}>ABSENT FACT ABSTENTION</span>
                <h3 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#FFFFFF' }}>Refusing to Fabricate Answers</h3>
                <p style={{ fontSize: '0.9375rem', color: '#8B95A5', lineHeight: '1.6' }}>
                  When no recorded evidence exists for a predicate (e.g. favorite_language), naive AI invents a plausible lie. ChronoGraph halts deterministically with Confidence = 0.00.
                </p>
                <div style={{ background: '#04060A', border: '1px solid #1F2838', padding: '1rem', borderRadius: '8px', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8125rem', color: '#F5F7FA' }}>
                  QUERY: "What is the user's favorite programming language?"
                </div>
              </div>

              {/* Visual Flow */}
              <div style={{ background: '#05070C', border: '1px solid rgba(0, 217, 255, 0.3)', borderRadius: '12px', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#00D9FF', fontWeight: '700' }}>
                  EPISTEMIC PIPELINE EXECUTION:
                </div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace" }}>
                  <span style={{ color: '#5A6474' }}>NO EVIDENCE</span>
                  <span>→</span>
                  <span style={{ color: '#5A6474' }}>NO VALID BELIEFS</span>
                  <span>→</span>
                  <span style={{ color: '#5A6474' }}>NO FABRICATION</span>
                  <span>→</span>
                  <span style={{ color: '#00D9FF', fontWeight: '700' }}>UNKNOWN</span>
                </div>

                <div style={{ background: '#040508', border: '1px solid #00D9FF', borderRadius: '8px', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontSize: '0.75rem', color: '#8B95A5', fontFamily: "'JetBrains Mono', monospace" }}>EPISTEMIC STATUS</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#00D9FF' }}>UNKNOWN</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '0.75rem', color: '#8B95A5', fontFamily: "'JetBrains Mono', monospace" }}>CONFIDENCE</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#00D9FF' }}>0.00</div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* DEMO 2: CONFLICTED DISAGREEMENT */}
          {activeTab === 'conflicted' && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr', gap: '2rem', alignItems: 'center' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <span className="mono-tag" style={{ color: '#FF4D5E' }}>ACTIVE DISAGREEMENT DETECTOR</span>
                <h3 style={{ fontSize: '1.75rem', fontWeight: '800', color: '#FFFFFF' }}>Flagging Overlapping Conflicts</h3>
                <p style={{ fontSize: '0.9375rem', color: '#8B95A5', lineHeight: '1.6' }}>
                  When two active assertions overlap in time without explicit supersession ("Delhi" vs "Bangalore"), ChronoGraph flags CONFLICTED with Confidence = 0.50 rather than silently guessing.
                </p>
                <div style={{ background: '#04060A', border: '1px solid #1F2838', padding: '1rem', borderRadius: '8px', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8125rem', color: '#F5F7FA' }}>
                  QUERY AT FEB 15: "Where is the user located?"
                </div>
              </div>

              {/* Visual Flow */}
              <div style={{ background: '#05070C', border: '1px solid rgba(255, 77, 94, 0.3)', borderRadius: '12px', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                <div style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#FF4D5E', fontWeight: '700' }}>
                  OVERLAPPING ACTIVE INTERVALS:
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.75rem' }}>
                  <div style={{ background: 'rgba(255, 77, 94, 0.15)', border: '1px solid #FF4D5E', padding: '0.625rem 1rem', borderRadius: '6px', color: '#FF4D5E', display: 'flex', justifyContent: 'space-between' }}>
                    <span>BELIEF A: "Delhi"</span>
                    <span>[Jan 1, Mar 1)</span>
                  </div>
                  <div style={{ background: 'rgba(255, 77, 94, 0.15)', border: '1px solid #FF4D5E', padding: '0.625rem 1rem', borderRadius: '6px', color: '#FF4D5E', display: 'flex', justifyContent: 'space-between' }}>
                    <span>BELIEF B: "Bangalore"</span>
                    <span>[Feb 1, Apr 1)</span>
                  </div>
                </div>

                <div style={{ background: '#040508', border: '1px solid #FF4D5E', borderRadius: '8px', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontSize: '0.75rem', color: '#8B95A5', fontFamily: "'JetBrains Mono', monospace" }}>EPISTEMIC STATUS</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#FF4D5E' }}>CONFLICTED</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '0.75rem', color: '#8B95A5', fontFamily: "'JetBrains Mono', monospace" }}>CONFIDENCE</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#FF4D5E' }}>0.50</div>
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
