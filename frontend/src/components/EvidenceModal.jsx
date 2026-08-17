import React from 'react';
import { X, FileText, Calendar, Layers } from 'lucide-react';

export default function EvidenceModal({ isOpen, onClose, evidenceList }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        
        {/* Header */}
        <div style={{ padding: '1.25rem 1.5rem', borderBottom: '1px solid #232A3D', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#F3F4F6' }}>
            <FileText size={20} color="#3B82F6" />
            Grounded Evidence Observations ({evidenceList?.length || 0})
          </h3>
          <button onClick={onClose} style={{ color: '#9CA3AF', padding: '0.25rem', borderRadius: '6px' }}>
            <X size={20} />
          </button>
        </div>

        {/* Body */}
        <div style={{ padding: '1.5rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {!evidenceList || evidenceList.length === 0 ? (
            <p style={{ color: '#6B7280', fontSize: '0.875rem' }}>No evidence observations attached.</p>
          ) : (
            evidenceList.map((ev, idx) => (
              <div
                key={ev.id || idx}
                style={{ background: '#0D1017', border: '1px solid #232A3D', borderRadius: '10px', padding: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#9CA3AF' }}>
                  <span style={{ fontFamily: 'monospace' }}>Observation ID: {ev.id}</span>
                  <span>Session: {ev.session_id}</span>
                </div>

                <p style={{ fontSize: '0.9375rem', color: '#F3F4F6', lineHeight: '1.5', background: '#131722', padding: '0.75rem', borderRadius: '6px', borderLeft: '3px solid #3B82F6' }}>
                  "{ev.text}"
                </p>

                <div style={{ fontSize: '0.75rem', color: '#6B7280', display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                  <Calendar size={12} />
                  <span>Observed At: {new Date(ev.observed_at).toLocaleString()}</span>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div style={{ padding: '1rem 1.5rem', borderTop: '1px solid #232A3D', display: 'flex', justifyContent: 'flex-end' }}>
          <button className="btn btn-secondary" onClick={onClose}>Close</button>
        </div>

      </div>
    </div>
  );
}
