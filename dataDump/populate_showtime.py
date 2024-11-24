import random
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    ForeignKey,
    DateTime,
    Enum,
    Float,
    Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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

# Theater Table
class Theater(Base):
    __tablename__ = 'theaters'
    theater_id = Column(String, primary_key=True)  # UUID as a string
    theater_name = Column(String, nullable=False)
    theater_location = Column(String, nullable=False)

    # Relationship to showtimes
    showtimes = relationship("Showtime", back_populates="theater")


# Movie Table
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

    # Relationship to showtimes
    showtimes = relationship("Showtime", back_populates="movie")

# Database connection (replace with your database URL)
engine = create_engine('')  # Change URL for your database
Session = sessionmaker(bind=engine)
session = Session()

def populate_showtimes():
    """
    Populates the 'showtimes' table with randomized intervals for showtimes
    for the next month. Intervals are chosen randomly from predefined options.
    """
    try:
        # Fetch all theaters and movies from the database
        theaters = session.query(Theater).all()
        movies = session.query(Movie).all()

        if not theaters or not movies:
            print("No theaters or movies found in the database.")
            return

        # Define random intervals (in hours) for showtimes
        intervals = [3, 5, 8, 12, 24]  # Possible intervals between showtimes in hours

        # Generate showtimes for the next month
        today = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)  # Start at 10:00 AM today
        end_date = today + timedelta(days=30)  # Generate showtimes for the next 30 days

        # Iterate through each theater
        for theater in theaters:
            current_time = today

            while current_time < end_date:
                # Randomly select a movie
                random_movie = random.choice(movies)

                # Create a new showtime entry
                new_showtime = Showtime(
                    theater_id=theater.theater_id,
                    movie_id=random_movie.movie_id,
                    language=random_movie.language,  # Use movie language by default
                    show_time=current_time
                )
                session.add(new_showtime)

                # Randomly increment the current time by one of the intervals
                random_interval = random.choice(intervals)
                current_time += timedelta(hours=random_interval)

        # Commit all new showtimes to the database
        session.commit()
        print("Showtimes successfully populated with randomized intervals for the next month!")

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

# Call the function to populate the showtimes
populate_showtimes()

# Call the function to populate the showtimes
populate_showtimes()