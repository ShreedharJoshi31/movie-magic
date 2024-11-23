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

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}