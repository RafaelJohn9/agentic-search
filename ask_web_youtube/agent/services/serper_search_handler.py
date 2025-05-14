"""serper search handler module.

This module provides a class to handle search queries using the Serper API.
"""

import httpx
from typing import Optional
import os

from utils.log_config import setup_logger


class SerperSearchHandler:
    """
    A handler class for performing searches using the Serper API.

    This class provides methods to query the Serper search engine and retrieve results.
    It includes robust logging, error handling, and static typing to ensure reliability.

    Attributes:
        base_url (str): The base URL for the Serper API.
        api_key (str): The API key for authenticating with the Serper API.
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initialize the SerperSearchHandler with the base API URL and API key.

        Args:
            api_key (Optional[str]): The API key for the Serper API. If not provided, it will be fetched from the environment variable 'SERPER_API_KEY'.
        """
        self.base_url = "https://google.serper.dev/search"
        self.api_key = api_key or os.getenv("SERPER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either as an argument or via the 'SERPER_API_KEY' environment variable."
            )

        self.logger = setup_logger(__name__)

    def search(self, query: str, max_pages: int = 3) -> list:
        """
        Perform a search query using the Serper API.

        Args:
            query (str): The search query string.

        Returns:
            list: A list of search results.

        Raises:
            ValueError: If the query is empty or invalid.
        """
        if not query.strip():
            self.logger.error("Search query cannot be empty.")
            raise ValueError("Search query cannot be empty.")

        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "q": query,
        }

        results = []
        for page in range(1, max_pages + 1):
            payload["page"] = str(page)
            try:
                self.logger.debug(f"Sending request to Serper API: {self.base_url}")
                with httpx.Client() as client:
                    response = client.post(
                        self.base_url, headers=headers, json=payload, timeout=10
                    )
                response.raise_for_status()
                self.logger.debug("Request successful, parsing response.")
                return response.json()
            except httpx.TimeoutException:
                self.logger.error("The request timed out.")
            except httpx.RequestError as e:
                self.logger.error(f"An error occurred while making the request: {e}")
            except ValueError as e:
                self.logger.error(f"Error parsing response: {e}")
            except Exception as e:
                self.logger.error(f"An unexpected error occurred: {e}")

        return results
