from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import random
from sqlalchemy.orm import sessionmaker
# from app.schemas.models import Movie, Review
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

engine = create_engine('postgresql://avnadmin:AVNS_B__mg-mo4ERejoa7Rh9@pg-235500ec-shreedharjoshi03-f6ce.b.aivencloud.com:10885/defaultdb', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# List of random usernames and comments
usernames = ["user1", "user2", "user3", "user4", "user5", "critic1", "critic2", "fan1", "fan2", "moviebuff"]
comments = [
    "Amazing movie!", "Loved it!", "Not my type of movie.", "Could be better.", 
    "Highly recommended!", "Boring in parts.", "Great acting!", "Fantastic visuals!", 
    "Poor storyline.", "Perfect weekend watch."
]

def generate_reviews():
    try:
        # Fetch all movies from the database
        movies = session.query(Movie).all()

        if not movies:
            print("No movies found in the database.")
            return

        # Loop through each movie and generate reviews
        for movie in movies:
            num_reviews = random.randint(5, 10)  # Generate 5 to 10 reviews per movie
            total_rating = 0  # Track total rating for calculating average

            for _ in range(num_reviews):
                rating = random.uniform(1.0, 5.0)  # Random rating between 1 and 5
                comment = random.choice(comments)  # Random comment
                username = random.choice(usernames)  # Random username
                
                # Create a new review
                review = Review(
                    movie_id=movie.movie_id,
                    username=username,
                    review_time=datetime.now(),
                    review_rating=round(rating, 1),  # Round rating to 1 decimal place
                    review_comment=comment
                )
                session.add(review)
                total_rating += rating

            # Calculate and update the average rating for the movie
            avg_rating = round(total_rating / num_reviews, 1)  # Average rating rounded to 1 decimal place
            movie.average_rating = avg_rating

        # Commit the transaction
        session.commit()
        print("Reviews and average ratings added successfully!")

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

# Call the function to populate reviews
generate_reviews()