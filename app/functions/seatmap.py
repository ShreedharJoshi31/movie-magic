from schemas.models import SeatMap, Transaction, Booking, Showtime, Movie, Theater
from sqlalchemy.orm import Session
import uuid
from database import get_db  # Import the get_db function
from datetime import datetime
from sqlalchemy import select
from functions.payment_functions import create_razorpay_order

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
    

def book_seat(email: str, showtime_id: int, seat_no: str, price: float, category: str):
    """
    Books a seat for a given showtime using the user's email and handles payment via Razorpay.

    Args:
    - email: The email of the user (used to identify the user).
    - showtime_id: The ID of the showtime.
    - seat_no: The seat number to book (e.g., 'A1').
    - price: The price of the seat.
    - category: The category of the seat (Recliner, Gold, Silver).

    Returns:
    - A dictionary indicating success or failure of the booking.
    """
    try:
        with next(get_db()) as db:
            # Generate a unique transaction ID
            transaction_id = str(uuid.uuid4())

            # Create a new transaction with payment_status=False initially
            transaction = Transaction(
                transaction_id=transaction_id,
                user_id=email,  # Using email as the user ID
                payment_status=False,  # Payment status will be updated after Razorpay response
                transaction_time=datetime.now()
            )
            db.add(transaction)
            db.commit()  # Commit the new transaction to capture it in case of failure

            # Call the Razorpay payment function
            payment_response = create_razorpay_order(price)

            if not payment_response["success"]:
                # If payment fails, return an error and update the transaction
                transaction.payment_status = False
                db.commit()  # Update the transaction with the failed payment status
                return {
                    "error": "Payment failed",
                    "details": payment_response["error"]
                }

            # Update transaction to reflect successful payment
            transaction.payment_status = True
            db.commit()

            # Fetch the showtime details
            showtime = db.execute(select(Showtime).where(Showtime.showtime_id == showtime_id)).scalars().first()
            if not showtime:
                return {"error": f"Showtime with ID {showtime_id} does not exist."}

            # Fetch the movie and theater details
            movie = db.execute(select(Movie).where(Movie.movie_id == showtime.movie_id)).scalars().first()
            theater = db.execute(select(Theater).where(Theater.theater_id == showtime.theater_id)).scalars().first()

            if not movie or not theater:
                return {"error": "Movie or Theater details could not be found."}

            # Create a new seat entry and mark it as booked
            seat = SeatMap(
                showtime_id=showtime_id,
                seat_no=seat_no,
                seat_category=category,
                seat_price=price,
                seat_status=True  # Mark the seat as booked
            )
            db.add(seat)

            # Create a new booking
            booking = Booking(
                user_id=email,  # Using email as the user ID
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

            return {
                "success": f"Seat {seat_no} successfully booked for {movie.movie_name} at {theater.theater_name} on {showtime.show_time}.",
                "payment_order": payment_response["order"]  # Include Razorpay order details in the response
            }

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

def get_seat_prices(seat_no: str):
    """
    Returns the price of a given seat based on its seat number and category.

    Args:
    - seat_no: The seat number (e.g., 'A1').

    Returns:
    - The price of the seat.
    """
    return """
    if the seat_no starts with 'A' or 'B': it is a Recliner seat with price 700
    if the seat_no starts with 'C' or 'D': it is a Gold seat with price 500
    if the seat_no starts with 'E' or 'F' or 'G': it is a Silver seat with price 300
    """