import React, { useState } from 'react';
import { Clock, AlertTriangle, HelpCircle, ArrowRight, ShieldAlert } from 'lucide-react';

export default function ProblemSection() {
  const [selectedTimeline, setSelectedTimeline] = useState(0);

  const timelineEvents = [
    { date: 'JAN 20, 2025', value: 'VS Code', status: 'SUPPORTED', desc: 'Active preference established at t0.' },
    { date: 'FEB 20, 2025', value: 'Cursor', status: 'SUPERSEDED', desc: 'Cursor preference supersedes VS Code at t1.' },
    { date: 'MAR 20, 2025', value: 'VS Code', status: 'ACTIVE', desc: 'Reversion back to VS Code supersedes Cursor at t2.' }
  ];

  return (
    <section id="why-chronograph" style={{ padding: '6rem 0 4rem 0', borderTop: '1px solid #141A24', background: '#05070B' }}>
      <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '4rem' }}>
        
        {/* THREE PROBLEM CARDS: 01 TIME, 02 CONFLICT, 03 UNCERTAINTY */}
        <div>
          <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.875rem', alignItems: 'center', marginBottom: '3rem' }}>
            <span className="mono-tag" style={{ color: '#FF7A18' }}>
              WHY CHRONOGRAPH?
            </span>
            <h2 style={{ fontSize: '3rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
              Three Fundamental Memory Failures
            </h2>
            <p style={{ fontSize: '1.125rem', color: '#8B95A5', maxWidth: '720px', lineHeight: '1.6' }}>
              Standard RAG treats all memories as flat text chunks, ignoring time, disagreement, and missing facts.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.75rem' }}>
            
            {/* 01 TIME */}
            <div style={{ background: '#080C12', border: '1px solid #1F2838', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.25rem', transition: 'all 0.25s ease' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="mono-tag" style={{ color: '#FF7A18', fontSize: '1.125rem' }}>01</span>
                <Clock size={20} color="#FF7A18" />
              </div>
              <h3 style={{ fontSize: '1.375rem', fontWeight: '800', color: '#FFFFFF' }}>TIME</h3>
              <p style={{ fontSize: '0.9375rem', color: '#8B95A5', lineHeight: '1.6' }}>
                "What was true THEN?" Naive vector search returns March memories when queried about January, leaking future facts.
              </p>
              <div style={{ background: '#04060A', border: '1px solid #FF7A18', borderRadius: '8px', padding: '0.75rem', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#FF9F43', fontWeight: '700' }}>
                CHRONOGRAPH: POINT-IN-TIME RESOLUTION (T)
              </div>
            </div>

            {/* 02 CONFLICT */}
            <div style={{ background: '#080C12', border: '1px solid #1F2838', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.25rem', transition: 'all 0.25s ease' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="mono-tag" style={{ color: '#FF4D5E', fontSize: '1.125rem' }}>02</span>
                <AlertTriangle size={20} color="#FF4D5E" />
              </div>
              <h3 style={{ fontSize: '1.375rem', fontWeight: '800', color: '#FFFFFF' }}>CONFLICT</h3>
              <p style={{ fontSize: '0.9375rem', color: '#8B95A5', lineHeight: '1.6' }}>
                "What happens when memory disagrees?" Naive systems silently pick an arbitrary winner instead of flagging a conflict.
              </p>
              <div style={{ background: '#04060A', border: '1px solid #FF4D5E', borderRadius: '8px', padding: '0.75rem', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#FF4D5E', fontWeight: '700' }}>
                CHRONOGRAPH: CONFLICTED STATE (0.5 CONF)
              </div>
            </div>

            {/* 03 UNCERTAINTY */}
            <div style={{ background: '#080C12', border: '1px solid #1F2838', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.25rem', transition: 'all 0.25s ease' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="mono-tag" style={{ color: '#00D9FF', fontSize: '1.125rem' }}>03</span>
                <HelpCircle size={20} color="#00D9FF" />
              </div>
              <h3 style={{ fontSize: '1.375rem', fontWeight: '800', color: '#FFFFFF' }}>UNCERTAINTY</h3>
              <p style={{ fontSize: '0.9375rem', color: '#8B95A5', lineHeight: '1.6' }}>
                "What if there is no evidence?" Standard RAG hallucinates a guess. ChronoGraph deterministically abstains.
              </p>
              <div style={{ background: '#04060A', border: '1px solid #00D9FF', borderRadius: '8px', padding: '0.75rem', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", color: '#00D9FF', fontWeight: '700' }}>
                CHRONOGRAPH: UNKNOWN ABSTENTION (0.0 CONF)
              </div>
            </div>

          </div>
        </div>

        {/* TEMPORAL TIMELINE SECTION: SAME MEMORY. DIFFERENT TIME. */}
        <div style={{ background: '#070A10', border: '1px solid #1F2838', borderRadius: '16px', padding: '2.5rem', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '0.5rem', alignItems: 'center' }}>
            <span className="mono-tag" style={{ color: '#00D9FF' }}>VISUAL TIMELINE IDENTIFIER</span>
            <h2 style={{ fontSize: '2.5rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif" }}>
              Same memory. Different time.
            </h2>
            <p style={{ fontSize: '1rem', color: '#8B95A5', maxWidth: '640px' }}>
              The answer changes because time changes — not because memory was overwritten or erased.
            </p>
          </div>

          {/* Horizontal Timeline Component */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem', position: 'relative', marginTop: '1rem' }}>
            {timelineEvents.map((ev, idx) => (
              <div
                key={idx}
                onClick={() => setSelectedTimeline(idx)}
                style={{
                  background: selectedTimeline === idx ? 'rgba(255, 122, 24, 0.12)' : '#04060A',
                  border: selectedTimeline === idx ? '1px solid #FF7A18' : '1px solid #141A24',
                  borderRadius: '12px', padding: '1.5rem', cursor: 'pointer', transition: 'all 0.25s ease',
                  display: 'flex', flexDirection: 'column', gap: '0.75rem'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace" }}>
                  <span style={{ color: '#8B95A5' }}>{ev.date}</span>
                  <span style={{
                    color: ev.status === 'ACTIVE' ? '#35D07F' : '#FF9F43',
                    background: ev.status === 'ACTIVE' ? 'rgba(53, 208, 127, 0.15)' : 'rgba(255, 159, 67, 0.15)',
                    padding: '0.15rem 0.5rem', borderRadius: '4px', fontWeight: '700'
                  }}>
                    {ev.status}
                  </span>
                </div>

                <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#FFFFFF' }}>
                  "{ev.value}"
                </div>

                <p style={{ fontSize: '0.8125rem', color: '#8B95A5', lineHeight: '1.4' }}>
                  {ev.desc}
                </p>
              </div>
            ))}
          </div>

        </div>

      </div>
    </section>
  );
}
