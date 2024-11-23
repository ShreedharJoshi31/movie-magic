from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    location = Column(String)

class Review(Base):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True, autoincrement=True)  # Unique review ID
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), nullable=False)  # FK to Movie table
    username = Column(String, nullable=False)  # Username of the reviewer
    review_time = Column(DateTime, default=datetime.now(), nullable=False)  # Time of review
    review_rating = Column(Float, nullable=False)  # Rating on a scale of 1 to 5
    review_comment = Column(String, nullable=True)  # Optional comment

    # Relationship with Movie
    movie = relationship("Movie", back_populates="reviews")

class Movie(Base):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True, autoincrement=False)
    movie_name = Column(String, nullable=False)
    movie_description = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    cast = Column(String, nullable=False)
    language = Column(String, nullable=False)
    mood = Column(String, nullable=False)
    average_rating = Column(Float, nullable=False)
    showtimes = relationship("Showtime", back_populates="movie")
    reviews = relationship("Review", back_populates="movie")  # New relationship

    # SeatMap Table
class SeatMap(Base):
    __tablename__ = 'seatmap'

    seatmap_id = Column(Integer, primary_key=True, autoincrement=True)
    showtime_id = Column(Integer, ForeignKey('showtimes.showtime_id'), nullable=False)
    seat_category = Column(String, nullable=False)  # E.g., VIP, Regular, etc.
    seat_price = Column(Float, nullable=False)
    seat_no = Column(String, nullable=False)  # Seat number (e.g., A1, B5)
    seat_status = Column(Boolean, default=False)  # False = Available, True = Booked

    # Relationship
    showtime = relationship("Showtime", back_populates="seatmap")


# Showtimes Table
class Showtime(Base):
    __tablename__ = 'showtimes'

    showtime_id = Column(Integer, primary_key=True, autoincrement=True)
    theater_id = Column(String, ForeignKey('theaters.theater_id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), nullable=False)
    language = Column(String, nullable=False)
    show_time = Column(DateTime, nullable=False)

    # Relationships
    theater = relationship("Theater", back_populates="showtimes")
    movie = relationship("Movie", back_populates="showtimes")
    seatmap = relationship("SeatMap", back_populates="showtime")

class Theater(Base):
    __tablename__ = 'theaters'
    theater_id = Column(String, primary_key=True)  # UUID as a string
    theater_name = Column(String, nullable=False)
    theater_location = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)  # New column for latitude
    longitude = Column(Float, nullable=True)  # New column for longitude

    showtimes = relationship("Showtime", back_populates="theater")

# Transaction Table
class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(String, primary_key=True)  # UUID as a string
    user_id = Column(String, nullable=False)  # User ID (could be a UUID or string)
    payment_status = Column(Boolean, nullable=False, default=False)  # True = Paid, False = Pending
    transaction_time = Column(DateTime, default=datetime.now(), nullable=False)

    # Relationship to bookings
    bookings = relationship("Booking", back_populates="transaction")


# Bookings Table
class Booking(Base):
    __tablename__ = 'bookings'

    booking_id = Column(Integer, primary_key=True, autoincrement=True)  # Unique booking ID
    user_id = Column(String, nullable=False)  # User ID (same as in Transaction)
    transaction_id = Column(String, ForeignKey('transactions.transaction_id'), nullable=False)  # FK to Transaction
    user_name = Column(String, nullable=False)  # User's name
    movie_name = Column(String, nullable=False)  # Movie name
    theater = Column(String, nullable=False)  # Theater name
    show_time = Column(DateTime, nullable=False)  # Show date and time
    seat = Column(String, nullable=False)  # Seat number (e.g., A1, B3)
    booking_time = Column(DateTime, default=datetime.now(), nullable=False)  # Booking timestamp

    # Relationship to transaction
    transaction = relationship("Transaction", back_populates="bookings")