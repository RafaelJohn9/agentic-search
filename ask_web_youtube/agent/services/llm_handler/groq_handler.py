"""GroqHandler class for interacting with Groq's API using a third-party package."""

import logging
from typing import Any, Dict, Optional
from groq import Groq
import httpx
import os


class GroqHandler:
    """
    A handler class to interact with Groq's API using the `groq` package.

    Attributes:
        api_key (str): The API key for authenticating with Groq.
        client (Groq): The Groq client instance for API interaction.
    """

    def __init__(
        self, api_key: Optional[str] = None, model: Optional[str] = None
    ) -> None:
        """
        Initialize the GroqHandler with the provided API key and optional model.

        Args:
            api_key (Optional[str]): The API key for Groq. If not provided, it will be fetched from the environment variable `GROQ_API_KEY`.
            model (Optional[str]): The model to use (e.g., "llama3-8b-8192").
        """

        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either as an argument or via the `GROQ_API_KEY` environment variable."
            )

        self.model = model
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.client = Groq(api_key=self.api_key)

    def query(
        self,
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

        if not self.model:
            url = "https://api.groq.com/openai/v1/models"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            try:
                self.logger.info("Fetching available models from Groq API...")
                response = httpx.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                available_models = response.json().get("data", [])

                if not available_models:
                    raise ValueError("No models available in Groq API.")
                hardcoded_model = "llama3-8b-8192"
                self.logger.info(
                    f"Checking if hardcoded model '{hardcoded_model}' is available..."
                )
                if not any(
                    model.get("id") == hardcoded_model for model in available_models
                ):
                    raise ValueError(
                        f"Hardcoded model '{hardcoded_model}' is not available in Groq API. "
                        "Please update the hardcoded model to an appropriate one."
                    )

                self.model = hardcoded_model
            except httpx.RequestError as e:
                self.logger.error(f"HTTP request error while fetching models: {e}")
                raise
            except Exception as e:
                self.logger.error(f"Error fetching models from Groq API: {e}")
                raise

        kwargs["model"] = self.model

        try:
            self.logger.info("Querying Groq Chat Completion API...")
            response = self.client.chat.completions.create(**kwargs)
            self.logger.info("Query successful.")

            return_data = {
                "model": self.model,
                "data": response.choices[0].message.content,
            }
            return return_data
        except Exception as e:
            self.logger.error(f"Error querying Groq API: {e}")
            raise
