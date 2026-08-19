import React, { useState } from 'react';
import { PlusCircle, Database, CheckCircle2 } from 'lucide-react';
import { ingestMemory } from '../api';

export default function IngestionView({ onIngestSuccess }) {
  const [collection, setCollection] = useState('chronograph_demo');
  const [sessionId, setSessionId] = useState('session_interactive');
  const [text, setText] = useState('');
  const [timestamp, setTimestamp] = useState(new Date().toISOString().slice(0, 16));
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const isoTs = new Date(timestamp).toISOString();
      const res = await ingestMemory(collection, sessionId, text, isoTs);
      setResult(res);
      setText('');
      if (onIngestSuccess) onIngestSuccess();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: '680px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      <h2 className="card-title">
        <PlusCircle size={20} color="#60A5FA" />
        Ingest Memory Statement into HydraDB & ChronoGraph
      </h2>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div className="input-group">
            <label className="input-label">Collection Partition</label>
            <input
              className="input-control"
              value={collection}
              onChange={(e) => setCollection(e.target.value)}
              placeholder="e.g. chronograph_demo"
              required
            />
          </div>

          <div className="input-group">
            <label className="input-label">Session ID</label>
            <input
              className="input-control"
              value={sessionId}
              onChange={(e) => setSessionId(e.target.value)}
              placeholder="e.g. session_1"
              required
            />
          </div>
        </div>

        <div className="input-group">
          <label className="input-label">Observation Timestamp</label>
          <input
            type="datetime-local"
            className="input-control"
            value={timestamp}
            onChange={(e) => setTimestamp(e.target.value)}
            required
          />
        </div>

        <div className="input-group">
          <label className="input-label">Raw Memory Text Statement</label>
          <textarea
            className="input-control"
            style={{ minHeight: '90px', resize: 'vertical' }}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="e.g. I switched to VS Code and prefer VS Code for development."
            required
          />
        </div>

        <button type="submit" className="btn btn-primary" style={{ marginTop: '0.5rem' }} disabled={loading}>
          <Database size={16} />
          {loading ? 'Ingesting Memory...' : 'Ingest Memory & Normalize Belief'}
        </button>
      </form>

      {error && (
        <div style={{ padding: '0.875rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '10px', color: '#F87171', fontSize: '0.875rem' }}>
          {error}
        </div>
      )}

      {result && (
        <div style={{ padding: '1.125rem', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.35)', borderRadius: '12px', color: '#F8FAFC', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#34D399', fontWeight: '700' }}>
            <CheckCircle2 size={18} />
            Memory Statement Ingested Successfully!
          </div>
          <p style={{ fontSize: '0.8125rem', color: '#CBD5E1' }}>{result.message}</p>
          <div style={{ fontSize: '0.75rem', color: '#94A3B8', fontFamily: 'monospace', display: 'flex', flexDirection: 'column', gap: '0.25rem', marginTop: '0.25rem' }}>
            <div>Observation ID: {result.observation_ids?.join(', ')}</div>
            <div>Belief States Created: {result.belief_ids?.join(', ') || 'None'}</div>
          </div>
        </div>
      )}
    </div>
  );
}
