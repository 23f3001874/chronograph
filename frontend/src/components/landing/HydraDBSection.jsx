import React from 'react';
import { Database, Cpu, ArrowRight, ExternalLink } from 'lucide-react';

export default function HydraDBSection() {
  return (
    <section style={{ padding: '6rem 0 4rem 0', background: '#000000', borderTop: '1px solid #141822' }}>
      <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
        
        {/* Section Header */}
        <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.875rem', alignItems: 'center' }}>
          <span className="mono-tag" style={{ color: '#00F0FF' }}>
            SUBSTRATE INTEGRATION
          </span>
          <h2 style={{ fontSize: '3rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
            Built on HydraDB.
          </h2>
          <p style={{ fontSize: '1.125rem', color: '#94A3B8', maxWidth: '720px', lineHeight: '1.6' }}>
            ChronoGraph leverages HydraDB Cloud's graph-native vector and Cypher storage substrate for high-performance context and evidence grounding.
          </p>
        </div>

        {/* Relationship Architectural Card */}
        <div style={{ background: '#05070D', border: '1px solid #1F2430', borderRadius: '16px', padding: '2.5rem', display: 'grid', gridTemplateColumns: '1fr 1.2fr', gap: '3rem', alignItems: 'center' }}>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <span className="mono-tag" style={{ color: '#60A5FA' }}>HACK HYDRA 2026</span>
            <h3 style={{ fontSize: '1.875rem', fontWeight: '800', color: '#FFFFFF' }}>Built for Hack Hydra with HydraDB</h3>
            <p style={{ fontSize: '0.9375rem', color: '#94A3B8', lineHeight: '1.6' }}>
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
          <div style={{ background: '#030408', border: '1px solid #1E3A8A', borderRadius: '12px', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8125rem' }}>
            <div style={{ padding: '0.875rem', background: '#080F20', borderLeft: '3px solid #3B82F6', borderRadius: '6px', color: '#60A5FA' }}>
              HYDRADB CLOUD SUBSTRATE (Graph-native context)
            </div>
            <div style={{ textAlign: 'center', color: '#64748B' }}>↓ EVIDENCE GROUNDING</div>
            <div style={{ padding: '0.875rem', background: '#080F20', borderLeft: '3px solid #00F0FF', borderRadius: '6px', color: '#00F0FF' }}>
              CHRONOGRAPH ENGINE (Temporal belief layer)
            </div>
            <div style={{ textAlign: 'center', color: '#64748B' }}>↓ REASONED ANSWER</div>
            <div style={{ padding: '0.875rem', background: '#080F20', borderLeft: '3px solid #34D399', borderRadius: '6px', color: '#34D399' }}>
              AI AGENT WORKFLOW (Historical reasoning)
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}
