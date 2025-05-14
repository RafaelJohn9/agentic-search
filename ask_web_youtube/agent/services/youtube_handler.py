"""
YouTubeHandler Class with Transcript Fetching using youtube_transcript_api.

Fetches videos via YouTube API and retrieves captions with timestamps using
the youtube_transcript_api for public videos.
"""

import isodate
from typing import List, Dict, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from youtube_transcript_api._api import YouTubeTranscriptApi

from utils.log_config import setup_logger


class YouTubeHandler:
    """A class to handle YouTube API interactions and transcript fetching."""

    from typing import Optional

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize the YouTubeHandler with the provided API key or from environment variable."""
        self.api_key = api_key or os.getenv("YOUTUBE_DATA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided or set in the environment variable 'YOUTUBE_DATA_API_KEY'."
            )
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.logger = setup_logger(__name__)

    def fetch_videos(
        self, query: str, max_results: int = 2, include_transcripts: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Fetch videos from YouTube API. Sort by duration and select up to `max_results` videos that have transcripts if requested.

        :param query: Search query string.
        :param max_results: Number of results to return.
        :param include_transcripts: Whether to include transcripts.
        :return: List of video details.
        """
        try:
            self.logger.info(f"Fetching results for query: '{query}'")

            # Step 1: Search videos
            search_response = (
                self.youtube.search()
                .list(
                    q=query,
                    part="id,snippet",
                    maxResults=max_results * 10,
                    type="video",
                )
                .execute()
            )

            # Step 2: Collect video IDs and titles
            candidates: List[Dict[str, Any]] = []
            for item in search_response.get("items", []):
                video_id = item["id"]["videoId"]
                title = item["snippet"]["title"]
                self.logger.info(f"Found video: {title} (ID: {video_id})")

                # Fetch duration
                try:
                    video_response = (
                        self.youtube.videos()
                        .list(part="contentDetails", id=video_id)
                        .execute()
                    )
                    iso_duration = video_response["items"][0]["contentDetails"][
                        "duration"
                    ]
                    duration = isodate.parse_duration(iso_duration).total_seconds()
                except Exception as e:
                    self.logger.warning(f"Could not fetch duration for {video_id}: {e}")
                    duration = float("inf")

                candidates.append(
                    {
                        "video_id": video_id,
                        "title": title,
                        "duration": duration,
                    }
                )

            # Step 3: Sort by duration
            sorted_candidates = sorted(candidates, key=lambda x: x["duration"])

            # Step 4: Collect results with/without transcripts
            results: List[Dict[str, Any]] = []
            index = 0

            while len(results) < max_results and index < len(sorted_candidates):
                video = sorted_candidates[index]
                index += 1

                if include_transcripts:
                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(
                            video["video_id"]
                        )
                        video["transcript"] = transcript
                        video["transcripts_available"] = True
                        video["duration"] = sum(
                            segment["duration"] for segment in transcript
                        )
                        results.append(video)
                    except (TranscriptsDisabled, NoTranscriptFound):
                        self.logger.info(f"No transcript for: {video['title']}")
                    except Exception as e:
                        self.logger.error(f"Transcript error for {video['title']}: {e}")
                else:
                    video["transcripts_available"] = False
                    results.append(video)

            return results

        except HttpError as e:
            self.logger.error(f"HTTP error: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")

        return []
