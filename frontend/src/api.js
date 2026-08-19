const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    if (!res.ok) return { status: 'error' };
    return await res.json();
  } catch (err) {
    return { status: 'offline', error: err.message };
  }
}

export async function queryTemporalState(subjectId, predicate, timestamp = null, includeEvidence = true, includeLineage = true) {
  const payload = {
    subject_id: subjectId,
    predicate: predicate,
    timestamp: timestamp,
    include_evidence: includeEvidence,
    include_lineage: includeLineage,
  };

  const res = await fetch(`${API_BASE_URL}/api/v1/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Query execution failed');
  }

  return await res.json();
}

export async function getTimeline(subjectId, predicate) {
  const res = await fetch(`${API_BASE_URL}/api/v1/timeline/${subjectId}/${predicate}`);
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Timeline retrieval failed');
  }
  return await res.json();
}

export async function getBeliefDetail(beliefId) {
  const res = await fetch(`${API_BASE_URL}/api/v1/beliefs/${beliefId}`);
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Belief detail retrieval failed');
  }
  return await res.json();
}

export async function getEvidence(beliefId) {
  const res = await fetch(`${API_BASE_URL}/api/v1/beliefs/${beliefId}/evidence`);
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Evidence retrieval failed');
  }
  return await res.json();
}

export async function getLineage(beliefId) {
  const res = await fetch(`${API_BASE_URL}/api/v1/beliefs/${beliefId}/lineage`);
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Lineage retrieval failed');
  }
  return await res.json();
}

export async function ingestMemory(collection, sessionId, text, timestamp = null) {
  const payload = {
    collection: collection,
    session_id: sessionId,
    text: text,
    timestamp: timestamp,
  };

  const res = await fetch(`${API_BASE_URL}/api/v1/ingest`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Ingestion failed');
  }

  return await res.json();
}

export async function loadDemoScenario() {
  const res = await fetch(`${API_BASE_URL}/api/v1/demo/load`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Demo load failed');
  }

  return await res.json();
}
