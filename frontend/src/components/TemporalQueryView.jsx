import React, { useState } from 'react';
import { Calendar, Search, FileText, ShieldCheck, AlertCircle, AlertTriangle, Cpu, Layers } from 'lucide-react';
import EpistemicBadge from './EpistemicBadge';
import { queryTemporalState } from '../api';

export default function TemporalQueryView({ subjectId, setSubjectId, predicate, setPredicate, onInspectEvidence }) {
  const [selectedDate, setSelectedDate] = useState('2025-01-20T00:00:00Z');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleQuery = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await queryTemporalState(subjectId, predicate, selectedDate, true, true);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePresetDate = (isoStr) => {
    setSelectedDate(isoStr);
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.25fr', gap: '1.5rem' }}>
      
      {/* Controls Column */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        <h2 className="card-title">
          <Search size={20} color="#60A5FA" />
          Point-in-Time Temporal Query ($T$)
        </h2>

        <div className="input-group">
          <label className="input-label">Subject Entity ID</label>
          <input
            className="input-control"
            value={subjectId}
            onChange={(e) => setSubjectId(e.target.value)}
            placeholder="e.g. user"
          />
        </div>

        <div className="input-group">
          <label className="input-label">Predicate Attribute</label>
          <select
            className="input-control"
            value={predicate}
            onChange={(e) => setPredicate(e.target.value)}
          >
            <option value="favorite_editor">favorite_editor (VS Code → Cursor → VS Code)</option>
            <option value="location">location (Delhi vs Bangalore Contradiction)</option>
            <option value="favorite_language">favorite_language (Absent Fact / UNKNOWN)</option>
          </select>
        </div>

        <div className="input-group">
          <label className="input-label">Evaluation Timestamp $T$ (ISO-8601)</label>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <input
              type="datetime-local"
              className="input-control"
              style={{ flex: 1 }}
              value={selectedDate.slice(0, 16)}
              onChange={(e) => setSelectedDate(new Date(e.target.value).toISOString())}
            />
          </div>
        </div>

        {/* Quick Presets */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.625rem' }}>
          <span style={{ fontSize: '0.75rem', color: '#94A3B8', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Scrub Temporal Timeline:</span>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button className="btn btn-secondary" style={{ padding: '0.3rem 0.625rem', fontSize: '0.75rem' }} onClick={() => { setPredicate('favorite_editor'); handlePresetDate('2025-01-20T00:00:00Z'); }}>
              Jan 20 (VS Code)
            </button>
            <button className="btn btn-secondary" style={{ padding: '0.3rem 0.625rem', fontSize: '0.75rem' }} onClick={() => { setPredicate('favorite_editor'); handlePresetDate('2025-02-20T00:00:00Z'); }}>
              Feb 20 (Cursor)
            </button>
            <button className="btn btn-secondary" style={{ padding: '0.3rem 0.625rem', fontSize: '0.75rem' }} onClick={() => { setPredicate('favorite_editor'); handlePresetDate('2025-03-20T00:00:00Z'); }}>
              Mar 20 (VS Code)
            </button>
            <button className="btn btn-secondary" style={{ padding: '0.3rem 0.625rem', fontSize: '0.75rem', borderColor: 'rgba(251, 191, 36, 0.4)', color: '#FBBF24' }} onClick={() => { setPredicate('favorite_language'); handlePresetDate('2025-01-15T00:00:00Z'); }}>
              UNKNOWN Fact
            </button>
            <button className="btn btn-secondary" style={{ padding: '0.3rem 0.625rem', fontSize: '0.75rem', borderColor: 'rgba(248, 113, 113, 0.4)', color: '#F87171' }} onClick={() => { setPredicate('location'); handlePresetDate('2025-02-15T00:00:00Z'); }}>
              CONFLICTED State
            </button>
          </div>
        </div>

        <button className="btn btn-primary" style={{ marginTop: '0.5rem' }} onClick={handleQuery} disabled={loading}>
          {loading ? 'Resolving Temporal State...' : 'Execute Point-in-Time Query'}
        </button>

        {error && (
          <div style={{ padding: '0.875rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '10px', color: '#F87171', fontSize: '0.875rem' }}>
            {error}
          </div>
        )}
      </div>

      {/* Resolution Output Column */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        <h2 className="card-title">
          <ShieldCheck size={20} color="#34D399" />
          Structured Epistemic Resolution
        </h2>

        {!result ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '280px', color: '#64748B', gap: '0.75rem' }}>
            <Cpu size={42} opacity={0.3} color="#3B82F6" />
            <p style={{ fontSize: '0.875rem', fontWeight: '500' }}>Select parameters and click Execute Point-in-Time Query</p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            
            {/* Status & Value Hero Card */}
            <div style={{ background: 'rgba(11, 15, 25, 0.9)', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: '14px', padding: '1.25rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)' }}>
              <div>
                <span style={{ fontSize: '0.75rem', color: '#94A3B8', textTransform: 'uppercase', letterSpacing: '0.06em', fontWeight: '700' }}>
                  Resolved Value (as of {new Date(result.as_of).toLocaleDateString()})
                </span>
                <div style={{ fontSize: '1.75rem', fontWeight: '800', color: result.status === 'SUPPORTED' ? '#F8FAFC' : (result.status === 'CONFLICTED' ? '#F87171' : '#FBBF24'), marginTop: '0.25rem' }}>
                  {result.status === 'SUPPORTED' ? result.value : (result.status === 'CONFLICTED' ? 'Conflicted (Active Disagreement)' : 'Unknown (Absent Fact)')}
                </div>
              </div>
              <EpistemicBadge status={result.status} />
            </div>

            {/* UNKNOWN / CONFLICTED Hero Explanations */}
            {result.status === 'UNKNOWN' && (
              <div style={{ padding: '1rem', background: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.35)', borderRadius: '12px', display: 'flex', gap: '0.875rem', alignItems: 'flex-start' }}>
                <AlertCircle size={22} color="#FBBF24" style={{ marginTop: '2px', flexShrink: 0 }} />
                <div>
                  <h4 style={{ fontSize: '0.875rem', fontWeight: '700', color: '#FBBF24', letterSpacing: '0.02em' }}>EPISTEMIC ABSTENTION (UNKNOWN)</h4>
                  <p style={{ fontSize: '0.8125rem', color: '#CBD5E1', marginTop: '0.25rem', lineHeight: '1.4' }}>
                    No recorded evidence exists for predicate <strong>'{result.predicate}'</strong>. ChronoGraph refrains from hallucinating or guessing a fallback value.
                  </p>
                </div>
              </div>
            )}

            {result.status === 'CONFLICTED' && (
              <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.35)', borderRadius: '12px', display: 'flex', gap: '0.875rem', alignItems: 'flex-start' }}>
                <AlertTriangle size={22} color="#F87171" style={{ marginTop: '2px', flexShrink: 0 }} />
                <div>
                  <h4 style={{ fontSize: '0.875rem', fontWeight: '700', color: '#F87171', letterSpacing: '0.02em' }}>SIMULTANEOUS ACTIVE CONFLICT</h4>
                  <p style={{ fontSize: '0.8125rem', color: '#CBD5E1', marginTop: '0.25rem', lineHeight: '1.4' }}>
                    Multiple active disagreeing assertions exist simultaneously for <strong>'{result.predicate}'</strong> without supersession. ChronoGraph flags a conflict rather than picking an arbitrary winner.
                  </p>
                </div>
              </div>
            )}

            {/* Confidence & Reasoning */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1rem' }}>
              <div style={{ background: 'rgba(11, 15, 25, 0.8)', border: '1px solid rgba(59, 130, 246, 0.2)', borderRadius: '12px', padding: '1rem' }}>
                <span style={{ fontSize: '0.75rem', color: '#94A3B8', fontWeight: '600' }}>Confidence Score</span>
                <div style={{ fontSize: '1.5rem', fontWeight: '800', color: result.confidence > 0.8 ? '#34D399' : (result.confidence > 0.0 ? '#FBBF24' : '#94A3B8'), marginTop: '0.25rem' }}>
                  {(result.confidence * 100).toFixed(0)}%
                </div>
              </div>
              <div style={{ background: 'rgba(11, 15, 25, 0.8)', border: '1px solid rgba(59, 130, 246, 0.2)', borderRadius: '12px', padding: '1rem' }}>
                <span style={{ fontSize: '0.75rem', color: '#94A3B8', fontWeight: '600' }}>Epistemic Reason</span>
                <p style={{ fontSize: '0.8125rem', color: '#CBD5E1', marginTop: '0.25rem', lineHeight: '1.4' }}>
                  {result.reason}
                </p>
              </div>
            </div>

            {/* Grounded Evidence List */}
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.625rem' }}>
                <span style={{ fontSize: '0.875rem', fontWeight: '700', color: '#F8FAFC', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <FileText size={16} color="#60A5FA" />
                  Grounded Evidence Observations ({result.evidence?.length || 0})
                </span>
              </div>
              
              {result.evidence && result.evidence.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.625rem' }}>
                  {result.evidence.map((ev) => (
                    <div
                      key={ev.id}
                      style={{ background: 'rgba(11, 15, 25, 0.85)', border: '1px solid rgba(59, 130, 246, 0.25)', borderRadius: '12px', padding: '0.875rem', fontSize: '0.8125rem', display: 'flex', flexDirection: 'column', gap: '0.375rem' }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94A3B8' }}>
                        <span>Observed: {new Date(ev.observed_at).toLocaleString()}</span>
                        <span style={{ fontFamily: 'monospace', background: 'rgba(59, 130, 246, 0.15)', color: '#60A5FA', padding: '0.1rem 0.4rem', borderRadius: '4px' }}>Session: {ev.session_id}</span>
                      </div>
                      <p style={{ color: '#E2E8F0', fontStyle: 'italic', fontSize: '0.875rem' }}>"{ev.text}"</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ padding: '1rem', background: 'rgba(11, 15, 25, 0.6)', border: '1px border-dashed rgba(59, 130, 246, 0.2)', borderRadius: '12px', color: '#64748B', fontSize: '0.8125rem', textAlign: 'center' }}>
                  No grounded evidence observations associated with this query state.
                </div>
              )}
            </div>

          </div>
        )}
      </div>

    </div>
  );
}
