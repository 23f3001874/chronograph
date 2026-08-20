import React from 'react';
import { Database, Cpu, ExternalLink } from 'lucide-react';

export default function HydraDBSection() {
  return (
    <section style={{ padding: '6rem 0 4rem 0', background: '#040508', borderTop: '1px solid #141A24' }}>
      <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
        
        {/* Section Header */}
        <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.875rem', alignItems: 'center' }}>
          <span className="mono-tag" style={{ color: '#FF7A18' }}>
            SUBSTRATE INTEGRATION
          </span>
          <h2 style={{ fontSize: '3rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
            Built on HydraDB.
          </h2>
          <p style={{ fontSize: '1.125rem', color: '#8B95A5', maxWidth: '720px', lineHeight: '1.6' }}>
            ChronoGraph leverages HydraDB Cloud's graph-native vector and Cypher storage substrate for high-performance context and evidence grounding.
          </p>
        </div>

        {/* Relationship Architectural Card */}
        <div style={{ background: '#070A10', border: '1px solid #1F2838', borderRadius: '16px', padding: '2.5rem', display: 'grid', gridTemplateColumns: '1fr 1.2fr', gap: '3rem', alignItems: 'center' }}>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <span className="mono-tag" style={{ color: '#FF9F43' }}>HACK HYDRA 2026</span>
            <h3 style={{ fontSize: '1.875rem', fontWeight: '800', color: '#FFFFFF' }}>Built for Hack Hydra with HydraDB</h3>
            <p style={{ fontSize: '0.9375rem', color: '#8B95A5', lineHeight: '1.6' }}>
              ChronoGraph is designed specifically for Hack Hydra Track 3 (Memory & Context Retrieval), demonstrating how graph-native memory engines enable deterministic temporal reasoning.
            </p>
            <a
              href="https://hydradb.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="btn-infrastructure btn-infrastructure-primary"
              style={{ width: 'fit-content', marginTop: '0.5rem' }}
            >
              Explore HydraDB
              <ExternalLink size={16} />
            </a>
          </div>

          {/* Substrate Stack Visualization */}
          <div style={{ background: '#04060A', border: '1px solid #FF7A18', borderRadius: '12px', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8125rem' }}>
            <div style={{ padding: '0.875rem', background: '#0A0E18', borderLeft: '3px solid #FF7A18', borderRadius: '6px', color: '#FF9F43' }}>
              HYDRADB CLOUD SUBSTRATE (Graph-native context)
            </div>
            <div style={{ textAlign: 'center', color: '#5A6474' }}>↓ EVIDENCE GROUNDING</div>
            <div style={{ padding: '0.875rem', background: '#0A0E18', borderLeft: '3px solid #00D9FF', borderRadius: '6px', color: '#00D9FF' }}>
              CHRONOGRAPH ENGINE (Temporal belief layer)
            </div>
            <div style={{ textAlign: 'center', color: '#5A6474' }}>↓ REASONED ANSWER</div>
            <div style={{ padding: '0.875rem', background: '#0A0E18', borderLeft: '3px solid #35D07F', borderRadius: '6px', color: '#35D07F' }}>
              AI AGENT WORKFLOW (Historical reasoning)
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}
