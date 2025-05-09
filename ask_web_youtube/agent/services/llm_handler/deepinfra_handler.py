"""DeepInfraHandler class for interacting with DeepInfra's API."""

import logging
from typing import Optional
import deepinfra


class DeepInfraHandler:
    """
    A handler class to interact with DeepInfra's API using the `deepinfra` package.

    Attributes:
        api_key (str): The API key for authenticating with DeepInfra.
        model (Optional[str]): The default model to use.
    """

    def __init__(self, api_key: str, model: Optional[str] = None) -> None:
        """
        Initialize the DeepInfraHandler with the provided API key and optional model.

        Args:
            api_key (str): The API key for DeepInfra.
            model (Optional[str]): The default model to use. Defaults to None.
        """
        self.api_key = api_key
        self.model = model
        deepinfra.api_key = self.api_key
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def query_response(
        self,
        instructions: str,
        input_text: str,
    ) -> str:
        """
        Query the DeepInfra API.

        Args:
            instructions (str): Instructions for the model.
            input_text (str): Input text for the model.

        Returns:
            str: The generated text from the DeepInfra API.
        """
        try:
            self.logger.info("Querying DeepInfra API...")

            kwargs = dict(
                instructions=instructions,
                input=input_text,
            )

            if self.model:
                kwargs["model"] = self.model

            response = deepinfra.responses.create(**kwargs)
            self.logger.info("Query successful.")
            return response.output_text
        except Exception as e:
            self.logger.error(f"Error querying DeepInfra API: {e}")
            raise
