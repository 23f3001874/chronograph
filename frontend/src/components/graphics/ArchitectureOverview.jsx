import React from 'react';
import { ArrowDown, Cpu, Database, ShieldCheck, Layers, GitBranch } from 'lucide-react';

export default function ArchitectureOverview() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', width: '100%' }}>
      
      {/* Box 1: HydraDB Substrate */}
      <div style={{ border: '1px solid #1F2430', borderRadius: '12px', padding: '1.25rem', background: '#05070B', position: 'relative' }}>
        <div style={{ fontSize: '0.75rem', fontFamily: 'monospace', color: '#94A3B8', fontWeight: '700', textTransform: 'uppercase', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Database size={16} color="#3B82F6" />
          1. HYDRADB CLOUD SUBSTRATE (STORAGE & RETRIEVAL)
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
          <div style={{ background: '#0B0F19', border: '1px solid #1F2430', padding: '0.875rem', borderRadius: '8px', fontSize: '0.8125rem', color: '#CBD5E1' }}>
            <div style={{ color: '#FFFFFF', fontWeight: '700', marginBottom: '0.25rem' }}>Vector Store</div>
            Semantic embeddings & similarity search
          </div>
          <div style={{ background: '#0B0F19', border: '1px solid #1F2430', padding: '0.875rem', borderRadius: '8px', fontSize: '0.8125rem', color: '#CBD5E1' }}>
            <div style={{ color: '#FFFFFF', fontWeight: '700', marginBottom: '0.25rem' }}>OpenCypher Graph</div>
            Entity-relationship context graph
          </div>
          <div style={{ background: '#0B0F19', border: '1px solid #1F2430', padding: '0.875rem', borderRadius: '8px', fontSize: '0.8125rem', color: '#CBD5E1' }}>
            <div style={{ color: '#FFFFFF', fontWeight: '700', marginBottom: '0.25rem' }}>Collection Partition</div>
            Multitenant isolated document store
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <ArrowDown size={24} color="#3B82F6" />
      </div>

      {/* Box 2: ChronoGraph Reasoning Core */}
      <div style={{ border: '1px solid rgba(59, 130, 246, 0.4)', borderRadius: '12px', padding: '1.25rem', background: '#080C14', boxShadow: '0 0 25px rgba(59, 130, 246, 0.15)' }}>
        <div style={{ fontSize: '0.75rem', fontFamily: 'monospace', color: '#00F0FF', fontWeight: '700', textTransform: 'uppercase', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Cpu size={16} color="#00F0FF" />
          2. CHRONOGRAPH TEMPORAL REASONING CORE
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem' }}>
          <div style={{ background: '#0D1322', border: '1px solid rgba(59, 130, 246, 0.3)', padding: '0.875rem', borderRadius: '8px', fontSize: '0.8125rem', color: '#F8FAFC' }}>
            <div style={{ color: '#00F0FF', fontWeight: '700', marginBottom: '0.25rem' }}>Normalizer</div>
            Extracts triplet $[S, P, O]$ & timestamp
          </div>
          <div style={{ background: '#0D1322', border: '1px solid rgba(59, 130, 246, 0.3)', padding: '0.875rem', borderRadius: '8px', fontSize: '0.8125rem', color: '#F8FAFC' }}>
            <div style={{ color: '#00F0FF', fontWeight: '700', marginBottom: '0.25rem' }}>State Machine</div>
            Enforces $[v_{from}, v_{until})$ validity
          </div>
          <div style={{ background: '#0D1322', border: '1px solid rgba(59, 130, 246, 0.3)', padding: '0.875rem', borderRadius: '8px', fontSize: '0.8125rem', color: '#F8FAFC' }}>
            <div style={{ color: '#00F0FF', fontWeight: '700', marginBottom: '0.25rem' }}>Contradiction</div>
            Detects active overlapping conflicts
          </div>
          <div style={{ background: '#0D1322', border: '1px solid rgba(59, 130, 246, 0.3)', padding: '0.875rem', borderRadius: '8px', fontSize: '0.8125rem', color: '#F8FAFC' }}>
            <div style={{ color: '#00F0FF', fontWeight: '700', marginBottom: '0.25rem' }}>Abstention</div>
            Returns UNKNOWN for absent facts
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <ArrowDown size={24} color="#00F0FF" />
      </div>

      {/* Box 3: Epistemic State Resolution */}
      <div style={{ border: '1px solid #1F2430', borderRadius: '12px', padding: '1.25rem', background: '#05070B' }}>
        <div style={{ fontSize: '0.75rem', fontFamily: 'monospace', color: '#94A3B8', fontWeight: '700', textTransform: 'uppercase', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <ShieldCheck size={16} color="#34D399" />
          3. EPISTEMIC STATE RESOLUTION & GROUNDED LINEAGE
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
          <div style={{ background: 'rgba(52, 211, 153, 0.1)', border: '1px solid rgba(52, 211, 153, 0.3)', padding: '0.875rem', borderRadius: '8px', fontSize: '0.8125rem', color: '#34D399' }}>
            <div style={{ fontWeight: '700', marginBottom: '0.25rem' }}>SUPPORTED</div>
            Active truth at target timestamp $T$
          </div>
          <div style={{ background: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.3)', padding: '0.875rem', borderRadius: '8px', fontSize: '0.8125rem', color: '#F59E0B' }}>
            <div style={{ fontWeight: '700', marginBottom: '0.25rem' }}>UNKNOWN</div>
            Epistemic abstention (0.0 confidence)
          </div>
          <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', padding: '0.875rem', borderRadius: '8px', fontSize: '0.8125rem', color: '#F87171' }}>
            <div style={{ fontWeight: '700', marginBottom: '0.25rem' }}>CONFLICTED</div>
            Simultaneous active disagreement
          </div>
        </div>
      </div>

    </div>
  );
}
