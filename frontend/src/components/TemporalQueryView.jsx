import React, { useState } from 'react';
import { Calendar, Search, FileText, GitCommit, HelpCircle, ShieldCheck, AlertTriangle, AlertCircle } from 'lucide-react';
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
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr', gap: '1.5rem' }}>
      
      {/* Controls Column */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        <h2 className="card-title">
          <Search size={20} color="#3B82F6" />
          Point-in-Time State Query (T)
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
            <option value="favorite_language">favorite_language (Absent / UNKNOWN)</option>
          </select>
        </div>

        <div className="input-group">
          <label className="input-label">Evaluation Timestamp T (ISO-8601)</label>
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

        {/* Quick Date Presets */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <span style={{ fontSize: '0.75rem', color: '#9CA3AF', fontWeight: '600' }}>Demo Quick Presets:</span>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button className="btn btn-secondary" style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }} onClick={() => { setPredicate('favorite_editor'); handlePresetDate('2025-01-20T00:00:00Z'); }}>
              Jan 20 (VS Code)
            </button>
            <button className="btn btn-secondary" style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }} onClick={() => { setPredicate('favorite_editor'); handlePresetDate('2025-02-20T00:00:00Z'); }}>
              Feb 20 (Cursor)
            </button>
            <button className="btn btn-secondary" style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }} onClick={() => { setPredicate('favorite_editor'); handlePresetDate('2025-03-20T00:00:00Z'); }}>
              Mar 20 (VS Code)
            </button>
            <button className="btn btn-secondary" style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem', borderColor: '#F59E0B', color: '#F59E0B' }} onClick={() => { setPredicate('favorite_language'); handlePresetDate('2025-01-15T00:00:00Z'); }}>
              UNKNOWN Fact
            </button>
            <button className="btn btn-secondary" style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem', borderColor: '#EF4444', color: '#EF4444' }} onClick={() => { setPredicate('location'); handlePresetDate('2025-02-15T00:00:00Z'); }}>
              CONFLICTED State
            </button>
          </div>
        </div>

        <button className="btn btn-primary" style={{ marginTop: '0.5rem' }} onClick={handleQuery} disabled={loading}>
          {loading ? 'Resolving Temporal State...' : 'Execute Resolution Query'}
        </button>

        {error && (
          <div style={{ padding: '0.75rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', color: '#EF4444', fontSize: '0.875rem' }}>
            {error}
          </div>
        )}
      </div>

      {/* Resolution Output Column */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <h2 className="card-title">
          <ShieldCheck size={20} color="#10B981" />
          Structured Epistemic Resolution
        </h2>

        {!result ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '260px', color: '#6B7280', gap: '0.5rem' }}>
            <Search size={36} opacity={0.4} />
            <p style={{ fontSize: '0.875rem' }}>Select parameters and click Execute Resolution Query</p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            
            {/* Status & Value Header */}
            <div style={{ background: '#0D1017', border: '1px solid #232A3D', borderRadius: '10px', padding: '1.25rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <span style={{ fontSize: '0.75rem', color: '#9CA3AF', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Resolved Value (as of {new Date(result.as_of).toLocaleDateString()})
                </span>
                <div style={{ fontSize: '1.5rem', fontWeight: '700', color: result.status === 'SUPPORTED' ? '#F3F4F6' : (result.status === 'CONFLICTED' ? '#EF4444' : '#F59E0B'), marginTop: '0.25rem' }}>
                  {result.status === 'SUPPORTED' ? result.value : (result.status === 'CONFLICTED' ? 'Conflicted (Active Disagreement)' : 'Unknown (Absent Fact)')}
                </div>
              </div>
              <EpistemicBadge status={result.status} />
            </div>

            {/* Status Explanatory Box for UNKNOWN or CONFLICTED */}
            {result.status === 'UNKNOWN' && (
              <div style={{ padding: '0.875rem', background: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.3)', borderRadius: '8px', display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                <AlertCircle size={20} color="#F59E0B" style={{ marginTop: '2px', flexShrink: 0 }} />
                <div>
                  <h4 style={{ fontSize: '0.875rem', fontWeight: '600', color: '#F59E0B' }}>EPISTEMIC ABSTENTION</h4>
                  <p style={{ fontSize: '0.8125rem', color: '#D1D5DB', marginTop: '0.25rem' }}>
                    No recorded evidence exists for predicate <strong>'{result.predicate}'</strong>. ChronoGraph refrains from hallucinating or guessing a fallback value.
                  </p>
                </div>
              </div>
            )}

            {result.status === 'CONFLICTED' && (
              <div style={{ padding: '0.875rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                <AlertTriangle size={20} color="#EF4444" style={{ marginTop: '2px', flexShrink: 0 }} />
                <div>
                  <h4 style={{ fontSize: '0.875rem', fontWeight: '600', color: '#EF4444' }}>SIMULTANEOUS ACTIVE CONFLICT</h4>
                  <p style={{ fontSize: '0.8125rem', color: '#D1D5DB', marginTop: '0.25rem' }}>
                    Multiple active disagreeing assertions exist simultaneously for <strong>'{result.predicate}'</strong> without supersession. ChronoGraph flags a conflict rather than picking an arbitrary winner.
                  </p>
                </div>
              </div>
            )}

            {/* Confidence & Reasoning */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1rem' }}>
              <div style={{ background: '#0D1017', border: '1px solid #232A3D', borderRadius: '8px', padding: '0.875rem' }}>
                <span style={{ fontSize: '0.75rem', color: '#9CA3AF' }}>Confidence Score</span>
                <div style={{ fontSize: '1.25rem', fontWeight: '600', color: result.confidence > 0.8 ? '#10B981' : (result.confidence > 0.0 ? '#F59E0B' : '#9CA3AF'), marginTop: '0.25rem' }}>
                  {(result.confidence * 100).toFixed(0)}%
                </div>
              </div>
              <div style={{ background: '#0D1017', border: '1px solid #232A3D', borderRadius: '8px', padding: '0.875rem' }}>
                <span style={{ fontSize: '0.75rem', color: '#9CA3AF' }}>Epistemic Explanation</span>
                <p style={{ fontSize: '0.8125rem', color: '#D1D5DB', marginTop: '0.25rem', lineHeight: '1.4' }}>
                  {result.reason}
                </p>
              </div>
            </div>

            {/* Grounded Evidence List */}
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.875rem', fontWeight: '600', color: '#F3F4F6', display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                  <FileText size={16} color="#3B82F6" />
                  Grounded Evidence ({result.evidence?.length || 0})
                </span>
              </div>
              
              {result.evidence && result.evidence.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {result.evidence.map((ev) => (
                    <div
                      key={ev.id}
                      style={{ background: '#0D1017', border: '1px solid #232A3D', borderRadius: '8px', padding: '0.75rem', fontSize: '0.8125rem', display: 'flex', flexDirection: 'column', gap: '0.25rem' }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#9CA3AF' }}>
                        <span>Observed: {new Date(ev.observed_at).toLocaleString()}</span>
                        <span>Session: {ev.session_id}</span>
                      </div>
                      <p style={{ color: '#E5E7EB', fontStyle: 'italic' }}>"{ev.text}"</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ padding: '0.75rem', background: '#0D1017', border: '1px border-dashed #232A3D', borderRadius: '8px', color: '#6B7280', fontSize: '0.8125rem' }}>
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
