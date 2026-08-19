import React from 'react';
import { X, FileText, Calendar } from 'lucide-react';

export default function EvidenceModal({ isOpen, onClose, evidenceList }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        
        {/* Header */}
        <div style={{ padding: '1.25rem 1.5rem', borderBottom: '1px solid rgba(59, 130, 246, 0.2)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: 'rgba(15, 23, 42, 0.95)' }}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '0.625rem', color: '#F8FAFC' }}>
            <FileText size={20} color="#60A5FA" />
            Grounded Evidence Observations ({evidenceList?.length || 0})
          </h3>
          <button onClick={onClose} style={{ color: '#94A3B8', padding: '0.25rem', borderRadius: '6px' }}>
            <X size={20} />
          </button>
        </div>

        {/* Body */}
        <div style={{ padding: '1.5rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {!evidenceList || evidenceList.length === 0 ? (
            <p style={{ color: '#64748B', fontSize: '0.875rem' }}>No evidence observations attached.</p>
          ) : (
            evidenceList.map((ev, idx) => (
              <div
                key={ev.id || idx}
                style={{ background: 'rgba(11, 15, 25, 0.9)', border: '1px solid rgba(59, 130, 246, 0.25)', borderRadius: '12px', padding: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94A3B8' }}>
                  <span style={{ fontFamily: 'monospace', color: '#60A5FA' }}>ID: {ev.id}</span>
                  <span>Session: {ev.session_id}</span>
                </div>

                <p style={{ fontSize: '0.9375rem', color: '#F8FAFC', lineHeight: '1.5', background: 'rgba(15, 23, 42, 0.9)', padding: '0.875rem', borderRadius: '8px', borderLeft: '3px solid #3B82F6', fontStyle: 'italic' }}>
                  "{ev.text}"
                </p>

                <div style={{ fontSize: '0.75rem', color: '#64748B', display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                  <Calendar size={12} color="#60A5FA" />
                  <span>Observed At: {new Date(ev.observed_at).toLocaleString()}</span>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div style={{ padding: '1rem 1.5rem', borderTop: '1px solid rgba(59, 130, 246, 0.2)', display: 'flex', justifyContent: 'flex-end', background: 'rgba(15, 23, 42, 0.95)' }}>
          <button className="btn btn-secondary" onClick={onClose}>Close</button>
        </div>

      </div>
    </div>
  );
}
