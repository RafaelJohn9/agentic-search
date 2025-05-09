"""OpenAIHandler class for interacting with OpenAI's API."""

import logging
from typing import Optional
import openai


class OpenAIHandler:
    """
    A handler class to interact with OpenAI's API using the `openai` package.

    Attributes:
        api_key (str): The API key for authenticating with OpenAI.
    """

    def __init__(self, api_key: str, model: Optional[str] = None) -> None:
        """
        Initialize the OpenAIHandler with the provided API key and optional model.

        Args:
            api_key (str): The API key for OpenAI.
            model (Optional[str]): The default model to use (e.g., "gpt-4o"). Defaults to None.
        """
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def query_response(
        self,
        instructions: str,
        input_text: str,
    ) -> str:
        """
        Query the OpenAI Responses API.

        Args:
            model (str): The model to use (e.g., "gpt-4o").
            instructions (str): Instructions for the model.
            input_text (str): Input text for the model.

        Returns:
            str: The generated text from the OpenAI API.
        """
        try:
            self.logger.info("Querying OpenAI Responses API...")

            kwargs = dict(
                instructions=instructions,
                input=input_text,
            )

            if self.model:
                kwargs["model"] = self.model

            response = openai.responses.create(**kwargs)
            self.logger.info("Query successful.")
            return response.output_text
        except Exception as e:
            self.logger.error(f"Error querying OpenAI API: {e}")
            raise
