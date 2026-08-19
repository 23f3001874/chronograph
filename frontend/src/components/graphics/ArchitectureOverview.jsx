import React from 'react';
import { Database, Cpu, ShieldCheck } from 'lucide-react';

export default function ArchitectureOverview() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', width: '100%', maxWidth: '1100px', margin: '0 auto' }}>
      
      {/* Tier 1: HydraDB Substrate */}
      <div style={{ background: '#000000', border: '1px solid #2E2E2E', borderRadius: '10px', padding: '1.75rem' }}>
        <div style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#94A3B8', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
          <Database size={16} color="#3B82F6" />
          THE HYDRADB CLOUD SUBSTRATE (STORAGE & RETRIEVAL)
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.25rem' }}>
          <div style={{ background: '#05070B', border: '1px solid #1A1D24', padding: '1rem', borderRadius: '8px' }}>
            <div style={{ color: '#FFFFFF', fontWeight: '700', fontSize: '0.9375rem' }}>Vector Store</div>
            <div style={{ color: '#64748B', fontSize: '0.8125rem', marginTop: '0.25rem' }}>Semantic embeddings & similarity search</div>
          </div>
          <div style={{ background: '#05070B', border: '1px solid #1A1D24', padding: '1rem', borderRadius: '8px' }}>
            <div style={{ color: '#FFFFFF', fontWeight: '700', fontSize: '0.9375rem' }}>OpenCypher Graph</div>
            <div style={{ color: '#64748B', fontSize: '0.8125rem', marginTop: '0.25rem' }}>Entity-relationship context graph</div>
          </div>
          <div style={{ background: '#05070B', border: '1px solid #1A1D24', padding: '1rem', borderRadius: '8px' }}>
            <div style={{ color: '#FFFFFF', fontWeight: '700', fontSize: '0.9375rem' }}>Collection Partition</div>
            <div style={{ color: '#64748B', fontSize: '0.8125rem', marginTop: '0.25rem' }}>Multitenant document isolation</div>
          </div>
        </div>
      </div>

      {/* Tier 2: ChronoGraph Engine Core */}
      <div style={{ background: '#000000', border: '1px solid #3B82F6', borderRadius: '10px', padding: '1.75rem', boxShadow: '0 0 30px rgba(59, 130, 246, 0.12)' }}>
        <div style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#00F0FF', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
          <Cpu size={16} color="#00F0FF" />
          CHRONOGRAPH TEMPORAL REASONING CORE
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem' }}>
          <div style={{ background: '#050A14', border: '1px solid rgba(59, 130, 246, 0.3)', padding: '1rem', borderRadius: '8px' }}>
            <div style={{ color: '#00F0FF', fontWeight: '700', fontSize: '0.875rem' }}>Normalizer</div>
            <div style={{ color: '#94A3B8', fontSize: '0.78125rem', marginTop: '0.25rem' }}>Extracts triplet [S, P, O]</div>
          </div>
          <div style={{ background: '#050A14', border: '1px solid rgba(59, 130, 246, 0.3)', padding: '1rem', borderRadius: '8px' }}>
            <div style={{ color: '#00F0FF', fontWeight: '700', fontSize: '0.875rem' }}>State Machine</div>
            <div style={{ color: '#94A3B8', fontSize: '0.78125rem', marginTop: '0.25rem' }}>Enforces valid interval</div>
          </div>
          <div style={{ background: '#050A14', border: '1px solid rgba(59, 130, 246, 0.3)', padding: '1rem', borderRadius: '8px' }}>
            <div style={{ color: '#00F0FF', fontWeight: '700', fontSize: '0.875rem' }}>Contradiction</div>
            <div style={{ color: '#94A3B8', fontSize: '0.78125rem', marginTop: '0.25rem' }}>Flags active conflicts</div>
          </div>
          <div style={{ background: '#050A14', border: '1px solid rgba(59, 130, 246, 0.3)', padding: '1rem', borderRadius: '8px' }}>
            <div style={{ color: '#00F0FF', fontWeight: '700', fontSize: '0.875rem' }}>Abstention</div>
            <div style={{ color: '#94A3B8', fontSize: '0.78125rem', marginTop: '0.25rem' }}>Returns UNKNOWN</div>
          </div>
        </div>
      </div>

      {/* Tier 3: Resolution States */}
      <div style={{ background: '#000000', border: '1px solid #2E2E2E', borderRadius: '10px', padding: '1.75rem' }}>
        <div style={{ fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#94A3B8', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
          <ShieldCheck size={16} color="#34D399" />
          EPISTEMIC STATE RESOLUTION & LINEAGE STACK
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.25rem' }}>
          <div style={{ background: 'rgba(52, 211, 153, 0.08)', border: '1px solid rgba(52, 211, 153, 0.25)', padding: '1rem', borderRadius: '8px' }}>
            <div style={{ color: '#34D399', fontWeight: '700', fontSize: '0.875rem' }}>SUPPORTED</div>
            <div style={{ color: '#94A3B8', fontSize: '0.78125rem', marginTop: '0.25rem' }}>Active historical truth</div>
          </div>
          <div style={{ background: 'rgba(245, 158, 11, 0.08)', border: '1px solid rgba(245, 158, 11, 0.25)', padding: '1rem', borderRadius: '8px' }}>
            <div style={{ color: '#F59E0B', fontWeight: '700', fontSize: '0.875rem' }}>UNKNOWN</div>
            <div style={{ color: '#94A3B8', fontSize: '0.78125rem', marginTop: '0.25rem' }}>Epistemic abstention (0.0 conf)</div>
          </div>
          <div style={{ background: 'rgba(239, 68, 68, 0.08)', border: '1px solid rgba(239, 68, 68, 0.25)', padding: '1rem', borderRadius: '8px' }}>
            <div style={{ color: '#F87171', fontWeight: '700', fontSize: '0.875rem' }}>CONFLICTED</div>
            <div style={{ color: '#94A3B8', fontSize: '0.78125rem', marginTop: '0.25rem' }}>Active disagreement state</div>
          </div>
        </div>
      </div>

    </div>
  );
}
