import React from 'react';
import { Activity, Clock, GitBranch, PlusCircle, Search, Layers, Zap } from 'lucide-react';

export default function Header({ activeTab, setActiveTab, healthStatus, onLoadEditorScenario, onLoadContradictionScenario, onLoadAbsentQuery }) {
  return (
    <header className="card" style={{ padding: '1rem 1.5rem', marginBottom: '0.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        
        {/* Title & Brand */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{ background: '#2563EB', padding: '0.5rem', borderRadius: '10px', display: 'flex' }}>
            <Activity size={24} color="#FFFFFF" />
          </div>
          <div>
            <h1 style={{ fontSize: '1.25rem', fontWeight: '700', letterSpacing: '-0.02em', color: '#F3F4F6' }}>
              ChronoGraph
            </h1>
            <p style={{ fontSize: '0.75rem', color: '#9CA3AF' }}>
              Temporal Belief & Memory Reasoning Engine
            </p>
          </div>
        </div>

        {/* Preset Scenarios */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.75rem', color: '#6B7280', fontWeight: '500' }}>Presets:</span>
          <button className="btn btn-secondary" style={{ padding: '0.375rem 0.75rem', fontSize: '0.75rem' }} onClick={onLoadEditorScenario}>
            <Zap size={14} color="#3B82F6" />
            VS Code → Cursor → VS Code
          </button>
          <button className="btn btn-secondary" style={{ padding: '0.375rem 0.75rem', fontSize: '0.75rem' }} onClick={onLoadContradictionScenario}>
            <Zap size={14} color="#EF4444" />
            Overlapping Contradiction
          </button>
          <button className="btn btn-secondary" style={{ padding: '0.375rem 0.75rem', fontSize: '0.75rem' }} onClick={onLoadAbsentQuery}>
            <Zap size={14} color="#9CA3AF" />
            Absent Query (UNKNOWN)
          </button>
        </div>

        {/* Server Connection Pill */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: '#0D1017', padding: '0.375rem 0.75rem', borderRadius: '9999px', border: '1px solid #232A3D', fontSize: '0.75rem' }}>
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: healthStatus === 'ok' ? '#10B981' : '#EF4444' }}></span>
          <span style={{ color: '#9CA3AF' }}>Backend:</span>
          <span style={{ fontWeight: '600', color: healthStatus === 'ok' ? '#10B981' : '#EF4444' }}>
            {healthStatus === 'ok' ? 'Connected (HydraDB Ready)' : 'Disconnected'}
          </span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <nav style={{ display: 'flex', gap: '0.5rem', marginTop: '1.25rem', borderTop: '1px solid #232A3D', paddingTop: '0.75rem' }}>
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
