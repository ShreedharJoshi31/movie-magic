# app/controllers/seatmap_controller.py

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from app.services.seatmap_service import SeatMapService
from app.schemas.schemas import (
    SeatMapResponse,
    CreateSeatMapRequest,
    BookSeatsRequest,
    UpdateCategoryPriceRequest
)
from app.database import get_db

async def create_seatmap(
    showtime_id: int,
    seat_layout: CreateSeatMapRequest,
    db: Session = Depends(get_db)
) -> List[SeatMapResponse]:
    """
    Handle seatmap creation for a showtime.
    """
    try:
        seats = SeatMapService.create_seatmap_for_showtime(
            db=db,
            showtime_id=showtime_id,
            seat_layout=seat_layout.seats
        )
        return seats
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

async def get_seatmap(
    showtime_id: int,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Get complete seatmap for a showtime.
    """
    try:
        seatmap = SeatMapService.get_showtime_seatmap(
            db=db,
            showtime_id=showtime_id
        )
        if not seatmap:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seatmap not found"
            )
        return seatmap
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def get_available_seats(
    showtime_id: int,
    db: Session = Depends(get_db)
) -> List[SeatMapResponse]:
    """
    Get all available seats for a showtime.
    """
    try:
        seats = SeatMapService.get_available_seats(
            db=db,
            showtime_id=showtime_id
        )
        return seats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def get_category_availability(
    showtime_id: int,
    category: str,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Get availability information for a specific seat category.
    """
    try:
        availability = SeatMapService.get_category_availability(
            db=db,
            showtime_id=showtime_id,
            category=category
        )
        if not availability:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category {category} not found"
            )
        return availability
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def book_seats(
    showtime_id: int,
    request: BookSeatsRequest,
    db: Session = Depends(get_db)
) -> List[SeatMapResponse]:
    """
    Handle booking multiple seats.
    """
    try:
        booked_seats = SeatMapService.book_seats(
            db=db,
            showtime_id=showtime_id,
            seat_numbers=request.seat_numbers
        )
        return booked_seats
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def release_seats(
    showtime_id: int,
    request: BookSeatsRequest,
    db: Session = Depends(get_db)
) -> List[SeatMapResponse]:
    """
    Handle releasing (unbooking) multiple seats.
    """
    try:
        released_seats = SeatMapService.release_seats(
            db=db,
            showtime_id=showtime_id,
            seat_numbers=request.seat_numbers
        )
        return released_seats
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def update_category_price(
    showtime_id: int,
    category: str,
    request: UpdateCategoryPriceRequest,
    db: Session = Depends(get_db)
) -> List[SeatMapResponse]:
    """
    Handle updating price for all seats in a category.
    """
    try:
        updated_seats = SeatMapService.update_category_price(
            db=db,
            showtime_id=showtime_id,
            category=category,
            new_price=request.new_price
        )
        if not updated_seats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category {category} not found"
            )
        return updated_seats
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )