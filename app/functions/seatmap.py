from app.schemas.models import SeatMap, Transaction, Booking, Showtime, Movie, Theater
from sqlalchemy.orm import Session
import uuid
from app.database import get_db  # Import the get_db function
from datetime import datetime
from sqlalchemy import select

def get_seatmap_by_showtime(showtime_id: int):
    """
    Fetches the complete seat map for a given showtime, indicating which seats are booked.

    Args:
    - showtime_id: The ID of the showtime for which the seat map is needed.

    Returns:
    - A dictionary with the complete seat map, indicating booked and available seats.
    """
    try:
        with next(get_db()) as db:
            # Fetch all booked seats for the given showtime_id
            booked_seats = db.execute(select(SeatMap)
                                      .where(SeatMap.showtime_id == showtime_id)
                                      .limit(5)
                                      ).scalars().all()
            
            # Extract the booked seat numbers
            booked_seat_nos = {seat.seat_no for seat in booked_seats}

            # Define the rows and columns for the seat map
            rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
            columns = range(1, 10)  # Columns 1 to 9

            # Generate the complete seat map
            seatmap = {}
            for row in rows:
                for col in columns:
                    seat_no = f"{row}{col}"
                    seatmap[seat_no] = "Booked" if seat_no in booked_seat_nos else "Available"

            return seatmap

    except Exception as e:
        print(f"An error occurred while fetching the seat map: {e}")
        return {}
    

def book_seat(email: str, user_name: str, showtime_id: int, seat_no: str):
    """
    Books a seat for a given showtime using the user's email.

    Args:
    - email: The email of the user (used to identify the user).
    - user_name: The name of the user.
    - showtime_id: The ID of the showtime.
    - seat_no: The seat number to book (e.g., 'A1').

    Returns:
    - A dictionary indicating success or failure of the booking.
    """
    try:
        with next(get_db()) as db:
            # Validate the seat for the given showtime
            seat = db.execute(select(SeatMap)
                              .where(SeatMap.showtime_id == showtime_id, SeatMap.seat_no == seat_no)
                              ).scalars().first()

            if not seat:
                return {"error": f"Seat {seat_no} does not exist for showtime ID {showtime_id}."}
            if seat.seat_status:  # Seat is already booked
                return {"error": f"Seat {seat_no} is already booked."}

            # Mark the seat as booked
            seat.seat_status = True

            # Generate a unique transaction ID
            transaction_id = str(uuid.uuid4())

            # Create a new transaction
            transaction = Transaction(
                transaction_id=transaction_id,
                user_id=email,  # Using email as the user_id
                payment_status=True,  # Assuming payment is successful
                transaction_time=datetime.now()
            )
            db.add(transaction)

            # Fetch the showtime details
            showtime = db.execute(select(Showtime).where(Showtime.showtime_id == showtime_id)).scalars().first()
            if not showtime:
                return {"error": f"Showtime with ID {showtime_id} does not exist."}

            # Fetch the movie and theater details
            movie = db.execute(select(Movie).where(Movie.movie_id == showtime.movie_id)).scalars().first()
            theater = db.execute(select(Theater).where(Theater.theater_id == showtime.theater_id)).scalars().first()

            # Create a new booking
            booking = Booking(
                user_id=email,  # Using email as the user ID
                user_name=user_name,
                transaction_id=transaction_id,
                movie_name=movie.movie_name,
                theater=theater.theater_name,
                show_time=showtime.show_time,
                seat=seat_no,
                booking_time=datetime.now()
            )
            db.add(booking)

            # Commit the changes to the database
            db.commit()

            return {"success": f"Seat {seat_no} successfully booked for {movie.movie_name} at {theater.theater_name} on {showtime.show_time}."}

    except Exception as e:
        return {"error": f"An error occurred while booking the seat: {e}"}
    
def cancel_booking(email: str, seat_no: str, showtime_id: int):
    """
    Cancels a booking for a given user and seat using the user's email.

    Args:
    - email: The email of the user (used to identify the user).
    - seat_no: The seat number to cancel (e.g., 'A1').
    - showtime_id: The ID of the showtime.

    Returns:
    - A dictionary indicating success or failure of the cancellation.
    """
    try:
        with next(get_db()) as db:
            # Find the booking for the user based on their email
            booking = db.execute(select(Booking)
                                 .where(
                                     Booking.user_id == email,
                                     Booking.seat == seat_no,
                                     Booking.show_time == db.execute(
                                         select(Showtime.show_time).where(Showtime.showtime_id == showtime_id)
                                     ).scalar()
                                 )
                                 ).scalars().first()

            if not booking:
                return {"error": f"No booking found for email {email} and seat {seat_no}."}

            # Find and update the seat status
            seat = db.execute(select(SeatMap)
                              .where(SeatMap.showtime_id == showtime_id, SeatMap.seat_no == seat_no)
                              ).scalars().first()
            if seat:
                seat.seat_status = False  # Mark the seat as available

            # Delete the booking entry
            db.delete(booking)

            # Optionally delete the transaction if there are no other bookings under it
            transaction = db.execute(select(Transaction)
                                      .where(Transaction.transaction_id == booking.transaction_id)
                                      ).scalars().first()
            if transaction:
                other_bookings = db.execute(select(Booking)
                                            .where(Booking.transaction_id == transaction.transaction_id)
                                            ).scalars().all()
                if not other_bookings:  # No other bookings under this transaction
                    db.delete(transaction)

            # Commit the changes
            db.commit()

            return {"success": f"Booking for seat {seat_no} successfully canceled."}

    except Exception as e:
        return {"error": f"An error occurred while canceling the booking: {e}"}
    

def check_booking_by_email(email: str):
    """
    Checks all bookings for a user based on their email.

    Args:
    - email: The email of the user.

    Returns:
    - A list of dictionaries containing booking details, or an error message.
    """
    try:
        with next(get_db()) as db:
            # Fetch user bookings
            bookings = db.execute(select(Booking).where(Booking.user_id == email)).scalars().all()

            if not bookings:
                return {"error": f"No bookings found for email {email}."}

            # Prepare the booking details
            booking_details = []
            for booking in bookings:
                booking_details.append({
                    "movie_name": booking.movie_name,
                    "theater": booking.theater,
                    "show_time": booking.show_time,
                    "seat": booking.seat,
                    "booking_time": booking.booking_time,
                    "transaction_id": booking.transaction_id
                })

            return {"bookings": booking_details}

    except Exception as e:
        return {"error": f"An error occurred while fetching bookings: {e}"}