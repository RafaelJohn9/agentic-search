from agent.agent import Agent
from dotenv import load_dotenv

if __name__ == "__main__":
    """
    Test fetching videos with an invalid query to trigger an HTTP error.
    """
    load_dotenv()
    # Initialize the agent
    agent = Agent()
    response = agent.process_request(
        input_text="What is the capital of France?",
        enable_web=True,
        enable_youtube=True,
    )
    print(response)
