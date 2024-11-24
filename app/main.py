import os
import sys
import streamlit as st
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings, PromptTemplate
from system_prompt import prompt

# Load environment variables
load_dotenv()

# Load OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API key not found. Please set it in the .env file.")
    st.stop()

# Settings for LlamaIndex
Settings.llm = OpenAI(model="gpt-4o", temperature=0.7, api_key=openai_api_key, system_prompt="")

# System prompt setup
system_prompt = prompt
react_system_prompt = PromptTemplate(system_prompt)

# Initialize ReActAgent
agent = ReActAgent.from_tools([], verbose=True, max_iterations=50)
agent.update_prompts({"agent_worker:system_prompt": react_system_prompt})

# Streamlit App
st.title("Movie Booking Assistant")

# Sidebar Chat Interface
st.sidebar.header("Chat with the Assistant")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input box for user message
user_input = st.sidebar.text_input("Enter your message:", key="user_input")

# Handle user input
if st.sidebar.button("Send"):
    if user_input.strip():
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            # Get agent response
            response = agent.chat(user_input)

            # Add agent response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response.response})
        except Exception as e:
            # Handle errors
            error_message = f"Error: {e}"
            st.sidebar.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
    else:
        st.sidebar.warning("Please enter a message.")

# Display chat history in the sidebar
for message in st.session_state.messages:
    if message["role"] == "user":
        st.sidebar.markdown(f"**You:** {message['content']}")
    elif message["role"] == "assistant":
        st.sidebar.markdown(f"**Assistant:** {message['content']}")

# Main Page
st.markdown(
    """
    ## Welcome to the Movie Booking Assistant
    This assistant is powered by a custom ReActAgent to help you:
    - Find movies, theaters, and showtimes
    - Provide recommendations based on your mood, preferences, or location
    - Handle seat bookings and cancellations
    - Manage payments and more!
    
    Simply type your question or request in the chat box to get started.
    """
)