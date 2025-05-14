"""
This module provides the main functionality for the Agentic Search application.

It includes the main page, sidebar, debug panel, and entry point for the application.
"""

import streamlit as st
from dotenv import load_dotenv

from agent.agent import Agent
from utils.log_config import get_log_buffer


# Main Page
def main_page(agent):
    """
    Display the title, a text input box for user queries, and an "Ask" button.

    When the "Ask" button is clicked, process the user's query using the provided agent
    and display the response. Allow the user to enable or disable web and YouTube search
    through session state variables.

    Args:
        agent: An object that processes user queries and returns responses.
    """
    st.title("Ask the Web + YouTube")
    st.write("Ask anything and get answers from the web or YouTube!")

    # Text box for user input
    query = st.text_input("Enter your query:")

    # "Ask" button
    if st.button("Ask"):
        if query:
            # Process the query using the agent
            with st.spinner("Fetching results..."):
                try:
                    response = agent.process_request(
                        input_text=query,
                        enable_web=st.session_state.include_web,
                        enable_youtube=st.session_state.include_youtube,
                    )
                    # Store the query and response in session state
                    st.session_state.last_query = query
                    st.session_state.last_response = response
                    st.write("### Answer:")
                    st.write(response)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a query.")


# Sidebar
def sidebar(agent):
    """Create a sidebar with options for selecting whether to include web and YouTube searches."""
    with st.sidebar.expander("Options", expanded=False):
        st.write("Choose your search sources:")

        # Toggle options
        st.session_state.include_web = st.checkbox("Include Web", value=True)
        st.session_state.include_youtube = st.checkbox("Include YouTube", value=True)

        # Default to "Both" if both are selected
        if st.session_state.include_web and st.session_state.include_youtube:
            st.write("Search Mode: Both")
        elif st.session_state.include_web:
            st.write("Search Mode: Web Only")
        elif st.session_state.include_youtube:
            st.write("Search Mode: YouTube Only")
        else:
            st.warning("No sources selected!")

    with st.sidebar.expander("Verify Agent's Result", expanded=False):
        st.write("Verify the accuracy of the agent's response:")

        # Button to verify the result
        if st.button("Verify Result"):
            if "last_query" in st.session_state and "last_response" in st.session_state:
                # Prompt for verification
                VERIFICATION_PROMPT = (
                    "Verify if the following response is correct for the query.",
                    "If you agree that the response is correct, onlyt the word  `True` should be returned.",
                    "If incorrect, return False with the incorrect references. "
                    f"\n\nQuery: {st.session_state.last_query}\nResponse: {st.session_state.last_response}",
                )
                with st.spinner("Verifying result..."):
                    try:
                        verification_result = agent.process_request(
                            input_text=VERIFICATION_PROMPT,
                            enable_web=False,
                            enable_youtube=False,
                        )["data"]
                        # Accept both string "true" and boolean True as correct
                        if (
                            str(verification_result).strip().lower() == "true"
                            or verification_result is True
                        ):
                            st.success("✔ The response is verified as correct.")
                        else:
                            st.error(
                                f"✘ The response is incorrect. Details: {verification_result}"
                            )
                    except Exception as e:
                        st.error(f"An error occurred during verification: {e}")
            else:
                st.warning("No query or response available to verify.")


# Debug Panel
def debug_panel():
    """
    Create a debug panel to display the log buffer.

    Useful for debugging and monitoring the application's behavior.
    """
    with st.expander("Debug Panel"):
        st.text(get_log_buffer())


# Main function
def main():
    """
    Run the Streamlit application.

    Initialize the agent, set up the sidebar, main page, and debug panel.
    """
    load_dotenv()
    agent = Agent()

    # Initialize session state for toggles
    if "include_web" not in st.session_state:
        st.session_state.include_web = True
    if "include_youtube" not in st.session_state:
        st.session_state.include_youtube = True

    sidebar(agent)
    main_page(agent)
    debug_panel()


if __name__ == "__main__":
    main()
