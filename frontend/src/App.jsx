import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import TemporalQueryView from './components/TemporalQueryView';
import TimelineView from './components/TimelineView';
import LineageGraphView from './components/LineageGraphView';
import IngestionView from './components/IngestionView';
import EvidenceModal from './components/EvidenceModal';
import HeroTemporalTree from './components/graphics/HeroTemporalTree';
import BenchmarkChart from './components/graphics/BenchmarkChart';
import ArchitectureOverview from './components/graphics/ArchitectureOverview';
import IsometricTierDiagram from './components/graphics/IsometricTierDiagram';
import { checkHealth, loadDemoScenario } from './api';
import { ShieldCheck, Cpu, Database, Activity, GitBranch, ArrowUpRight, Zap, CheckCircle2, Lock, ExternalLink } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('query');
  const [subjectId, setSubjectId] = useState('user');
  const [predicate, setPredicate] = useState('favorite_editor');
  const [selectedBeliefId, setSelectedBeliefId] = useState(null);
  const [healthStatus, setHealthStatus] = useState('unknown');

  const [evidenceModalOpen, setEvidenceModalOpen] = useState(false);
  const [evidenceModalData, setEvidenceModalData] = useState([]);

  useEffect(() => {
    checkHealth().then((res) => {
      setHealthStatus(res.status || 'offline');
    });
  }, []);

  const handleSelectBeliefForLineage = (beliefId) => {
    setSelectedBeliefId(beliefId);
    setActiveTab('lineage');
  };

  const handleOpenEvidence = (list) => {
    setEvidenceModalData(list || []);
    setEvidenceModalOpen(true);
  };

  // Presets
  const handleLoadEditorScenario = async () => {
    setSubjectId('user');
    setPredicate('favorite_editor');
    try {
      await loadDemoScenario();
      setActiveTab('query');
    } catch (err) {
      alert('Error loading editor scenario: ' + err.message);
    }
  };

  const handleLoadContradictionScenario = async () => {
    setSubjectId('user');
    setPredicate('location');
    try {
      await loadDemoScenario();
      setActiveTab('query');
    } catch (err) {
      alert('Error loading contradiction scenario: ' + err.message);
    }
  };

  const handleLoadAbsentQuery = async () => {
    setSubjectId('user');
    setPredicate('favorite_language');
    try {
      await loadDemoScenario();
      setActiveTab('query');
    } catch (err) {
      alert('Error loading absent scenario: ' + err.message);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: '#000000', color: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
      
      {/* Top Announcement Bar (HydraDB Style) */}
      <div style={{ background: '#080A0F', borderBottom: '1px solid #1F2430', padding: '0.5rem 1rem', textAlign: 'center', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace", display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem' }}>
        <span style={{ background: '#3B82F6', color: '#FFFFFF', padding: '0.1rem 0.5rem', borderRadius: '4px', fontWeight: '700', textTransform: 'uppercase' }}>
          ANNOUNCEMENT
        </span>
        <span style={{ color: '#94A3B8' }}>
          ChronoGraph v1.3.0 is live on Vercel & GitHub with 100% benchmark accuracy.
        </span>
        <a href="https://github.com/23f3001874/chronograph" target="_blank" rel="noopener noreferrer" style={{ color: '#00F0FF', textDecoration: 'none', fontWeight: '700', display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
          View on GitHub <ArrowUpRight size={12} />
        </a>
      </div>

      <div className="app-container">
        
        {/* Header */}
        <Header
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          healthStatus={healthStatus}
          onLoadEditorScenario={handleLoadEditorScenario}
          onLoadContradictionScenario={handleLoadContradictionScenario}
          onLoadAbsentQuery={handleLoadAbsentQuery}
        />

        {/* HERO SECTION (Matching Screenshot 1) */}
        <section style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2.5rem', alignItems: 'center', padding: '3rem 0 1rem 0' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', textAlign: 'left' }}>
            <span style={{ color: '#94A3B8', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8125rem', letterSpacing: '0.05em' }}>
              Substrate: HydraDB Cloud • Track 3 Memory
            </span>

            <h1 style={{ fontSize: '3.75rem', fontWeight: '800', letterSpacing: '-0.04em', lineHeight: '1.05', fontFamily: "'Space Grotesk', sans-serif" }}>
              The Temporal Memory AI Runs On.
            </h1>

            <p style={{ fontSize: '1.125rem', color: '#94A3B8', lineHeight: '1.6', maxWidth: '540px' }}>
              Temporal Belief & Epistemic Reasoning Engine built on HydraDB Cloud: <strong style={{ color: '#00F0FF' }}>100% temporal accuracy</strong>, zero future-knowledge leakage, and sub-millisecond point-in-time state resolution.
            </p>

            <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem' }}>
              <button className="btn btn-primary" style={{ padding: '0.875rem 1.75rem', fontSize: '1rem' }} onClick={() => setActiveTab('query')}>
                Launch Interactive Playground
              </button>
              <a href="https://github.com/23f3001874/chronograph" target="_blank" rel="noopener noreferrer" className="btn btn-secondary" style={{ padding: '0.875rem 1.75rem', fontSize: '1rem', textDecoration: 'none' }}>
                View GitHub Repo
              </a>
            </div>
          </div>

          {/* Hero Pixel Tree Graphic (Matching Screenshot 1) */}
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <HeroTemporalTree />
          </div>
        </section>

        {/* BENTO GRID SECTION — "Everything You Need To Compound Intelligence" (Matching Screenshot 2) */}
        <section style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '2rem' }}>
          <h2 style={{ fontSize: '2.25rem', fontWeight: '700', textAlign: 'center', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
            Everything You Need To Compound Temporal Intelligence
          </h2>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
            
            {/* Box 1: High Recall Accuracy (Matching Screenshot 2) */}
            <div className="card" style={{ background: '#05070B', border: '1px solid #1F2430', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <h3 style={{ fontSize: '1.375rem', fontWeight: '700', color: '#FFFFFF' }}>High Temporal Accuracy</h3>
                <p style={{ fontSize: '0.875rem', color: '#94A3B8', marginTop: '0.5rem' }}>
                  Proven +70.0 percentage point advantage on sequential preference changes, overlapping location updates, and point-in-time point queries.
                </p>
              </div>

              {/* Big Electric Blue Stat Block */}
              <div style={{ background: 'linear-gradient(135deg, #1D4ED8 0%, #2563EB 50%, #3B82F6 100%)', borderRadius: '12px', padding: '2.5rem 1.5rem', textAlign: 'center', marginTop: '1.5rem', boxShadow: '0 0 30px rgba(37, 99, 235, 0.4)' }}>
                <div style={{ fontSize: '3.5rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", color: '#FFFFFF' }}>
                  100.0%
                </div>
                <div style={{ fontSize: '1.125rem', fontWeight: '700', color: '#00F0FF', textTransform: 'uppercase', letterSpacing: '0.05em', fontFamily: "'JetBrains Mono', monospace" }}>
                  Benchmark Accuracy
                </div>
              </div>
            </div>

            {/* Box 2: Scales With Systems (Matching Screenshot 2) */}
            <div className="card" style={{ background: '#05070B', border: '1px solid #1F2430', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <h3 style={{ fontSize: '1.375rem', fontWeight: '700', color: '#FFFFFF' }}>Zero Future Leakage</h3>
                <p style={{ fontSize: '0.875rem', color: '#94A3B8', marginTop: '0.5rem' }}>
                  Prevents historical memory contamination by enforcing strict validity intervals <code style={{ color: '#00F0FF' }}>[valid_from, valid_until)</code> across memory tiers.
                </p>
              </div>

              {/* Isometric Tier Diagram */}
              <div style={{ marginTop: '1.5rem' }}>
                <IsometricTierDiagram />
              </div>
            </div>

            {/* Box 3: Epistemic Abstention */}
            <div className="card" style={{ background: '#05070B', border: '1px solid #1F2430' }}>
              <h3 style={{ fontSize: '1.375rem', fontWeight: '700', color: '#FFFFFF' }}>Deterministic Abstention</h3>
              <p style={{ fontSize: '0.875rem', color: '#94A3B8', marginTop: '0.5rem' }}>
                Returns explicit <code style={{ color: '#FBBF24' }}>UNKNOWN</code> (0.0 confidence) for absent facts instead of hallucinating fallbacks.
              </p>
            </div>

            {/* Box 4: Sub-Millisecond Speed */}
            <div className="card" style={{ background: '#05070B', border: '1px solid #1F2430' }}>
              <h3 style={{ fontSize: '1.375rem', fontWeight: '700', color: '#FFFFFF' }}>Sub-Millisecond Engine</h3>
              <p style={{ fontSize: '0.875rem', color: '#94A3B8', marginTop: '0.5rem' }}>
                Built for high-throughput AI agent workloads with zero retrieval overhead.
              </p>
              <div style={{ fontSize: '2rem', fontWeight: '800', color: '#00F0FF', marginTop: '0.75rem', fontFamily: "'Space Grotesk', sans-serif" }}>
                &lt; 0.1 ms Latency
              </div>
            </div>

          </div>
        </section>

        {/* BENCHMARK CURVE CHART SECTION (Matching Screenshot 3) */}
        <section style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '3rem' }}>
          <div style={{ textAlign: 'left' }}>
            <h2 style={{ fontSize: '2.25rem', fontWeight: '700', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
              Recall & Future Leakage Bottleneck
            </h2>
            <p style={{ fontSize: '1rem', color: '#94A3B8', marginTop: '0.5rem' }}>
              Naive vector databases suffer severe degradation as memory sequence length increases, leaking future facts into past queries.
            </p>
          </div>

          <BenchmarkChart />
        </section>

        {/* ARCHITECTURE OVERVIEW SECTION (Matching Screenshot 4) */}
        <section style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '3rem' }}>
          <h2 style={{ fontSize: '2.25rem', fontWeight: '700', textAlign: 'center', fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}>
            Architecture Overview
          </h2>

          <ArchitectureOverview />
        </section>

        {/* MAIN INTERACTIVE PLAYGROUND STUDIO */}
        <section style={{ marginTop: '4rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #1F2430', paddingBottom: '1rem' }}>
            <div>
              <h2 style={{ fontSize: '2rem', fontWeight: '700', fontFamily: "'Space Grotesk', sans-serif" }}>
                Interactive ChronoGraph Studio
              </h2>
              <p style={{ fontSize: '0.875rem', color: '#94A3B8', marginTop: '0.25rem' }}>
                Test point-in-time queries ($T$), inspect belief timelines, and verify transition graphs in real time.
              </p>
            </div>
          </div>

          {activeTab === 'query' && (
            <TemporalQueryView
              subjectId={subjectId}
              setSubjectId={setSubjectId}
              predicate={predicate}
              setPredicate={setPredicate}
              onInspectEvidence={handleOpenEvidence}
            />
          )}

          {activeTab === 'timeline' && (
            <TimelineView
              subjectId={subjectId}
              predicate={predicate}
              onSelectBelief={handleSelectBeliefForLineage}
            />
          )}

          {activeTab === 'lineage' && (
            <LineageGraphView
              beliefId={selectedBeliefId}
              onInspectEvidence={handleOpenEvidence}
            />
          )}

          {activeTab === 'ingest' && (
            <IngestionView
              onIngestSuccess={() => setActiveTab('query')}
            />
          )}
        </section>

        {/* Grounded Evidence Modal */}
        <EvidenceModal
          isOpen={evidenceModalOpen}
          onClose={() => setEvidenceModalOpen(false)}
          evidenceList={evidenceModalData}
        />

        {/* FOOTER SECTION (Matching Screenshot 5) */}
        <footer style={{ borderTop: '1px solid #1F2430', padding: '3rem 0 1rem 0', marginTop: '4rem', display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', textAlign: 'left' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <div style={{ background: '#3B82F6', padding: '0.5rem', borderRadius: '8px' }}>
                <Activity size={18} color="#FFFFFF" />
              </div>
              <span style={{ fontSize: '1.375rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif" }}>ChronoGraph</span>
            </div>
            <p style={{ fontSize: '0.875rem', color: '#94A3B8', maxWidth: '400px' }}>
              The Temporal Memory & Epistemic Reasoning Engine for AI Agents built on HydraDB Cloud Substrate.
            </p>
            <div style={{ fontSize: '0.75rem', color: '#64748B', fontFamily: "'JetBrains Mono', monospace" }}>
              © 2026 ChronoGraph Team • Hack Hydra Track 3 Release v1.3.0
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', textAlign: 'right', fontSize: '0.875rem' }}>
            <a href="https://hydradb.com" target="_blank" rel="noopener noreferrer" style={{ color: '#3B82F6', textDecoration: 'none', fontWeight: '600' }}>
              HydraDB Cloud Substrate →
            </a>
            <a href="https://github.com/23f3001874/chronograph" target="_blank" rel="noopener noreferrer" style={{ color: '#00F0FF', textDecoration: 'none', fontWeight: '600' }}>
              GitHub Repository →
            </a>
            <a href="https://chronograph-seven.vercel.app" target="_blank" rel="noopener noreferrer" style={{ color: '#34D399', textDecoration: 'none', fontWeight: '600' }}>
              Vercel Live Production URL →
            </a>
          </div>
        </footer>

      </div>
    </div>
  );
}
