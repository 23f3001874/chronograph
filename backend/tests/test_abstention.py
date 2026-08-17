"""Tests for abstention and explicit UNKNOWN responses."""

from datetime import datetime, timezone
import pytest

from app.engine.abstention import check_abstention
from app.engine.store import ChronoGraphStore
from app.models.domain import ResolutionStatus


def test_scenario_f_unknown_abstention():
    """Scenario F: Querying an absent predicate returns status UNKNOWN and 0.0 confidence."""
    store = ChronoGraphStore()
    now = datetime(2025, 6, 1, tzinfo=timezone.utc)

    result = check_abstention(store, "user", "favorite_language", now)

    assert result is not None
    assert result.status == ResolutionStatus.UNKNOWN
    assert result.confidence == 0.0
    assert "No recorded evidence" in result.reason
    assert result.evidence_ids == []
    assert result.beliefs == []
