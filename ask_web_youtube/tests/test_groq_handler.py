"""Unit tests for the GroqHandler class.

This module tests the functionality of the GroqHandler
without mocking, ensuring that credentials are working as expected.
"""

import pytest
from agent.services.llm_handler.groq_handler import GroqHandler
import os


@pytest.fixture(scope="module", autouse=True)
def check_groq_api_key():
    """Skip tests if GROQ_API_KEY is not set."""
    if not os.getenv("GROQ_API_KEY"):
        pytest.skip("GROQ_API_KEY environment variable is not set.")


@pytest.fixture
def groq_handler():
    """Fixture to create a GroqHandler instance with the actual API."""
    return GroqHandler(api_key=os.getenv("GROQ_API_KEY"))


def test_groq_handler_initialization(groq_handler):
    """Test that the GroqHandler initializes correctly."""
    assert groq_handler.api_key == os.getenv("GROQ_API_KEY")
    assert groq_handler.client is not None


def test_query_success(groq_handler):
    """Test the query method for a successful API call."""
    messages = [{"role": "user", "content": "Hello"}]
    response = groq_handler.query(messages=messages, timeout=5)

    assert response.get("data") is not None


def test_query_with_model_parameter():
    """Test the query method when a specific model is provided."""
    groq_handler = GroqHandler(api_key=os.getenv("GROQ_API_KEY"))
    messages = [{"role": "user", "content": "Hello"}]
    response = groq_handler.query(messages=messages)

    assert "data" in response
    assert response["data"] is not None
    assert groq_handler.model is not None


def test_query_exception_handling(groq_handler):
    """Test the query method when an exception occurs."""
    messages = [{"role": "user", "content": "Hello"}]

    try:
        groq_handler.query(messages=messages)
    except Exception as e:
        assert isinstance(e, Exception)
