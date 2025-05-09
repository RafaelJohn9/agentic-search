"""duckduck go search handler module.
This module provides a class to handle search queries using the DuckDuckGo API.
"""

import logging
import requests
from typing import Any, Dict, Optional


class DuckDuckGoSearchHandler:
    """
    A handler class for performing searches using the DuckDuckGo API.

    This class provides methods to query the DuckDuckGo search engine and retrieve results.
    It includes robust logging, error handling, and static typing to ensure reliability.

    Attributes:
        base_url (str): The base URL for the DuckDuckGo API.
    """

    def __init__(self) -> None:
        """
        Initializes the DuckDuckGoSearchHandler with the base API URL.
        """
        self.base_url = "https://api.duckduckgo.com/"
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self.logger.addHandler(handler)

    def search(self, query: str, format: str = "json") -> Optional[Dict[str, Any]]:
        """
        Performs a search query using the DuckDuckGo API.

        Args:
            query (str): The search query string.
            format (str): The response format, default is "json".

        Returns:
            Optional[Dict[str, Any]]: The search results as a dictionary if successful, None otherwise.

        Raises:
            ValueError: If the query is empty or invalid.
        """
        if not query.strip():
            self.logger.error("Search query cannot be empty.")
            raise ValueError("Search query cannot be empty.")

        params = {"q": query, "format": format, "no_redirect": 1, "no_html": 1}

        try:
            self.logger.debug(
                f"Sending request to DuckDuckGo API with params: {params}"
            )
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            self.logger.debug("Request successful, parsing response.")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred while making the request: {e}")
        except ValueError as e:
            self.logger.error(f"Error parsing response: {e}")
        return None
