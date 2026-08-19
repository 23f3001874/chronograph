import React, { useState, useEffect } from 'react';
import { Clock, ArrowRight, RefreshCw, ChevronRight } from 'lucide-react';
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
          <Clock size={20} color="#60A5FA" />
          Belief Evolution Timeline ({subjectId} → {predicate})
        </h2>
        <button className="btn btn-secondary" style={{ padding: '0.4rem 0.875rem', fontSize: '0.75rem' }} onClick={fetchTimeline} disabled={loading}>
          <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
          Refresh Timeline
        </button>
      </div>

      {error && (
        <div style={{ padding: '0.875rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '10px', color: '#F87171', fontSize: '0.875rem' }}>
          {error}
        </div>
      )}

      {timeline.length === 0 ? (
        <div style={{ padding: '3rem', textAlign: 'center', color: '#64748B', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.75rem' }}>
          <Clock size={40} opacity={0.3} color="#3B82F6" />
          <p style={{ fontSize: '0.875rem', fontWeight: '500' }}>No recorded beliefs found for subject '{subjectId}' and predicate '{predicate}'.</p>
        </div>
      ) : (
        <div style={{ position: 'relative', paddingLeft: '1.75rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          
          {/* Vertical Electric Line */}
          <div style={{ position: 'absolute', left: '0.5rem', top: '1.25rem', bottom: '1.25rem', width: '2px', background: 'linear-gradient(180deg, #2563EB 0%, #3B82F6 50%, rgba(59, 130, 246, 0.1) 100%)' }} />

          {timeline.map((item, idx) => {
            return (
              <div key={item.belief_id} style={{ position: 'relative', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                
                {/* Timeline Dot Node */}
                <div style={{
                  position: 'absolute', left: '-1.65rem', top: '1.25rem', width: '14px', height: '14px', borderRadius: '50%',
                  background: item.status === 'ACTIVE' ? '#34D399' : item.status === 'CONFLICTED' ? '#F87171' : '#FBBF24',
                  border: '3px solid #030712', boxShadow: item.status === 'ACTIVE' ? '0 0 12px #34D399' : 'none'
                }} />

                {/* Timeline Card */}
                <div
                  className="card"
                  style={{
                    background: 'rgba(11, 15, 25, 0.85)', border: '1px solid rgba(59, 130, 246, 0.25)', padding: '1.125rem 1.375rem', display: 'flex',
                    alignItems: 'center', justifyContent: 'space-between', cursor: 'pointer', transition: 'all 0.25s ease'
                  }}
                  onClick={() => onSelectBelief && onSelectBelief(item.belief_id)}
                >
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.375rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <span style={{ fontSize: '1.125rem', fontWeight: '700', color: '#F8FAFC' }}>
                        "{item.value}"
                      </span>
                      <EpistemicBadge status={item.status} />
                      <span style={{ fontSize: '0.75rem', background: 'rgba(59, 130, 246, 0.15)', color: '#60A5FA', padding: '0.125rem 0.5rem', borderRadius: '6px', fontFamily: 'monospace', fontWeight: '600' }}>
                        v{item.version}
                      </span>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8125rem', color: '#94A3B8' }}>
                      <Clock size={14} color="#60A5FA" />
                      <span>Valid: {new Date(item.valid_from).toLocaleDateString()}</span>
                      <ArrowRight size={12} />
                      <span>{item.valid_until ? new Date(item.valid_until).toLocaleDateString() : 'Present (Ongoing)'}</span>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#60A5FA', fontSize: '0.8125rem', fontWeight: '600' }}>
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
