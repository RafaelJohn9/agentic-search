"""Agent module.

This module defines an Agent class that utilizes various services to perform tasks.
"""

from jinja2 import Environment, FileSystemLoader
from typing import Dict

from agent.services.serper_search_handler import SerperSearchHandler
from agent.services.youtube_handler import YouTubeHandler
from agent.services.llm_handler.groq_handler import GroqHandler
from utils.log_config import setup_logger


class Agent:
    """
    An Agent class that integrates multiple services to perform complex tasks.

    This class acts as a coordinator, utilizing the SerperSearchHandler,
    YouTubeHandler, and GroqHandler to perform searches, retrieve YouTube data,
    and interact with a language model.
    """

    def __init__(
        self, template_path="agent/templates/agent_input_template.jinja2"
    ) -> None:
        """Initialize the Agent with its service handlers."""
        self.template_path = template_path
        self.serper_handler = SerperSearchHandler()
        self.youtube_handler = YouTubeHandler()
        self.llm_handler = GroqHandler()
        self.logger = setup_logger(__name__)
        self.logger.info("Agent initialized with template path: %s", self.template_path)

    def generate_from_template(self, data: dict) -> str:
        """
        Generate content from a Jinja2 template.

        Args:
            template_path (str): The file path to the Jinja2 template.
            data (dict): The data to render the template with.

        Returns:
            str: The rendered template content.
        """
        self.logger.info("Generating content from template with data: %s", data)
        # Extract the directory and template file name from self.template_path
        template_dir, template_file = self.template_path.rsplit("/", 1)

        # Set up the Jinja2 environment
        env = Environment(loader=FileSystemLoader(template_dir))

        # Load the template
        template = env.get_template(template_file)

        # Render the template with the provided data
        response = template.render({"data": data})
        return response

    def process_request(
        self, input_text: str, enable_web: bool = True, enable_youtube: bool = False
    ) -> Dict[str, str]:
        """
        Process input text using the language model.

        Args:
            input_text (str): The input text to process.

        Returns:
            str: The processed output from the language model.
        """
        data = {"question": input_text}

        if enable_web:
            # Perform a web search using Serper
            search_results = self.serper_handler.search(input_text)
            import json

            data["web_search"] = json.dumps(search_results)

        if enable_youtube:
            # Perform a YouTube search
            youtube_results = self.youtube_handler.fetch_videos(input_text)
            import json

            data["youtube_search"] = json.dumps(youtube_results)

        input = self.generate_from_template(data)
        # Process the input text using the language model
        return self.llm_handler.query([{"role": "user", "content": input}])
