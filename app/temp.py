import os
from dotenv import load_dotenv
load_dotenv()
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings
from app.functions.movie_functions import get_movies_by_name, get_movies_by_description, get_movies_by_genre, get_movies_by_cast, get_movies_by_language, get_movies_by_mood, get_movies_by_average_rating, get_movies_by_showtime
from app.functions.payment_functions import create_razorpay_order
from app.functions.theater_functions import get_nearby_theaters, get_accessible_theaters, get_movie_showtimes_near_location, get_showtimes_by_theater_name, get_theaters_by_location
from app.functions.seatmap import get_seatmap_by_showtime, book_seat, cancel_booking, check_booking_by_email
import pandas as pd


openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")


# settings
Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=openai_api_key, system_prompt="Your name is FLASH. Greet everyone at the start of every message.")

get_movies_by_name_tool = FunctionTool.from_defaults(fn=get_movies_by_name)
get_movies_by_description_tool = FunctionTool.from_defaults(fn=get_movies_by_description)
get_movies_by_genre_tool = FunctionTool.from_defaults(fn=get_movies_by_genre)
get_movies_by_cast_tool = FunctionTool.from_defaults(fn=get_movies_by_cast)
get_movies_by_language_tool = FunctionTool.from_defaults(fn=get_movies_by_language)
get_movies_by_mood_tool = FunctionTool.from_defaults(fn=get_movies_by_mood)
get_movies_by_average_rating_tool = FunctionTool.from_defaults(fn=get_movies_by_average_rating)
get_movies_by_showtime_tool = FunctionTool.from_defaults(fn=get_movies_by_showtime)
create_razorpay_order_tool = FunctionTool.from_defaults(fn=create_razorpay_order)
# theater functions
get_nearby_theaters_tool = FunctionTool.from_defaults(fn=get_nearby_theaters)
get_accessible_theaters_tool = FunctionTool.from_defaults(fn=get_accessible_theaters)
get_movie_showtimes_near_location_tool = FunctionTool.from_defaults(fn=get_movie_showtimes_near_location)
get_showtimes_by_theater_name_tool = FunctionTool.from_defaults(fn=get_showtimes_by_theater_name)
get_theaters_by_location_tool = FunctionTool.from_defaults(fn=get_theaters_by_location)
# seatmap functions
get_seatmap_by_showtime_tool = FunctionTool.from_defaults(fn=get_seatmap_by_showtime)
book_seat_tool = FunctionTool.from_defaults(fn=book_seat)
cancel_booking_tool = FunctionTool.from_defaults(fn=cancel_booking)
check_booking_by_email_tool = FunctionTool.from_defaults(fn=check_booking_by_email)

agent = ReActAgent.from_tools([ get_movies_by_name_tool, get_movies_by_description_tool, get_movies_by_genre_tool, get_movies_by_cast_tool, get_movies_by_language_tool, 
                               get_movies_by_mood_tool, get_movies_by_average_rating_tool, get_movies_by_showtime_tool, create_razorpay_order_tool, 
                               get_nearby_theaters_tool, get_accessible_theaters_tool, get_movie_showtimes_near_location_tool, get_showtimes_by_theater_name_tool, get_theaters_by_location_tool], verbose=True)

# while True:
#     user_input = input("Enter your query (type 'quit' to exit): ")
#     if user_input.lower() == 'quit':
#         break
#     response = agent.chat(user_input)
#     print(response)

response = agent.chat("I am feeling happy what movie would you recommend me to watch?")

print(response)

# response = agent.chat("Book me a ticket to anyone of them")

# print(response)