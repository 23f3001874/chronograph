import React from 'react';
import { Database, Cpu, ShieldCheck, ArrowRight, Layers, GitBranch } from 'lucide-react';

export default function ArchitectureSection() {
  const pipelineSteps = [
    { num: '01', title: 'Raw Observations', desc: 'Ingested chat transcript chunks & statements' },
    { num: '02', title: 'HydraDB Substrate', desc: 'Vector store & OpenCypher graph context' },
    { num: '03', title: 'Triplet Normalization', desc: 'Extracts [Subject, Predicate, Object] & timestamps' },
    { num: '04', title: 'Epistemic State Machine', desc: 'Enforces validity intervals [valid_from, valid_until)' },
    { num: '05', title: 'Temporal Resolver', desc: 'Point-in-time state evaluation at target T' },
    { num: '06', title: 'Point-in-Time Answer', desc: 'Returned value with evidence & confidence' }
  ];

  return (
    <section id="architecture" style={{ padding: '6rem 0 4rem 0', background: '#000000', borderTop: '1px solid #141822' }}>
      <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '3.5rem' }}>
        
        {/* Section Header */}
        <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.875rem', alignItems: 'center' }}>
          <span className="mono-tag" style={{ color: '#00F0FF' }}>
            SYSTEM PIPELINE ARCHITECTURE
          </span>
          <h2 style={{ fontSize: '3rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
            From memory to belief.
          </h2>
          <p style={{ fontSize: '1.125rem', color: '#94A3B8', maxWidth: '720px', lineHeight: '1.6' }}>
            HydraDB stores and retrieves contextual evidence. ChronoGraph interprets that evidence through temporal belief semantics.
          </p>
        </div>

        {/* Pipeline Step Flow Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: '1rem' }}>
          {pipelineSteps.map((step, idx) => (
            <div key={idx} style={{ background: '#05070D', border: '1px solid #1F2430', borderRadius: '12px', padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.75rem', position: 'relative' }}>
              <span className="mono-tag" style={{ color: '#00F0FF', fontSize: '0.875rem' }}>{step.num}</span>
              <h4 style={{ fontSize: '0.9375rem', fontWeight: '700', color: '#FFFFFF' }}>{step.title}</h4>
              <p style={{ fontSize: '0.78125rem', color: '#94A3B8', lineHeight: '1.4' }}>{step.desc}</p>
            </div>
          ))}
        </div>

        {/* TWO-TIER SUBSTRATE DISTINCTION BOX */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginTop: '1rem' }}>
          
          {/* TIER 1: HYDRADB SUBSTRATE */}
          <div style={{ background: '#04060A', border: '1px solid #1F2430', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', borderBottom: '1px solid #1A1D24', paddingBottom: '1rem' }}>
              <div style={{ background: '#3B82F6', padding: '0.5rem', borderRadius: '8px' }}>
                <Database size={20} color="#FFFFFF" />
              </div>
              <div>
                <span className="mono-tag" style={{ color: '#60A5FA' }}>LAYER 1 • CONTEXT SUBSTRATE</span>
                <h3 style={{ fontSize: '1.375rem', fontWeight: '800', color: '#FFFFFF' }}>HydraDB Cloud</h3>
              </div>
            </div>

            <p style={{ fontSize: '0.9375rem', color: '#94A3B8', lineHeight: '1.6' }}>
              HydraDB provides the graph-native vector and Cypher context storage. It stores raw observations, entity relationships, and embeddings, enabling sub-millisecond retrieval of grounded memory fragments.
            </p>

            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.8125rem', color: '#CBD5E1', fontFamily: "'JetBrains Mono', monospace" }}>
              <li>✓ Vector Similarity Search & Embeddings</li>
              <li>✓ OpenCypher Entity Context Graph</li>
              <li>✓ Multitenant Collection Isolation</li>
            </ul>
          </div>

          {/* TIER 2: CHRONOGRAPH ENGINE */}
          <div style={{ background: '#040712', border: '1px solid #1E3A8A', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.25rem', boxShadow: '0 0 35px rgba(59, 130, 246, 0.15)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', borderBottom: '1px solid #1E3A8A', paddingBottom: '1rem' }}>
              <div style={{ background: '#00F0FF', padding: '0.5rem', borderRadius: '8px' }}>
                <Cpu size={20} color="#000000" />
              </div>
              <div>
                <span className="mono-tag" style={{ color: '#00F0FF' }}>LAYER 2 • REASONING LAYER</span>
                <h3 style={{ fontSize: '1.375rem', fontWeight: '800', color: '#FFFFFF' }}>ChronoGraph Engine</h3>
              </div>
            </div>

            <p style={{ fontSize: '0.9375rem', color: '#93C5FD', lineHeight: '1.6' }}>
              ChronoGraph sits above HydraDB as the temporal belief reasoning layer. It translates raw observations into versioned belief states, models validity intervals, flags active conflicts, and prevents future knowledge leakage.
            </p>

            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.8125rem', color: '#00F0FF', fontFamily: "'JetBrains Mono', monospace" }}>
              <li>✓ Temporal Belief State Machine</li>
              <li>✓ Point-in-Time Resolution Engine (T)</li>
              <li>✓ Epistemic Uncertainty & Abstention</li>
            </ul>
          </div>

        </div>

      </div>
    </section>
  );
}
