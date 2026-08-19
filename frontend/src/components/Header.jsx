import React from 'react';
import { Activity, Clock, GitBranch, PlusCircle, Search, Zap, Cpu, ExternalLink } from 'lucide-react';

export default function Header({ activeTab, setActiveTab, healthStatus, onLoadEditorScenario, onLoadContradictionScenario, onLoadAbsentQuery }) {
  return (
    <header className="card" style={{ padding: '1.25rem 1.75rem', marginBottom: '0.5rem', background: 'rgba(11, 15, 25, 0.85)' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1.25rem' }}>
        
        {/* Brand & Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'linear-gradient(135deg, #2563EB 0%, #3B82F6 50%, #60A5FA 100%)', padding: '0.625rem', borderRadius: '12px', display: 'flex', boxShadow: '0 0 20px rgba(37, 99, 235, 0.4)' }}>
            <Activity size={24} color="#FFFFFF" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
              <h1 style={{ fontSize: '1.375rem', fontWeight: '800', letterSpacing: '-0.02em', color: '#F8FAFC', fontFamily: "'Plus Jakarta Sans', sans-serif" }}>
                ChronoGraph
              </h1>
              <span style={{ background: 'rgba(59, 130, 246, 0.15)', border: '1px solid rgba(59, 130, 246, 0.3)', color: '#60A5FA', fontSize: '0.6875rem', fontWeight: '700', padding: '0.125rem 0.5rem', borderRadius: '9999px', letterSpacing: '0.05em' }}>
                HYDRADB POWERED
              </span>
            </div>
            <p style={{ fontSize: '0.78125rem', color: '#94A3B8', marginTop: '0.125rem' }}>
              Temporal Belief & Epistemic Reasoning Engine for AI Memory
            </p>
          </div>
        </div>

        {/* Preset Scenarios Control Bar */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.75rem', color: '#64748B', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Presets:</span>
          <button className="btn btn-secondary" style={{ padding: '0.4rem 0.875rem', fontSize: '0.75rem', borderColor: 'rgba(59, 130, 246, 0.3)' }} onClick={onLoadEditorScenario}>
            <Zap size={14} color="#60A5FA" />
            VS Code → Cursor → VS Code
          </button>
          <button className="btn btn-secondary" style={{ padding: '0.4rem 0.875rem', fontSize: '0.75rem', borderColor: 'rgba(248, 113, 113, 0.3)' }} onClick={onLoadContradictionScenario}>
            <Zap size={14} color="#F87171" />
            Contradiction (CONFLICTED)
          </button>
          <button className="btn btn-secondary" style={{ padding: '0.4rem 0.875rem', fontSize: '0.75rem', borderColor: 'rgba(251, 191, 36, 0.3)' }} onClick={onLoadAbsentQuery}>
            <Zap size={14} color="#FBBF24" />
            Absent Fact (UNKNOWN)
          </button>
        </div>

        {/* Server Connection Status */}
        <div className="pill-status">
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: healthStatus === 'ok' ? '#34D399' : '#F87171', boxShadow: healthStatus === 'ok' ? '0 0 10px #34D399' : '0 0 10px #F87171' }}></span>
          <span style={{ color: '#94A3B8' }}>Substrate:</span>
          <span style={{ fontWeight: '700', color: healthStatus === 'ok' ? '#34D399' : '#F87171' }}>
            {healthStatus === 'ok' ? 'HydraDB Cloud (Ready)' : 'Disconnected'}
          </span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <nav style={{ display: 'flex', gap: '0.625rem', marginTop: '1.25rem', borderTop: '1px solid rgba(59, 130, 246, 0.15)', paddingTop: '0.875rem' }}>
        <button
          className={`btn ${activeTab === 'query' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveTab('query')}
        >
          <Search size={16} />
          Temporal Query (T)
        </button>
        <button
          className={`btn ${activeTab === 'timeline' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveTab('timeline')}
        >
          <Clock size={16} />
          Belief Timeline
        </button>
        <button
          className={`btn ${activeTab === 'lineage' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveTab('lineage')}
        >
          <GitBranch size={16} />
          Graph & Lineage Stack
        </button>
        <button
          className={`btn ${activeTab === 'ingest' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveTab('ingest')}
        >
          <PlusCircle size={16} />
          Memory Ingestion
        </button>
      </nav>
    </header>
  );
}
