"""GroqHandler class for interacting with Groq's API using a third-party package."""

import logging
from typing import Any, Dict, Optional
from groq import Groq


class GroqHandler:
    """
    A handler class to interact with Groq's API using the `groq` package.

    Attributes:
        api_key (str): The API key for authenticating with Groq.
        client (Groq): The Groq client instance for API interaction.
    """

    def __init__(self, api_key: str, model: Optional[str] = None) -> None:
        """
        Initialize the GroqHandler with the provided API key and optional model.

        Args:
            api_key (str): The API key for Groq.
            model (Optional[str]): The model to use (e.g., "llama3-8b-8192").
        """
        self.api_key = api_key
        self.model = model
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.client = Groq(api_key=self.api_key)

    def query_response(
        self,
        model: str,
        messages: list[Dict[str, str]],
        timeout: Optional[int] = 10,
    ) -> Dict[str, Any]:
        """
        Query the Groq Chat Completion API.

        Args:
            model (str): The model to use (e.g., "llama3-8b-8192").
            messages (list[Dict[str, str]]): A list of message dictionaries for the conversation.
            timeout (Optional[int]): The timeout for the request in seconds.

        Returns:
            Dict[str, Any]: The response from the Groq API.
        """
        kwargs = dict(
            messages=messages,
            timeout=timeout,
        )

        if self.model:
            kwargs["model"] = self.model

        try:
            self.logger.info("Querying Groq Chat Completion API...")
            response = self.client.chat.completions.create(**kwargs)
            self.logger.info("Query successful.")
            return response
        except Exception as e:
            self.logger.error(f"Error querying Groq API: {e}")
            raise
