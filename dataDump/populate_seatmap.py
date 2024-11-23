import random
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
# Step 1: Database connection
engine = create_engine('')  # Update with your database URL
Session = sessionmaker(bind=engine)
session = Session()

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
    # showtime = relationship("Showtime", back_populates="seatmap")


# Showtimes Table
class Showtime(Base):
    __tablename__ = 'showtimes'

    showtime_id = Column(Integer, primary_key=True, autoincrement=True)
    theater_id = Column(String, ForeignKey('theaters.theater_id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), nullable=False)
    language = Column(String, nullable=False)
    show_time = Column(DateTime, nullable=False)


# Step 2: Populate seatmap
def populate_seatmap():
    try:
        # Fetch all showtimes
        showtimes = session.query(Showtime).all()

        if not showtimes:
            print("No showtimes found in the database.")
            return

        # Row and column definitions
        rows = ["A", "B", "C", "D", "E", "F", "G"]  # Rows A-G
        columns = list(range(1, 10))  # Columns 1-9

        # Seat category pricing
        seat_categories = {
            "Recliner": {"rows": ["A", "B"], "price": 700},
            "Gold": {"rows": ["C", "D"], "price": 500},
            "Silver": {"rows": ["E", "F", "G"], "price": 300},
        }

        # Randomly select up to 200 entries to populate
        total_seats_to_fill = 200
        seats_filled = 0

        while seats_filled < total_seats_to_fill:
            # Randomly select a showtime
            showtime = random.choice(showtimes)

            # Randomly select a seat
            row = random.choice(rows)
            col = random.choice(columns)
            seat_no = f"{row}{col}"  # Example: A1, B5

            # Determine seat category and price
            for category, details in seat_categories.items():
                if row in details["rows"]:
                    seat_category = category
                    seat_price = details["price"]
                    break

            # Randomly decide if the seat is occupied or unoccupied
            seat_status = random.choice([True, False])  # True = Occupied, False = Unoccupied

            # Check if the seat already exists for this showtime
            existing_seat = session.query(SeatMap).filter_by(
                showtime_id=showtime.showtime_id,
                seat_no=seat_no
            ).first()

            # If the seat doesn't exist, add it
            if not existing_seat:
                new_seat = SeatMap(
                    showtime_id=showtime.showtime_id,
                    seat_category=seat_category,
                    seat_price=seat_price,
                    seat_no=seat_no,
                    seat_status=seat_status
                )
                session.add(new_seat)
                seats_filled += 1

        # Commit all entries to the database
        session.commit()
        print(f"{seats_filled} seats successfully populated in the seatmap!")

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

# Call the function to populate the seatmap
populate_seatmap()