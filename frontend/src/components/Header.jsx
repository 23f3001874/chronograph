import React from 'react';
import { Activity, Clock, GitBranch, PlusCircle, Search, Zap, GitFork, ExternalLink } from 'lucide-react';

export default function Header({ activeTab, setActiveTab, healthStatus, onLoadEditorScenario, onLoadContradictionScenario, onLoadAbsentQuery }) {
  return (
    <header className="card" style={{ padding: '1.25rem 2rem', background: '#080A0F', border: '1px solid #1F2430' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1.25rem' }}>
        
        {/* Brand Logo & Tag */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: '#3B82F6', padding: '0.625rem', borderRadius: '10px', display: 'flex', boxShadow: '0 0 20px rgba(59, 130, 246, 0.5)' }}>
            <Activity size={22} color="#FFFFFF" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <span style={{ fontSize: '1.5rem', fontWeight: '800', letterSpacing: '-0.03em', color: '#FFFFFF', fontFamily: "'Space Grotesk', sans-serif" }}>
                ChronoGraph
              </span>
              <span className="eyebrow-badge" style={{ padding: '0.15rem 0.6rem', fontSize: '0.6875rem' }}>
                HYDRADB POWERED
              </span>
            </div>
            <p style={{ fontSize: '0.78125rem', color: '#94A3B8', marginTop: '0.125rem' }}>
              Temporal Belief & Epistemic Reasoning Engine for AI Agents
            </p>
          </div>
        </div>

        {/* Live Substrate Status & GitHub */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: '#05060A', padding: '0.4rem 0.875rem', borderRadius: '9999px', border: '1px solid #1F2430', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace" }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: healthStatus === 'ok' ? '#34D399' : '#F87171', boxShadow: healthStatus === 'ok' ? '0 0 10px #34D399' : '0 0 10px #F87171' }}></span>
            <span style={{ color: '#94A3B8' }}>Substrate:</span>
            <span style={{ fontWeight: '700', color: healthStatus === 'ok' ? '#34D399' : '#F87171' }}>
              {healthStatus === 'ok' ? 'HydraDB Cloud (Connected)' : 'Disconnected'}
            </span>
          </div>

          <a
            href="https://github.com/23f3001874/chronograph"
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-secondary"
            style={{ padding: '0.4rem 0.875rem', fontSize: '0.75rem', gap: '0.375rem' }}
          >
            <GitFork size={14} />
            GitHub Repo
            <ExternalLink size={12} opacity={0.6} />
          </a>
        </div>
      </div>

      {/* Navigation & Presets Bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem', marginTop: '1.25rem', borderTop: '1px solid #1F2430', paddingTop: '1rem' }}>
        <nav style={{ display: 'flex', gap: '0.625rem' }}>
          <button
            className={`btn ${activeTab === 'query' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('query')}
          >
            <Search size={16} />
            Temporal Query Playground (T)
          </button>
          <button
            className={`btn ${activeTab === 'timeline' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('timeline')}
          >
            <Clock size={16} />
            Belief Evolution Timeline
          </button>
          <button
            className={`btn ${activeTab === 'lineage' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('lineage')}
          >
            <GitBranch size={16} />
            Lineage Transition Graph
          </button>
          <button
            className={`btn ${activeTab === 'ingest' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('ingest')}
          >
            <PlusCircle size={16} />
            Memory Studio
          </button>
        </nav>

        {/* Presets Bar */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ fontSize: '0.75rem', color: '#64748B', fontFamily: "'JetBrains Mono', monospace", fontWeight: '700', textTransform: 'uppercase' }}>Quick Demos:</span>
          <button className="btn btn-secondary" style={{ padding: '0.35rem 0.75rem', fontSize: '0.75rem', borderColor: 'rgba(59, 130, 246, 0.4)' }} onClick={onLoadEditorScenario}>
            <Zap size={13} color="#3B82F6" />
            VS Code → Cursor → VS Code
          </button>
          <button className="btn btn-secondary" style={{ padding: '0.35rem 0.75rem', fontSize: '0.75rem', borderColor: 'rgba(248, 113, 113, 0.4)' }} onClick={onLoadContradictionScenario}>
            <Zap size={13} color="#F87171" />
            CONFLICTED State
          </button>
          <button className="btn btn-secondary" style={{ padding: '0.35rem 0.75rem', fontSize: '0.75rem', borderColor: 'rgba(251, 191, 36, 0.4)' }} onClick={onLoadAbsentQuery}>
            <Zap size={13} color="#FBBF24" />
            UNKNOWN Fact
          </button>
        </div>
      </div>
    </header>
  );
}
