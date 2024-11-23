from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.models import SeatMap
from app.repositories.base import BaseRepository


class SeatMapRepository(BaseRepository):
    @staticmethod
    def create_seat(db: Session, seat_data: dict) -> SeatMap:
        """
        Create a new seat in the seatmap.

        :param db: Database session
        :param seat_data: Dictionary containing seat data
        :return: The created SeatMap object
        """
        return BaseRepository.create_entry(db=db, model=SeatMap, data=seat_data)

    @staticmethod
    def get_seat_by_id(db: Session, seatmap_id: int) -> Optional[SeatMap]:
        """
        Retrieve a seat by its ID.

        :param db: Database session
        :param seatmap_id: ID of the seat
        :return: The SeatMap object or None if not found
        """
        return BaseRepository.get_entry_by_id(db=db, model=SeatMap, seatmap_id=seatmap_id)

    @staticmethod
    def get_seats_by_showtime(db: Session, showtime_id: int) -> List[SeatMap]:
        """
        Retrieve all seats for a specific showtime.

        :param db: Database session
        :param showtime_id: ID of the showtime
        :return: List of SeatMap objects
        """
        try:
            return db.query(SeatMap).filter(SeatMap.showtime_id == showtime_id).all()
        except Exception as e:
            raise e

    @staticmethod
    def get_available_seats(db: Session, showtime_id: int) -> List[SeatMap]:
        """
        Retrieve all available seats for a specific showtime.

        :param db: Database session
        :param showtime_id: ID of the showtime
        :return: List of available SeatMap objects
        """
        try:
            return db.query(SeatMap).filter(
                SeatMap.showtime_id == showtime_id,
                SeatMap.seat_status == False  # False means available
            ).all()
        except Exception as e:
            raise e

    @staticmethod
    def get_seats_by_category(db: Session, showtime_id: int, seat_category: str) -> List[SeatMap]:
        """
        Retrieve all seats of a specific category for a showtime.

        :param db: Database session
        :param showtime_id: ID of the showtime
        :param seat_category: Category of seats (e.g., VIP, Regular)
        :return: List of SeatMap objects
        """
        try:
            return db.query(SeatMap).filter(
                SeatMap.showtime_id == showtime_id,
                SeatMap.seat_category == seat_category
            ).all()
        except Exception as e:
            raise e

    @staticmethod
    def update_seat_status(db: Session, seatmap_id: int, is_booked: bool) -> Optional[SeatMap]:
        """
        Update a seat's booking status.

        :param db: Database session
        :param seatmap_id: ID of the seat to update
        :param is_booked: New booking status
        :return: The updated SeatMap object or None if not found
        """
        update_data = {"seat_status": is_booked}
        return BaseRepository.update_entry(db=db, model=SeatMap, update_data=update_data, seatmap_id=seatmap_id)

    @staticmethod
    def update_seat_price(db: Session, seatmap_id: int, new_price: float) -> Optional[SeatMap]:
        """
        Update a seat's price.

        :param db: Database session
        :param seatmap_id: ID of the seat to update
        :param new_price: New price for the seat
        :return: The updated SeatMap object or None if not found
        """
        update_data = {"seat_price": new_price}
        return BaseRepository.update_entry(db=db, model=SeatMap, update_data=update_data, seatmap_id=seatmap_id)

    @staticmethod
    def delete_seat(db: Session, seatmap_id: int) -> bool:
        """
        Delete a seat from the seatmap.

        :param db: Database session
        :param seatmap_id: ID of the seat to delete
        :return: True if deleted, False if not found
        """
        return BaseRepository.hard_delete_entry(db=db, model=SeatMap, seatmap_id=seatmap_id)

    @staticmethod
    def bulk_create_seats(db: Session, seats_data: List[dict]) -> List[SeatMap]:
        """
        Create multiple seats at once.

        :param db: Database session
        :param seats_data: List of dictionaries containing seat data
        :return: List of created SeatMap objects
        """
        try:
            seats = [SeatMap(**seat_data) for seat_data in seats_data]
            db.bulk_save_objects(seats)
            db.commit()
            return seats
        except Exception as e:
            db.rollback()
            raise e