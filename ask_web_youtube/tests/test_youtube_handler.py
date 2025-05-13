"""
Tests for YouTubeHandler using pytest standards.
This module tests the functionality of the YouTubeHandler
"""

import os
import pytest
from agent.services.youtube_handler import YouTubeHandler
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Skip tests if YOUTUBE_DATA_API_KEY is not set
pytestmark = pytest.mark.skipif(
    not os.getenv("YOUTUBE_DATA_API_KEY"),
    reason="YOUTUBE_DATA_API_KEY environment variable is not set",
)


@pytest.fixture
def youtube_handler() -> YouTubeHandler:
    """
    Fixture to initialize the YouTubeHandler with the API key.

    Returns:
        YouTubeHandler: An instance of the YouTubeHandler class.
    """
    api_key = os.getenv("YOUTUBE_DATA_API_KEY")
    return YouTubeHandler(api_key)


def test_fetch_videos_success(youtube_handler: YouTubeHandler) -> None:
    """
    Test fetching videos with and without transcripts.

    Args:
        youtube_handler (YouTubeHandler): The YouTubeHandler instance.
    """
    videos_with_transcripts: List[Dict] = youtube_handler.fetch_videos(
        "Python programming", max_results=2, include_transcripts=True
    )
    assert len(videos_with_transcripts) > 0
    for video in videos_with_transcripts:
        assert "video_id" in video
        assert "title" in video
        assert "transcripts_available" in video
        assert video["transcripts_available"] is True

    videos_without_transcripts: List[Dict] = youtube_handler.fetch_videos(
        "Python programming", max_results=2, include_transcripts=False
    )
    assert len(videos_without_transcripts) > 0
    for video in videos_without_transcripts:
        assert "video_id" in video
        assert "title" in video
        assert "transcripts_available" in video


def test_fetch_videos_http_error(youtube_handler: YouTubeHandler) -> None:
    """
    Test handling of HTTP errors during video fetching.

    Args:
        youtube_handler (YouTubeHandler): The YouTubeHandler instance.
    """
    try:
        youtube_handler.fetch_videos("Invalid query", max_results=1, include_transcripts=True)
    except Exception as e:
        assert "HttpError" in str(e)



def test_fetch_videos_unexpected_error(youtube_handler: YouTubeHandler) -> None:
    """
    Test handling of unexpected errors during video fetching.

    Args:
        youtube_handler (YouTubeHandler): The YouTubeHandler instance.
    """
    try:
        youtube_handler.fetch_videos("", max_results=1, include_transcripts=True)
    except Exception as e:
        assert "Unexpected Error" in str(e)
