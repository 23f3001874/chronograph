import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import TemporalQueryView from './components/TemporalQueryView';
import TimelineView from './components/TimelineView';
import LineageGraphView from './components/LineageGraphView';
import IngestionView from './components/IngestionView';
import EvidenceModal from './components/EvidenceModal';
import { checkHealth, loadDemoScenario } from './api';

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

  // Load Preset 1: VS Code -> Cursor -> VS Code
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

  // Load Preset 2: Overlapping Contradiction
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

  // Load Preset 3: Absent Query (UNKNOWN)
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
    <div className="app-container">
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        healthStatus={healthStatus}
        onLoadEditorScenario={handleLoadEditorScenario}
        onLoadContradictionScenario={handleLoadContradictionScenario}
        onLoadAbsentQuery={handleLoadAbsentQuery}
      />

      <main style={{ flex: 1 }}>
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
      </main>

      <EvidenceModal
        isOpen={evidenceModalOpen}
        onClose={() => setEvidenceModalOpen(false)}
        evidenceList={evidenceModalData}
      />
    </div>
  );
}
