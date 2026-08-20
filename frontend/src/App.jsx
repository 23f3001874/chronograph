import React, { useState, useEffect } from 'react';
import HeaderNav from './components/landing/HeaderNav';
import HeroSection from './components/landing/HeroSection';
import ProblemSection from './components/landing/ProblemSection';
import CoreDifferenceSection from './components/landing/CoreDifferenceSection';
import InteractiveBeliefEvolver from './components/landing/InteractiveBeliefEvolver';
import EpistemicStatesSection from './components/landing/EpistemicStatesSection';
import EvidenceLineageSection from './components/landing/EvidenceLineageSection';
import ArchitectureSection from './components/landing/ArchitectureSection';
import BeliefReplaySection from './components/landing/BeliefReplaySection';
import BenchmarkSection from './components/landing/BenchmarkSection';
import HydraDBSection from './components/landing/HydraDBSection';
import ClosingSection from './components/landing/ClosingSection';
import FooterSection from './components/landing/FooterSection';

import TemporalQueryView from './components/TemporalQueryView';
import TimelineView from './components/TimelineView';
import LineageGraphView from './components/LineageGraphView';
import IngestionView from './components/IngestionView';
import EvidenceModal from './components/EvidenceModal';

import { checkHealth, loadDemoScenario } from './api';
import { Search, Clock, GitBranch, PlusCircle, Zap } from 'lucide-react';

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

  const scrollToStudio = () => {
    const el = document.getElementById('interactive-studio');
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSelectBeliefForLineage = (beliefId) => {
    setSelectedBeliefId(beliefId);
    setActiveTab('lineage');
    scrollToStudio();
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
      scrollToStudio();
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
      scrollToStudio();
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
      scrollToStudio();
    } catch (err) {
      alert('Error loading absent scenario: ' + err.message);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: '#040508', color: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
      
      {/* STICKY MINIMAL NAVIGATION */}
      <HeaderNav
        healthStatus={healthStatus}
        onLaunchDemo={scrollToStudio}
      />

      {/* 1. HERO SECTION (INTERACTIVE TEMPORAL BELIEF GRAPH) */}
      <HeroSection
        onExploreGraph={scrollToStudio}
      />

      {/* 2. THE PROBLEM ("Memory without time is not memory.") */}
      <ProblemSection />

      {/* 3. THE CORE DIFFERENCE (NAIVE VS CHRONOGRAPH MATRIX) */}
      <CoreDifferenceSection />

      {/* 4. CORE CHRONOGRAPH VISUALIZATION ("Don't retrieve the latest memory. Resolve what was true.") */}
      <InteractiveBeliefEvolver />

      {/* 5. CINEMATIC BELIEF REPLAY ("PLAY MEMORY") */}
      <BeliefReplaySection />

      {/* 6. EPISTEMIC STATES & INTERACTIVE UNKNOWN/CONFLICTED DEMOS */}
      <EpistemicStatesSection />

      {/* 7. EVIDENCE & LINEAGE ("Every belief has a history") */}
      <EvidenceLineageSection />

      {/* 8. ARCHITECTURE ("From memory to belief") */}
      <ArchitectureSection />

      {/* 9. BENCHMARK PROOF ("Temporal reasoning changes the answer") */}
      <BenchmarkSection />

      {/* 10. BUILT ON HYDRADB SUBSTRATE */}
      <HydraDBSection />

      {/* 11. INTERACTIVE DEVELOPER STUDIO CONSOLE */}
      <section id="interactive-studio" style={{ padding: '6rem 0 4rem 0', background: '#030509', borderTop: '1px solid #141822', scrollMarginTop: '4rem' }}>
        <div className="section-container" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          <div style={{ borderBottom: '1px solid #1F2430', paddingBottom: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: '1.5rem' }}>
            <div>
              <span className="mono-tag" style={{ color: '#34D399' }}>DEVELOPER WORKSPACE</span>
              <h2 style={{ fontSize: '2.5rem', fontWeight: '800', fontFamily: "'Space Grotesk', sans-serif", marginTop: '0.25rem' }}>
                Interactive ChronoGraph Studio
              </h2>
              <p style={{ fontSize: '0.9375rem', color: '#94A3B8', marginTop: '0.25rem' }}>
                Execute point-in-time queries (T), inspect belief evolution timelines, traverse cycle-safe lineage graphs, and ingest memory statements.
              </p>
            </div>

            {/* Presets Bar */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.75rem', color: '#64748B', fontFamily: "'JetBrains Mono', monospace", fontWeight: '700' }}>QUICK PRESETS:</span>
              <button className="btn-infrastructure btn-infrastructure-secondary" style={{ padding: '0.4rem 0.75rem', fontSize: '0.75rem' }} onClick={handleLoadEditorScenario}>
                <Zap size={13} color="#FF7A18" />
                VS Code → Cursor
              </button>
              <button className="btn-infrastructure btn-infrastructure-secondary" style={{ padding: '0.4rem 0.75rem', fontSize: '0.75rem' }} onClick={handleLoadContradictionScenario}>
                <Zap size={13} color="#FF4D5E" />
                CONFLICTED State
              </button>
              <button className="btn-infrastructure btn-infrastructure-secondary" style={{ padding: '0.4rem 0.75rem', fontSize: '0.75rem' }} onClick={handleLoadAbsentQuery}>
                <Zap size={13} color="#00D9FF" />
                UNKNOWN Fact
              </button>
            </div>
          </div>

          {/* Navigation Bar inside Studio */}
          <nav style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              className={`btn-infrastructure ${activeTab === 'query' ? 'btn-infrastructure-primary' : 'btn-infrastructure-secondary'}`}
              onClick={() => setActiveTab('query')}
            >
              <Search size={16} />
              Point-in-Time Query Playground (T)
            </button>
            <button
              className={`btn-infrastructure ${activeTab === 'timeline' ? 'btn-infrastructure-primary' : 'btn-infrastructure-secondary'}`}
              onClick={() => setActiveTab('timeline')}
            >
              <Clock size={16} />
              Belief Evolution Timeline
            </button>
            <button
              className={`btn-infrastructure ${activeTab === 'lineage' ? 'btn-infrastructure-primary' : 'btn-infrastructure-secondary'}`}
              onClick={() => setActiveTab('lineage')}
            >
              <GitBranch size={16} />
              Lineage Transition Graph
            </button>
            <button
              className={`btn-infrastructure ${activeTab === 'ingest' ? 'btn-infrastructure-primary' : 'btn-infrastructure-secondary'}`}
              onClick={() => setActiveTab('ingest')}
            >
              <PlusCircle size={16} />
              Memory Ingestion Studio
            </button>
          </nav>

          {/* Studio Tab Views */}
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

        </div>
      </section>

      {/* Grounded Evidence Modal */}
      <EvidenceModal
        isOpen={evidenceModalOpen}
        onClose={() => setEvidenceModalOpen(false)}
        evidenceList={evidenceModalData}
      />

      {/* 12. CLOSING SECTION ("AI shouldn't just remember.") */}
      <ClosingSection onLaunchDemo={scrollToStudio} />

      {/* 13. FOOTER SECTION */}
      <FooterSection />

    </div>
  );
}
