import React, { useState } from 'react';
import { GitBranch, FileText, ArrowDown, ShieldCheck, CheckCircle2, AlertTriangle, HelpCircle } from 'lucide-react';

export default function InteractiveBeliefEvolver() {
  const [hoveredNode, setHoveredNode] = useState(null);

  const beliefNodes = [
    {
      id: 'obs_1',
      type: 'OBSERVATION',
      label: 'Observation #1',
      value: '"I use VS Code for development."',
      timestamp: '2025-01-20T00:00:00Z',
      edgeLabel: 'GROUNDED_IN',
      edgeColor: '#3B82F6',
      details: {
        id: 'obs_1',
        source: 'Session #101',
        rawText: 'I use VS Code for development.',
        timestamp: 'Jan 20, 2025'
      }
    },
    {
      id: 'b1_vscode',
      type: 'BELIEF',
      label: 'Belief v1 (VS Code)',
      value: 'VS Code',
      status: 'SUPERSEDED',
      validFrom: 'Jan 20, 2025',
      validUntil: 'Feb 20, 2025',
      confidence: '0.90',
      edgeLabel: 'SUPERSEDES',
      edgeColor: '#FBBF24',
      details: {
        beliefId: 'b1_vscode',
        value: 'VS Code',
        status: 'SUPERSEDED',
        validFrom: '2025-01-20',
        validUntil: '2025-02-20',
        confidence: 0.90,
        source: 'Observation obs_1'
      }
    },
    {
      id: 'b2_cursor',
      type: 'BELIEF',
      label: 'Belief v2 (Cursor)',
      value: 'Cursor',
      status: 'SUPERSEDED',
      validFrom: 'Feb 20, 2025',
      validUntil: 'Mar 20, 2025',
      confidence: '0.90',
      edgeLabel: 'SUPERSEDES',
      edgeColor: '#FBBF24',
      details: {
        beliefId: 'b2_cursor',
        value: 'Cursor',
        status: 'SUPERSEDED',
        validFrom: '2025-02-20',
        validUntil: '2025-03-20',
        confidence: 0.90,
        source: 'Observation obs_2'
      }
    },
    {
      id: 'b3_vscode',
      type: 'BELIEF',
      label: 'Belief v3 (VS Code Reversion)',
      value: 'VS Code',
      status: 'ACTIVE',
      validFrom: 'Mar 20, 2025',
      validUntil: 'Present (Ongoing)',
      confidence: '0.95',
      edgeLabel: 'GROUNDED_IN EVIDENCE',
      edgeColor: '#34D399',
      details: {
        beliefId: 'b3_vscode',
        value: 'VS Code',
        status: 'ACTIVE',
        validFrom: '2025-03-20',
        validUntil: 'Present',
        confidence: 0.95,
        source: 'Observation obs_3'
      }
    }
  ];

  return (
    <section id="belief-graph" style={{ padding: '6rem 0 4rem 0', background: '#020408', borderTop: '1px solid #141822' }}>
      <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
        
        {/* Section Header */}
        <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.875rem', alignItems: 'center' }}>
          <span className="mono-tag" style={{ color: '#00F0FF' }}>
            GRAPH VISUALIZATION
          </span>
          <h2 style={{ fontSize: '3rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
            Watch a belief evolve.
          </h2>
          <p style={{ fontSize: '1.125rem', color: '#94A3B8', maxWidth: '720px', lineHeight: '1.6' }}>
            Hover over any node in the temporal graph to inspect grounded observations, validity intervals, confidence scores, and edge relationships.
          </p>
        </div>

        {/* Technical Graph Interactive Display */}
        <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '2.5rem', alignItems: 'flex-start' }}>
          
          {/* LEFT: GRAPH NODE STACK */}
          <div style={{ background: '#06080F', border: '1px solid #1F2430', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #1A1D24', paddingBottom: '1rem' }}>
              <span className="mono-tag" style={{ color: '#60A5FA' }}>
                DIRECTED ACYCLIC BELIEF GRAPH
              </span>
              <span style={{ fontSize: '0.75rem', color: '#64748B', fontFamily: "'JetBrains Mono', monospace" }}>
                HOVER NODE TO INSPECT
              </span>
            </div>

            {beliefNodes.map((node, idx) => (
              <React.Fragment key={node.id}>
                
                {/* Node Box */}
                <div
                  onMouseEnter={() => setHoveredNode(node)}
                  onMouseLeave={() => setHoveredNode(null)}
                  style={{
                    background: hoveredNode?.id === node.id ? 'rgba(59, 130, 246, 0.15)' : '#090D16',
                    border: hoveredNode?.id === node.id ? '1px solid #00F0FF' : '1px solid #1F2430',
                    borderRadius: '12px', padding: '1.25rem', cursor: 'pointer', transition: 'all 0.25s ease',
                    boxShadow: hoveredNode?.id === node.id ? '0 0 25px rgba(0, 240, 255, 0.2)' : 'none'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
                      <span className="mono-tag" style={{
                        color: node.type === 'OBSERVATION' ? '#60A5FA' : (node.status === 'ACTIVE' ? '#34D399' : '#FBBF24'),
                        background: 'rgba(255,255,255,0.05)', padding: '0.15rem 0.5rem', borderRadius: '4px'
                      }}>
                        {node.type}
                      </span>
                      <span style={{ fontSize: '1.125rem', fontWeight: '800', color: '#FFFFFF' }}>
                        {node.value}
                      </span>
                    </div>

                    {node.status && (
                      <span className="mono-tag" style={{
                        color: node.status === 'ACTIVE' ? '#34D399' : '#FBBF24',
                        background: node.status === 'ACTIVE' ? 'rgba(52, 211, 153, 0.15)' : 'rgba(251, 191, 36, 0.15)',
                        padding: '0.15rem 0.5rem', borderRadius: '4px'
                      }}>
                        {node.status}
                      </span>
                    )}
                  </div>
                </div>

                {/* Directed Edge Connector */}
                {idx < beliefNodes.length - 1 && (
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.25rem' }}>
                    <span className="mono-tag" style={{ fontSize: '0.6875rem', color: node.edgeColor, background: 'rgba(255,255,255,0.03)', padding: '0.15rem 0.6rem', borderRadius: '9999px', border: `1px solid ${node.edgeColor}` }}>
                      {node.edgeLabel}
                    </span>
                    <ArrowDown size={18} color={node.edgeColor} />
                  </div>
                )}

              </React.Fragment>
            ))}

          </div>

          {/* RIGHT: INSPECTOR PANEL */}
          <div style={{ background: '#080B12', border: '1px solid #1E3A8A', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.25rem', minHeight: '380px' }}>
            
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', borderBottom: '1px solid #1E3A8A', paddingBottom: '1rem' }}>
              <GitBranch size={18} color="#00F0FF" />
              <span className="mono-tag" style={{ color: '#00F0FF' }}>
                GRAPH NODE METADATA INSPECTOR
              </span>
            </div>

            {hoveredNode ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8125rem' }}>
                <div style={{ color: '#94A3B8' }}>NODE ID: <strong style={{ color: '#FFFFFF' }}>{hoveredNode.details.id || hoveredNode.details.beliefId}</strong></div>
                <div style={{ color: '#94A3B8' }}>TYPE: <strong style={{ color: '#60A5FA' }}>{hoveredNode.type}</strong></div>
                <div style={{ color: '#94A3B8' }}>VALUE: <strong style={{ color: '#34D399' }}>{hoveredNode.value}</strong></div>
                {hoveredNode.details.validFrom && (
                  <div style={{ color: '#94A3B8' }}>INTERVAL: <strong style={{ color: '#00F0FF' }}>[{hoveredNode.details.validFrom}, {hoveredNode.details.validUntil})</strong></div>
                )}
                {hoveredNode.details.confidence && (
                  <div style={{ color: '#94A3B8' }}>CONFIDENCE: <strong style={{ color: '#34D399' }}>{hoveredNode.details.confidence}</strong></div>
                )}
                {hoveredNode.details.rawText && (
                  <div style={{ background: '#04060A', border: '1px solid #1F2430', padding: '0.875rem', borderRadius: '8px', color: '#E2E8F0', fontStyle: 'italic' }}>
                    "{hoveredNode.details.rawText}"
                  </div>
                )}
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '240px', color: '#64748B', gap: '0.75rem', textAlign: 'center' }}>
                <GitBranch size={36} opacity={0.3} color="#3B82F6" />
                <p style={{ fontSize: '0.875rem', color: '#94A3B8' }}>Hover over any node on the left to inspect detailed belief parameters, validity intervals, and source observations.</p>
              </div>
            )}

          </div>

        </div>

      </div>
    </section>
  );
}
