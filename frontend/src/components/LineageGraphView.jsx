import React, { useState, useEffect } from 'react';
import { GitBranch, ArrowDown, FileText, CheckCircle2, AlertCircle } from 'lucide-react';
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
      <div className="card" style={{ padding: '3rem', textAlign: 'center', color: '#6B7280' }}>
        <GitBranch size={36} opacity={0.4} style={{ margin: '0 auto 0.5rem auto' }} />
        <p style={{ fontSize: '0.875rem' }}>Select a belief state from the Timeline or Query view to inspect its transition stack and evidence graph.</p>
      </div>
    );
  }

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h2 className="card-title" style={{ marginBottom: 0 }}>
          <GitBranch size={20} color="#3B82F6" />
          Belief Lineage Stack & Grounding Graph
        </h2>
        <span style={{ fontSize: '0.75rem', fontFamily: 'monospace', background: '#0D1017', padding: '0.25rem 0.5rem', borderRadius: '4px', border: '1px solid #232A3D', color: '#9CA3AF' }}>
          Target ID: {beliefId}
        </span>
      </div>

      {error && (
        <div style={{ padding: '0.75rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', color: '#EF4444', fontSize: '0.875rem' }}>
          {error}
        </div>
      )}

      {loading ? (
        <div style={{ padding: '2rem', textAlign: 'center', color: '#9CA3AF' }}>Building lineage graph...</div>
      ) : lineage && lineage.history ? (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem', margin: '1rem 0' }}>
          
          {lineage.history.map((item, idx) => {
            const b = item.belief;
            const observations = item.observations || [];
            const rel = item.relationship;

            return (
              <React.Fragment key={b.id}>
                
                {/* Node Box */}
                <div
                  style={{
                    width: '100%', maxWidth: '640px', background: '#0D1017', border: '1px solid #232A3D',
                    borderRadius: '12px', padding: '1.25rem', boxShadow: '0 4px 12px rgba(0,0,0,0.5)', display: 'flex',
                    flexDirection: 'column', gap: '0.75rem'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span style={{ fontSize: '1.125rem', fontWeight: '700', color: '#F3F4F6' }}>
                        "{b.object_value || b.object_id}"
                      </span>
                      <EpistemicBadge status={b.lifecycle_status} />
                    </div>
                    <span style={{ fontSize: '0.75rem', color: '#9CA3AF', fontFamily: 'monospace' }}>
                      ID: {b.id}
                    </span>
                  </div>

                  <div style={{ fontSize: '0.8125rem', color: '#9CA3AF', display: 'flex', gap: '1rem' }}>
                    <span>Valid From: {new Date(b.valid_from).toLocaleDateString()}</span>
                    <span>Valid Until: {b.valid_until ? new Date(b.valid_until).toLocaleDateString() : 'Present'}</span>
                    <span>Version: v{b.version}</span>
                  </div>

                  {/* Grounded Evidence List */}
                  {observations.length > 0 && (
                    <div style={{ background: '#131722', border: '1px solid #1F293D', borderRadius: '8px', padding: '0.75rem', fontSize: '0.8125rem' }}>
                      <span style={{ fontSize: '0.75rem', fontWeight: '600', color: '#3B82F6', display: 'flex', alignItems: 'center', gap: '0.25rem', marginBottom: '0.375rem' }}>
                        <FileText size={14} /> Grounded Observation Evidence:
                      </span>
                      {observations.map((obs) => (
                        <p key={obs.id} style={{ color: '#E5E7EB', fontStyle: 'italic', fontSize: '0.78125rem' }}>
                          "{obs.source_text}"
                        </p>
                      ))}
                    </div>
                  )}

                </div>

                {/* Directed Edge Connector */}
                {idx < lineage.history.length - 1 && (
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.25rem' }}>
                    <span style={{ fontSize: '0.75rem', fontWeight: '700', color: '#3B82F6', background: 'rgba(59, 130, 246, 0.1)', padding: '0.2rem 0.6rem', borderRadius: '9999px', border: '1px solid rgba(59, 130, 246, 0.3)' }}>
                      {lineage.history[idx + 1].relationship}
                    </span>
                    <ArrowDown size={20} color="#3B82F6" />
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
