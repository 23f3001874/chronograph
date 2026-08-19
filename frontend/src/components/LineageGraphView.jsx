import React, { useState, useEffect } from 'react';
import { GitBranch, ArrowDown, FileText } from 'lucide-react';
import EpistemicBadge from './EpistemicBadge';
import { getLineage } from '../api';

export default function LineageGraphView({ beliefId, onInspectEvidence }) {
  const [lineage, setLineage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchLineage = async () => {
    if (!beliefId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await getLineage(beliefId);
      setLineage(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLineage();
  }, [beliefId]);

  if (!beliefId) {
    return (
      <div className="card" style={{ padding: '3rem', textAlign: 'center', color: '#64748B', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.75rem' }}>
        <GitBranch size={40} opacity={0.3} color="#3B82F6" />
        <p style={{ fontSize: '0.875rem', fontWeight: '500' }}>Select a belief state from the Timeline or Query view to inspect its transition stack and evidence graph.</p>
      </div>
    );
  }

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h2 className="card-title" style={{ marginBottom: 0 }}>
          <GitBranch size={20} color="#60A5FA" />
          Belief Lineage Stack & Transition Graph
        </h2>
        <span style={{ fontSize: '0.75rem', fontFamily: 'monospace', background: 'rgba(59, 130, 246, 0.15)', padding: '0.25rem 0.625rem', borderRadius: '6px', border: '1px solid rgba(59, 130, 246, 0.3)', color: '#60A5FA', fontWeight: '600' }}>
          Target ID: {beliefId}
        </span>
      </div>

      {error && (
        <div style={{ padding: '0.875rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '10px', color: '#F87171', fontSize: '0.875rem' }}>
          {error}
        </div>
      )}

      {loading ? (
        <div style={{ padding: '2rem', textAlign: 'center', color: '#94A3B8' }}>Traversing cycle-safe lineage graph...</div>
      ) : lineage && lineage.history ? (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem', margin: '1rem 0' }}>
          
          {lineage.history.map((item, idx) => {
            const b = item.belief;
            const observations = item.observations || [];

            return (
              <React.Fragment key={b.id}>
                
                {/* Node Box */}
                <div
                  style={{
                    width: '100%', maxWidth: '640px', background: 'rgba(11, 15, 25, 0.9)', border: '1px solid rgba(59, 130, 246, 0.3)',
                    borderRadius: '14px', padding: '1.25rem', boxShadow: '0 8px 24px rgba(0,0,0,0.4)', display: 'flex',
                    flexDirection: 'column', gap: '0.75rem'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
                      <span style={{ fontSize: '1.125rem', fontWeight: '700', color: '#F8FAFC' }}>
                        "{b.object_value || b.object_id}"
                      </span>
                      <EpistemicBadge status={b.lifecycle_status} />
                    </div>
                    <span style={{ fontSize: '0.75rem', color: '#94A3B8', fontFamily: 'monospace' }}>
                      ID: {b.id}
                    </span>
                  </div>

                  <div style={{ fontSize: '0.8125rem', color: '#94A3B8', display: 'flex', gap: '1rem' }}>
                    <span>Valid From: {new Date(b.valid_from).toLocaleDateString()}</span>
                    <span>Valid Until: {b.valid_until ? new Date(b.valid_until).toLocaleDateString() : 'Present'}</span>
                    <span style={{ fontFamily: 'monospace', color: '#60A5FA' }}>v{b.version}</span>
                  </div>

                  {/* Grounded Evidence List */}
                  {observations.length > 0 && (
                    <div style={{ background: 'rgba(15, 23, 42, 0.8)', border: '1px solid rgba(59, 130, 246, 0.2)', borderRadius: '10px', padding: '0.875rem', fontSize: '0.8125rem' }}>
                      <span style={{ fontSize: '0.75rem', fontWeight: '700', color: '#60A5FA', display: 'flex', alignItems: 'center', gap: '0.375rem', marginBottom: '0.375rem' }}>
                        <FileText size={14} /> Grounded Evidence Observation:
                      </span>
                      {observations.map((obs) => (
                        <p key={obs.id} style={{ color: '#E2E8F0', fontStyle: 'italic', fontSize: '0.8125rem' }}>
                          "{obs.source_text}"
                        </p>
                      ))}
                    </div>
                  )}

                </div>

                {/* Directed Edge Connector */}
                {idx < lineage.history.length - 1 && (
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.25rem' }}>
                    <span style={{ fontSize: '0.75rem', fontWeight: '700', color: '#60A5FA', background: 'rgba(59, 130, 246, 0.15)', padding: '0.25rem 0.75rem', borderRadius: '9999px', border: '1px solid rgba(59, 130, 246, 0.35)', letterSpacing: '0.05em' }}>
                      {item.relationship || 'SUPERSEDES'}
                    </span>
                    <ArrowDown size={22} color="#3B82F6" />
                  </div>
                )}

              </React.Fragment>
            );
          })}

        </div>
      ) : null}
    </div>
  );
}
