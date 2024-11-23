from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from app.repositories.seatmap_repository import SeatMapRepository
from app.schemas.models import SeatMap
from fastapi import HTTPException


class SeatMapService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = SeatMapRepository()

    def create_seatmap_for_showtime(self, showtime_id: int, seat_layout: List[Dict]) -> List[SeatMap]:
        """
        Create a complete seatmap for a showtime.

        :param showtime_id: ID of the showtime
        :param seat_layout: List of seat configurations
        :return: List of created seats
        """
        try:
            # Add showtime_id to each seat configuration
            for seat in seat_layout:
                seat['showtime_id'] = showtime_id

            return self.repository.bulk_create_seats(self.db, seat_layout)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create seatmap: {str(e)}"
            )

    def get_showtime_seatmap(self, showtime_id: int) -> Dict:
        """
        Get complete seatmap information for a showtime.

        :param showtime_id: ID of the showtime
        :return: Dictionary containing seatmap details
        """
        try:
            seats = self.repository.get_seats_by_showtime(self.db, showtime_id)
            
            # Organize seats by category
            seatmap = {}
            for seat in seats:
                category = seat.seat_category
                if category not in seatmap:
                    seatmap[category] = {
                        'price': seat.seat_price,
                        'seats': []
                    }
                seatmap[category]['seats'].append({
                    'seat_no': seat.seat_no,
                    'status': seat.seat_status
                })
            
            return seatmap
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve seatmap: {str(e)}"
            )

    def get_available_seats(self, showtime_id: int) -> List[SeatMap]:
        """
        Get all available seats for a showtime.

        :param showtime_id: ID of the showtime
        :return: List of available seats
        """
        try:
            return self.repository.get_available_seats(self.db, showtime_id)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve available seats: {str(e)}"
            )

    def get_category_availability(self, showtime_id: int, category: str) -> Dict:
        """
        Get availability information for a specific seat category.

        :param showtime_id: ID of the showtime
        :param category: Seat category (e.g., VIP, Regular)
        :return: Dictionary with availability information
        """
        try:
            seats = self.repository.get_seats_by_category(self.db, showtime_id, category)
            total_seats = len(seats)
            available_seats = len([seat for seat in seats if not seat.seat_status])
            
            return {
                'category': category,
                'total_seats': total_seats,
                'available_seats': available_seats,
                'price': seats[0].seat_price if seats else None
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve category availability: {str(e)}"
            )

    def book_seats(self, showtime_id: int, seat_numbers: List[str]) -> List[SeatMap]:
        """
        Book multiple seats for a showtime.

        :param showtime_id: ID of the showtime
        :param seat_numbers: List of seat numbers to book
        :return: List of updated seat objects
        """
        try:
            booked_seats = []
            for seat_no in seat_numbers:
                seats = self.db.query(SeatMap).filter(
                    SeatMap.showtime_id == showtime_id,
                    SeatMap.seat_no == seat_no
                ).all()

                if not seats:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Seat {seat_no} not found"
                    )

                seat = seats[0]
                if seat.seat_status:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Seat {seat_no} is already booked"
                    )

                updated_seat = self.repository.update_seat_status(
                    self.db, 
                    seat.seatmap_id, 
                    True
                )
                booked_seats.append(updated_seat)

            return booked_seats
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to book seats: {str(e)}"
            )

    def release_seats(self, showtime_id: int, seat_numbers: List[str]) -> List[SeatMap]:
        """
        Release (unbook) multiple seats for a showtime.

        :param showtime_id: ID of the showtime
        :param seat_numbers: List of seat numbers to release
        :return: List of updated seat objects
        """
        try:
            released_seats = []
            for seat_no in seat_numbers:
                seats = self.db.query(SeatMap).filter(
                    SeatMap.showtime_id == showtime_id,
                    SeatMap.seat_no == seat_no
                ).all()

                if not seats:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Seat {seat_no} not found"
                    )

                seat = seats[0]
                if not seat.seat_status:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Seat {seat_no} is already available"
                    )

                updated_seat = self.repository.update_seat_status(
                    self.db, 
                    seat.seatmap_id, 
                    False
                )
                released_seats.append(updated_seat)

            return released_seats
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to release seats: {str(e)}"
            )

    def update_category_price(self, showtime_id: int, category: str, new_price: float) -> List[SeatMap]:
        """
        Update price for all seats in a category.

        :param showtime_id: ID of the showtime
        :param category: Seat category to update
        :param new_price: New price for the category
        :return: List of updated seat objects
        """
        try:
            seats = self.repository.get_seats_by_category(self.db, showtime_id, category)
            updated_seats = []
            
            for seat in seats:
                updated_seat = self.repository.update_seat_price(
                    self.db,
                    seat.seatmap_id,
                    new_price
                )
                updated_seats.append(updated_seat)
                
            return updated_seats
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update category price: {str(e)}"
            )