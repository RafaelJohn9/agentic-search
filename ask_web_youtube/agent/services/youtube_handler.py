"""
YouTubeHandler Class
This class handles interactions with the YouTube Data API v3.
It provides methods to fetch videos based on a search query and check if they have transcripts available.
"""

import logging
from typing import List, Dict
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class YouTubeHandler:
    """
    A class to handle YouTube API interactions.
    """

    def __init__(self, api_key: str) -> None:
        """
        Initialize the YouTubeHandler with the provided API key.
        """
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def fetch_videos_with_transcripts(
        self, query: str, max_results: int = 10
    ) -> List[Dict[str, str]]:
        """
        Fetch videos from YouTube API that contain transcripts.

        :param query: Search query string.
        :param max_results: Number of results to fetch.
        :return: List of video details containing transcripts.
        """
        try:
            self.logger.info(f"Fetching {max_results} results for query: '{query}'")
            search_response = (
                self.youtube.search()
                .list(q=query, part="id,snippet", maxResults=max_results, type="video")
                .execute()
            )

            videos: List[Dict[str, str]] = []
            for item in search_response.get("items", []):
                video_id = item["id"]["videoId"]
                video_title = item["snippet"]["title"]
                self.logger.info(f"Processing video: {video_title} (ID: {video_id})")

                # Check if the video has captions (transcripts)
                captions_response = (
                    self.youtube.captions()
                    .list(part="snippet", videoId=video_id)
                    .execute()
                )

                if captions_response.get("items"):
                    videos.append(
                        {
                            "video_id": video_id,
                            "title": video_title,
                            "transcripts_available": True,
                        }
                    )
                else:
                    self.logger.info(
                        f"No transcripts available for video: {video_title}"
                    )

            return videos

        except HttpError as e:
            self.logger.error(f"An HTTP error occurred: {e}")
            return []
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return []
