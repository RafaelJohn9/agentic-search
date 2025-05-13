"""
YouTubeHandler Class with Transcript Fetching using youtube_transcript_api.
Fetches videos via YouTube API and retrieves captions with timestamps using
the youtube_transcript_api for public videos.
"""

import logging
from typing import List, Dict, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)


class YouTubeHandler:
    """
    A class to handle YouTube API interactions and transcript fetching.
    """

    def __init__(self, api_key: str = None) -> None:
        """
        Initialize the YouTubeHandler with the provided API key or from environment variable.
        """

        self.api_key = api_key or os.getenv("YOUTUBE_DATA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided or set in the environment variable 'YOUTUBE_DATA_API_KEY'."
            )
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def fetch_videos(
        self, query: str, max_results: int = 2, include_transcripts: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Fetch videos from YouTube API. Optionally fetch transcripts with timestamps.

        :param query: Search query string.
        :param max_results: Number of results to fetch.
        :param include_transcripts: Whether to fetch transcripts with timestamps.
        :return: List of video details.
        """
        try:
            self.logger.info(f"Fetching {max_results} results for query: '{query}'")
            search_response = (
                self.youtube.search()
                .list(
                    q=query, part="id,snippet", maxResults=max_results * 2, type="video"
                )
                .execute()
            )

            videos: List[Dict[str, Any]] = []

            for item in search_response.get("items", []):
                if len(videos) >= max_results:
                    break

                video_id = item["id"]["videoId"]
                video_title = item["snippet"]["title"]
                self.logger.info(f"Processing video: {video_title} (ID: {video_id})")

                video_data: Dict[str, Any] = {
                    "video_id": video_id,
                    "title": video_title,
                }

                if include_transcripts:
                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(video_id)
                        video_data["transcript"] = (
                            transcript  # includes 'text', 'start', 'duration'
                        )
                        video_data["transcripts_available"] = True
                    except (TranscriptsDisabled, NoTranscriptFound):
                        self.logger.info(
                            f"No transcripts available for video: {video_title}"
                        )
                        video_data["transcripts_available"] = False
                    except Exception as e:
                        self.logger.error(f"Error fetching transcript: {e}")
                        video_data["transcripts_available"] = False
                else:
                    video_data["transcripts_available"] = False

                videos.append(video_data)

            return videos[:max_results]

        except HttpError as e:
            self.logger.error(f"An HTTP error occurred: {e}")
            return []
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return []
