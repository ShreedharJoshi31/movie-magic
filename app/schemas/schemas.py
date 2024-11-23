from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# User Schema
class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    location: Optional[str]

    class Config:
        orm_mode = True


# Movie Schema
class Movie(BaseModel):
    movie_id: int
    movie_name: str
    movie_description: str
    genre: str
    cast: str
    language: str
    mood: str
    average_rating: float
    showtimes: List["Showtime"] = []  # Relationship to Showtime

    class Config:
        orm_mode = True


# SeatMap Schema
class SeatMap(BaseModel):
    seatmap_id: int
    showtime_id: int
    seat_category: str
    seat_price: float
    seat_no: str
    seat_status: bool

    class Config:
        orm_mode = True


# Showtime Schema
class Showtime(BaseModel):
    showtime_id: int
    theater_id: str
    movie_id: int
    language: str
    show_time: datetime
    theater: Optional["Theater"]  # Relationship to Theater
    movie: Optional[Movie]  # Relationship to Movie
    seatmap: List[SeatMap] = []  # Relationship to SeatMap

    class Config:
        orm_mode = True


# Theater Schema
class Theater(BaseModel):
    theater_id: str
    theater_name: str
    theater_location: str
    showtimes: List[Showtime] = []  # Relationship to Showtime

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    payment_status: bool
    transaction_time: datetime
    bookings: List["Booking"] = []  # Relationship to Booking

    class Config:
        orm_mode = True

class Booking(BaseModel):
    booking_id: int
    user_id: str
    transaction_id: str
    user_name: str
    movie_name: str
    theater: str
    show_time: datetime
    seat: str
    booking_time: datetime
    transaction: Optional[Transaction]  # Relationship to Transaction

    class Config:
        orm_mode = True


# Resolve forward references
Movie.update_forward_refs()
Showtime.update_forward_refs()
Theater.update_forward_refs()