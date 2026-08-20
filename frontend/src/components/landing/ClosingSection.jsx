import React from 'react';
import { Database, Cpu, FileText, HelpCircle, ArrowRight } from 'lucide-react';

export default function ClosingSection({ onLaunchDemo }) {
  return (
    <section style={{ padding: '7rem 0 5rem 0', background: '#040508', borderTop: '1px solid #141A24' }}>
      <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '4rem', alignItems: 'center', textAlign: 'center' }}>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', maxWidth: '820px' }}>
          <span className="mono-tag" style={{ color: '#FF7A18' }}>
            THE FUTURE OF AI AGENT MEMORY
          </span>
          <h2 style={{ fontSize: '3.75rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.04em', lineHeight: '1.08' }}>
            AI shouldn't just remember. <br />
            <span style={{ background: 'linear-gradient(135deg, #FFFFFF 0%, #FF9F43 60%, #FF7A18 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              AI should know what was true.
            </span>
          </h2>
          <p style={{ fontSize: '1.1875rem', color: '#8B95A5', lineHeight: '1.65', marginTop: '0.5rem' }}>
            Bring point-in-time state resolution, grounded evidence lineage, and deterministic epistemic abstention to your autonomous AI agents.
          </p>
        </div>

        {/* 4 CORE SUBSTRATE PILLARS */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.5rem', width: '100%' }}>
          
          <div style={{ background: '#070A10', border: '1px solid #1F2838', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem', textAlign: 'left' }}>
            <div style={{ background: '#FF7A18', width: 'fit-content', padding: '0.5rem', borderRadius: '8px' }}>
              <Database size={20} color="#FFFFFF" />
            </div>
            <span className="mono-tag" style={{ color: '#FF9F43' }}>HYDRADB</span>
            <h4 style={{ fontSize: '1.25rem', fontWeight: '800', color: '#FFFFFF' }}>Memory</h4>
            <p style={{ fontSize: '0.8125rem', color: '#8B95A5', lineHeight: '1.5' }}>Graph-native vector & Cypher context substrate.</p>
          </div>

          <div style={{ background: '#070A10', border: '1px solid #1F2838', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem', textAlign: 'left' }}>
            <div style={{ background: '#00D9FF', width: 'fit-content', padding: '0.5rem', borderRadius: '8px' }}>
              <Cpu size={20} color="#040508" />
            </div>
            <span className="mono-tag" style={{ color: '#00D9FF' }}>CHRONOGRAPH</span>
            <h4 style={{ fontSize: '1.25rem', fontWeight: '800', color: '#FFFFFF' }}>Temporal Reasoning</h4>
            <p style={{ fontSize: '0.8125rem', color: '#8B95A5', lineHeight: '1.5' }}>Interval validity state machine & point-in-time solver.</p>
          </div>

          <div style={{ background: '#070A10', border: '1px solid #1F2838', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem', textAlign: 'left' }}>
            <div style={{ background: '#35D07F', width: 'fit-content', padding: '0.5rem', borderRadius: '8px' }}>
              <FileText size={20} color="#040508" />
            </div>
            <span className="mono-tag" style={{ color: '#35D07F' }}>EVIDENCE</span>
            <h4 style={{ fontSize: '1.25rem', fontWeight: '800', color: '#FFFFFF' }}>Grounded Answers</h4>
            <p style={{ fontSize: '0.8125rem', color: '#8B95A5', lineHeight: '1.5' }}>Cycle-safe lineage graph linking every answer to source text.</p>
          </div>

          <div style={{ background: '#070A10', border: '1px solid #1F2838', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem', textAlign: 'left' }}>
            <div style={{ background: '#FF4D5E', width: 'fit-content', padding: '0.5rem', borderRadius: '8px' }}>
              <HelpCircle size={20} color="#FFFFFF" />
            </div>
            <span className="mono-tag" style={{ color: '#FF4D5E' }}>UNKNOWN</span>
            <h4 style={{ fontSize: '1.25rem', fontWeight: '800', color: '#FFFFFF' }}>Honest Abstention</h4>
            <p style={{ fontSize: '0.8125rem', color: '#8B95A5', lineHeight: '1.5' }}>Zero hallucination on absent facts with confidence 0.00.</p>
          </div>

        </div>

        {/* CTA BUTTON */}
        <button
          className="btn-infrastructure btn-infrastructure-primary"
          style={{ padding: '1rem 2.5rem', fontSize: '1.125rem', marginTop: '1rem' }}
          onClick={onLaunchDemo}
        >
          Try ChronoGraph
          <ArrowRight size={20} />
        </button>

      </div>
    </section>
  );
}
