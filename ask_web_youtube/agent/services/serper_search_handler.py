"""serper search handler module.
This module provides a class to handle search queries using the Serper API.
"""

import logging
import requests
from typing import Any, Dict, Optional
import os


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
        Initializes the SerperSearchHandler with the base API URL and API key.

        Args:
            api_key (Optional[str]): The API key for the Serper API. If not provided, it will be fetched from the environment variable 'SERPER_API_KEY'.
        """

        self.base_url = "https://google.serper.dev/search"
        self.api_key = api_key or os.getenv("SERPER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either as an argument or via the 'SERPER_API_KEY' environment variable."
            )

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self.logger.addHandler(handler)

    def search(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Performs a search query using the Serper API.

        Args:
            query (str): The search query string.

        Returns:
            Optional[Dict[str, Any]]: The search results as a dictionary if successful, None otherwise.

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
        payload = {"q": query}

        try:
            self.logger.debug(f"Sending request to Serper API: {self.base_url}")
            response = requests.post(
                self.base_url, headers=headers, json=payload, timeout=10
            )
            response.raise_for_status()
            self.logger.debug("Request successful, parsing response.")
            return response.json()
        except requests.exceptions.Timeout:
            self.logger.error("The request timed out.")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred while making the request: {e}")
        except ValueError as e:
            self.logger.error(f"Error parsing response: {e}")
        return None
