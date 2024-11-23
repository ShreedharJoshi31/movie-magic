from app.routes import dummy_routes, user_routes
# from app.middleware.auth_middleware import AuthMiddleware
import os
from fastapi import FastAPI
# from app.routes import chat_routes, document_routes
# from app.middleware.auth_middleware import AuthMiddleware
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.database import engine
from app.schemas.models import Base
from fastapi import WebSocket, WebSocketDisconnect
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings
from app.functions.movie_functions import get_movies_by_name, get_movies_by_description, get_movies_by_genre, get_movies_by_cast, get_movies_by_language, get_movies_by_mood, get_movies_by_average_rating, get_movies_by_showtime
from app.functions.payment_functions import create_razorpay_order
from app.functions.theater_functions import get_nearby_theaters, get_accessible_theaters, get_movie_showtimes_near_location, get_showtimes_by_theater_name, get_theaters_by_location
from app.functions.seatmap import get_seatmap_by_showtime, book_seat, cancel_booking, check_booking_by_email
import pandas as pd
load_dotenv()

class AccessTokenRequest(BaseModel):
    access_token: str

app = FastAPI()

origins = [
    "*",
]

# Adding CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize Amplify

# Add middleware
# app.add_middleware(BaseHTTPMiddleware, dispatch=AuthMiddleware())

# Add CORS middleware to the FastAPI app
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(dummy_routes.router, prefix="/dummy", tags=["dummy"])
app.include_router(user_routes.router, prefix="/user", tags=["user"])


openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")


# settings
Settings.llm = OpenAI(model="gpt-4o", temperature=0.7, api_key=openai_api_key, system_prompt="Your name is FLASH. Greet everyone at the start of every message.")

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
                               get_nearby_theaters_tool, get_accessible_theaters_tool, get_movie_showtimes_near_location_tool, get_showtimes_by_theater_name_tool, get_theaters_by_location_tool,
                               get_seatmap_by_showtime_tool, book_seat_tool, check_booking_by_email_tool], verbose=True, max_iterations=20)


@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            print(f"Received message: {message}")  # Debug print

            try:
                response = agent.chat(message)
                print(f"Agent response: {response}")  # Debug print
                await websocket.send_json({"type": "response", "content":response.response})
            except Exception as e:
                print(f"Error in processing message: {e}")  # Debug print
                await websocket.send_text(f"Error processing message: {str(e)}")

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")