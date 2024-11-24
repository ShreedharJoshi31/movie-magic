import os
import sys
import streamlit as st

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings, PromptTemplate
from system_prompt import prompt

# Import functions for tools
from functions.movie_functions import (
    get_movies_by_name,
    get_movies_by_description,
    get_movies_by_genre,
    get_movies_by_cast,
    get_movies_by_language,
    get_movies_by_mood,
    get_movies_by_average_rating,
    get_movies_by_showtime,
)
from functions.payment_functions import create_razorpay_order
from functions.theater_functions import (
    get_nearby_theaters,
    get_accessible_theaters,
    get_movie_showtimes_near_location,
    get_showtimes_by_theater_name,
    get_theaters_by_location,
)
from functions.seatmap import (
    get_seatmap_by_showtime,
    book_seat,
    cancel_booking,
    check_booking_by_email,
    get_seat_prices,
)

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

# Define tools
get_movies_by_name_tool = FunctionTool.from_defaults(fn=get_movies_by_name)
get_movies_by_description_tool = FunctionTool.from_defaults(fn=get_movies_by_description)
get_movies_by_genre_tool = FunctionTool.from_defaults(fn=get_movies_by_genre)
get_movies_by_cast_tool = FunctionTool.from_defaults(fn=get_movies_by_cast)
get_movies_by_language_tool = FunctionTool.from_defaults(fn=get_movies_by_language)
get_movies_by_mood_tool = FunctionTool.from_defaults(fn=get_movies_by_mood)
get_movies_by_average_rating_tool = FunctionTool.from_defaults(fn=get_movies_by_average_rating)
get_movies_by_showtime_tool = FunctionTool.from_defaults(fn=get_movies_by_showtime)
create_razorpay_order_tool = FunctionTool.from_defaults(fn=create_razorpay_order)
get_nearby_theaters_tool = FunctionTool.from_defaults(fn=get_nearby_theaters)
get_accessible_theaters_tool = FunctionTool.from_defaults(fn=get_accessible_theaters)
get_movie_showtimes_near_location_tool = FunctionTool.from_defaults(fn=get_movie_showtimes_near_location)
get_showtimes_by_theater_name_tool = FunctionTool.from_defaults(fn=get_showtimes_by_theater_name)
get_theaters_by_location_tool = FunctionTool.from_defaults(fn=get_theaters_by_location)
get_seatmap_by_showtime_tool = FunctionTool.from_defaults(fn=get_seatmap_by_showtime)
book_seat_tool = FunctionTool.from_defaults(fn=book_seat)
cancel_booking_tool = FunctionTool.from_defaults(fn=cancel_booking)
check_booking_by_email_tool = FunctionTool.from_defaults(fn=check_booking_by_email)
get_seat_prices_tool = FunctionTool.from_defaults(fn=get_seat_prices)

# Initialize ReActAgent with the full set of tools
agent = ReActAgent.from_tools(
    [
        get_movies_by_name_tool,
        get_movies_by_description_tool,
        get_movies_by_genre_tool,
        get_movies_by_cast_tool,
        get_movies_by_language_tool,
        get_movies_by_mood_tool,
        get_movies_by_average_rating_tool,
        get_movies_by_showtime_tool,
        create_razorpay_order_tool,
        get_nearby_theaters_tool,
        get_accessible_theaters_tool,
        get_movie_showtimes_near_location_tool,
        get_showtimes_by_theater_name_tool,
        get_theaters_by_location_tool,
        get_seatmap_by_showtime_tool,
        book_seat_tool,
        cancel_booking_tool,
        check_booking_by_email_tool,
        get_seat_prices_tool,
    ],
    verbose=True,
    max_iterations=50,
)
agent.update_prompts({"agent_worker:system_prompt": react_system_prompt})

# Streamlit App
st.title("Movie Booking Assistant")

# Sidebar for app information
st.sidebar.header("About the Assistant")
st.sidebar.markdown(
    """
    ### Welcome to the Movie Booking Assistant!
    This assistant is powered by a custom ReActAgent to help you:
    - Find movies, theaters, and showtimes
    - Provide recommendations based on your preferences
    - Manage seat bookings and cancellations
    - Handle payment inquiries

    Use the chat interface on the **main page** to interact with the assistant.
    """
)

# Main Chat Interface
st.subheader("Chat with the Assistant")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat container
with st.container():
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**Assistant:** {message['content']}")

    # Input box for user message
    user_input = st.text_input("Enter your message:", key="user_input")

    # Handle user input
    if st.button("Send"):
        if user_input.strip():
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Immediately re-render the chat history
            with st.container():
                for message in st.session_state.messages:
                    if message["role"] == "user":
                        st.markdown(f"**You:** {message['content']}")
                    elif message["role"] == "assistant":
                        st.markdown(f"**Assistant:** {message['content']}")

            try:
                # Get agent response
                response = agent.chat(user_input)

                # Add agent response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response.response})

            except Exception as e:
                # Handle errors
                error_message = f"Error: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
        else:
            st.warning("Please enter a message.")