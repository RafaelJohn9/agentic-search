"""
Tests for SerperSearchHandler using pytest standards.

This module tests the functionality of the SerperSearchHandler
without mocking, ensuring that credentials are working as expected.
"""

import pytest
from agent.services.serper_search_handler import SerperSearchHandler


@pytest.fixture
def handler() -> SerperSearchHandler:
    """Fixture to initialize the SerperSearchHandler."""
    return SerperSearchHandler()


def test_search_successful(handler: SerperSearchHandler) -> None:
    """Test a successful search query."""
    result = handler.search("Apple Inc")
    assert result is not None, "Expected a non-None result for a valid query."
    assert "knowledgeGraph" in result, "Expected 'knowledgeGraph' key in the result."
    assert result["knowledgeGraph"]["title"] == "Apple", (
        "Expected 'title' in 'knowledgeGraph' to match the query."
    )


def test_search_empty_query(handler: SerperSearchHandler) -> None:
    """Test that an empty query raises a ValueError."""
    with pytest.raises(ValueError, match="Search query cannot be empty."):
        handler.search("")
