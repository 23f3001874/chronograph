import React, { useState } from 'react';
import { GitBranch, FileText, ArrowDown, ExternalLink, ShieldCheck } from 'lucide-react';

export default function EvidenceLineageSection() {
  const [selectedObs, setSelectedObs] = useState(null);

  const evidenceData = {
    id: 'obs_103',
    timestamp: '2025-03-20T09:15:00Z',
    sessionId: 'session_hack_hydra_303',
    sourceText: 'I switched back to VS Code. It is my favorite editor again.',
    groundedBelief: 'b3_vscode',
    predicate: 'favorite_editor',
    value: 'VS Code',
    confidence: '0.95',
    status: 'ACTIVE'
  };

  return (
    <section style={{ padding: '6rem 0 4rem 0', background: '#020408', borderTop: '1px solid #141822' }}>
      <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
        
        {/* Section Header */}
        <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.875rem', alignItems: 'center' }}>
          <span className="mono-tag" style={{ color: '#00F0FF' }}>
            AUDITABILITY & GROUNDING
          </span>
          <h2 style={{ fontSize: '3rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
            Every belief has a history.
          </h2>
          <p style={{ fontSize: '1.125rem', color: '#94A3B8', maxWidth: '720px', lineHeight: '1.6' }}>
            ChronoGraph maintains explicit grounded evidence links for every belief state, with full cycle-safe graph lineage traversal.
          </p>
        </div>

        {/* Visual Lineage Stack & Grounded Evidence Inspector */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2.5rem', alignItems: 'flex-start' }}>
          
          {/* LINEAGE STACK */}
          <div style={{ background: '#06080E', border: '1px solid #1F2430', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #1A1D24', paddingBottom: '1rem' }}>
              <span className="mono-tag" style={{ color: '#60A5FA' }}>BELIEF LINEAGE STACK</span>
              <span style={{ fontSize: '0.75rem', color: '#64748B', fontFamily: "'JetBrains Mono', monospace" }}>CYCLE-SAFE TRAVERSAL</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', alignItems: 'center' }}>
              
              {/* Belief 1 */}
              <div style={{ width: '100%', background: '#090D17', border: '1px solid #1F2430', borderRadius: '10px', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <span className="mono-tag" style={{ color: '#3B82F6' }}>v1 • VS CODE</span>
                  <div style={{ fontSize: '0.75rem', color: '#64748B', marginTop: '0.2rem', fontFamily: "'JetBrains Mono', monospace" }}>Valid: Jan 20 → Feb 20</div>
                </div>
                <span className="mono-tag" style={{ color: '#FBBF24', background: 'rgba(251, 191, 36, 0.15)', padding: '0.15rem 0.5rem', borderRadius: '4px' }}>SUPERSEDED</span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#60A5FA', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace" }}>
                <span>SUPERSEDES</span>
                <ArrowDown size={14} color="#60A5FA" />
              </div>

              {/* Belief 2 */}
              <div style={{ width: '100%', background: '#090D17', border: '1px solid #1F2430', borderRadius: '10px', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <span className="mono-tag" style={{ color: '#00F0FF' }}>v2 • CURSOR</span>
                  <div style={{ fontSize: '0.75rem', color: '#64748B', marginTop: '0.2rem', fontFamily: "'JetBrains Mono', monospace" }}>Valid: Feb 20 → Mar 20</div>
                </div>
                <span className="mono-tag" style={{ color: '#FBBF24', background: 'rgba(251, 191, 36, 0.15)', padding: '0.15rem 0.5rem', borderRadius: '4px' }}>SUPERSEDED</span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#60A5FA', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace" }}>
                <span>SUPERSEDES</span>
                <ArrowDown size={14} color="#60A5FA" />
              </div>

              {/* Belief 3 */}
              <div style={{ width: '100%', background: 'rgba(52, 211, 153, 0.1)', border: '1px solid #34D399', borderRadius: '10px', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <span className="mono-tag" style={{ color: '#34D399' }}>v3 • VS CODE</span>
                  <div style={{ fontSize: '0.75rem', color: '#34D399', marginTop: '0.2rem', fontFamily: "'JetBrains Mono', monospace" }}>Valid: Mar 20 → Present</div>
                </div>
                <span className="mono-tag" style={{ color: '#34D399', background: 'rgba(52, 211, 153, 0.2)', padding: '0.15rem 0.5rem', borderRadius: '4px' }}>ACTIVE</span>
              </div>

            </div>
          </div>

          {/* GROUNDED EVIDENCE INSPECTOR */}
          <div style={{ background: '#06080E', border: '1px solid #1E3A8A', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #1E3A8A', paddingBottom: '1rem' }}>
              <span className="mono-tag" style={{ color: '#00F0FF' }}>GROUNDED EVIDENCE OBSERVATION</span>
              <span style={{ fontSize: '0.75rem', color: '#34D399', fontFamily: "'JetBrains Mono', monospace" }}>EVIDENCE GROUNDED</span>
            </div>

            <div
              onClick={() => setSelectedObs(evidenceData)}
              style={{
                background: '#090D17', border: '1px solid rgba(59, 130, 246, 0.35)', borderRadius: '12px', padding: '1.25rem',
                cursor: 'pointer', display: 'flex', flexDirection: 'column', gap: '0.75rem', transition: 'all 0.2s ease'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94A3B8', fontFamily: "'JetBrains Mono', monospace" }}>
                <span>Observed: Mar 20, 2025</span>
                <span style={{ color: '#60A5FA' }}>ID: {evidenceData.id}</span>
              </div>
              <p style={{ fontSize: '0.9375rem', color: '#F8FAFC', fontStyle: 'italic', lineHeight: '1.5' }}>
                "{evidenceData.sourceText}"
              </p>
              <div style={{ fontSize: '0.75rem', color: '#34D399', fontFamily: "'JetBrains Mono', monospace", fontWeight: '700' }}>
                Click to inspect grounded evidence details →
              </div>
            </div>

            {/* Evidence Modal / Detail Card */}
            {selectedObs && (
              <div style={{ background: '#030509', border: '1px solid #34D399', borderRadius: '12px', padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.75rem', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8125rem' }}>
                <div style={{ color: '#34D399', fontWeight: '700' }}>EVIDENCE GROUNDING DETAIL:</div>
                <div style={{ color: '#CBD5E1' }}>OBSERVATION ID: <span style={{ color: '#60A5FA' }}>{selectedObs.id}</span></div>
                <div style={{ color: '#CBD5E1' }}>TIMESTAMP: <span style={{ color: '#00F0FF' }}>{selectedObs.timestamp}</span></div>
                <div style={{ color: '#CBD5E1' }}>SESSION: <span style={{ color: '#CBD5E1' }}>{selectedObs.sessionId}</span></div>
                <div style={{ color: '#CBD5E1' }}>GROUNDED BELIEF: <span style={{ color: '#34D399' }}>{selectedObs.groundedBelief}</span></div>
                <div style={{ color: '#CBD5E1' }}>CONFIDENCE: <span style={{ color: '#34D399' }}>{selectedObs.confidence} (95%)</span></div>
              </div>
            )}

          </div>

        </div>

      </div>
    </section>
  );
}
