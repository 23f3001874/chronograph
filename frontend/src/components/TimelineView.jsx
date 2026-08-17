import React, { useState, useEffect } from 'react';
import { Clock, ArrowRight, RefreshCw, GitCommit, ChevronRight } from 'lucide-react';
import EpistemicBadge from './EpistemicBadge';
import { getTimeline } from '../api';

export default function TimelineView({ subjectId, predicate, onSelectBelief }) {
  const [timeline, setTimeline] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTimeline = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getTimeline(subjectId, predicate);
      setTimeline(data.timeline || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTimeline();
  }, [subjectId, predicate]);

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h2 className="card-title" style={{ marginBottom: 0 }}>
          <Clock size={20} color="#F59E0B" />
          Belief Evolution Timeline ({subjectId} → {predicate})
        </h2>
        <button className="btn btn-secondary" style={{ padding: '0.375rem 0.75rem', fontSize: '0.75rem' }} onClick={fetchTimeline} disabled={loading}>
          <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
          Refresh Timeline
        </button>
      </div>

      {error && (
        <div style={{ padding: '0.75rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', color: '#EF4444', fontSize: '0.875rem' }}>
          {error}
        </div>
      )}

      {timeline.length === 0 ? (
        <div style={{ padding: '3rem', textAlign: 'center', color: '#6B7280', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
          <Clock size={36} opacity={0.4} />
          <p>No recorded beliefs found for subject '{subjectId}' and predicate '{predicate}'.</p>
        </div>
      ) : (
        <div style={{ position: 'relative', paddingLeft: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          
          {/* Vertical Timeline Bar */}
          <div style={{ position: 'absolute', left: '0.45rem', top: '1rem', bottom: '1rem', width: '2px', background: '#232A3D' }} />

          {timeline.map((item, idx) => {
            const isLatest = idx === timeline.length - 1;
            return (
              <div key={item.belief_id} style={{ position: 'relative', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                
                {/* Timeline Dot Node */}
                <div style={{
                  position: 'absolute', left: '-1.55rem', top: '1.25rem', width: '12px', height: '12px', borderRadius: '50%',
                  background: item.status === 'ACTIVE' ? '#10B981' : item.status === 'CONFLICTED' ? '#EF4444' : '#F59E0B',
                  border: '2px solid #090B10', boxShadow: item.status === 'ACTIVE' ? '0 0 10px rgba(16, 185, 129, 0.5)' : 'none'
                }} />

                {/* Timeline Card */}
                <div
                  className="card"
                  style={{
                    background: '#0D1017', border: '1px solid #232A3D', padding: '1rem 1.25rem', display: 'flex',
                    alignItems: 'center', justifyContent: 'space-between', cursor: 'pointer', transition: 'all 0.2s ease'
                  }}
                  onClick={() => onSelectBelief && onSelectBelief(item.belief_id)}
                >
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.375rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <span style={{ fontSize: '1.125rem', fontWeight: '700', color: '#F3F4F6' }}>
                        "{item.value}"
                      </span>
                      <EpistemicBadge status={item.status} />
                      <span style={{ fontSize: '0.75rem', background: '#1F293D', color: '#9CA3AF', padding: '0.125rem 0.5rem', borderRadius: '4px', fontFamily: 'monospace' }}>
                        v{item.version}
                      </span>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8125rem', color: '#9CA3AF' }}>
                      <Clock size={14} />
                      <span>Valid: {new Date(item.valid_from).toLocaleDateString()}</span>
                      <ArrowRight size={12} />
                      <span>{item.valid_until ? new Date(item.valid_until).toLocaleDateString() : 'Present (Ongoing)'}</span>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#3B82F6', fontSize: '0.8125rem', fontWeight: '500' }}>
                    <span>Inspect Lineage</span>
                    <ChevronRight size={16} />
                  </div>
                </div>

              </div>
            );
          })}

        </div>
      )}
    </div>
  );
}
