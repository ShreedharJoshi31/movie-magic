# app/routes/seatmap_routes.py

from fastapi import APIRouter
from app.controllers.seatmap_controller import (
    create_seatmap,
    get_seatmap,
    get_available_seats,
    get_category_availability,
    book_seats,
    release_seats,
    update_category_price
)
from app.schemas.schemas import (
    SeatMapResponse,
    CategoryAvailabilityResponse,
    CreateSeatMapRequest,
    BookSeatsRequest,
    UpdateCategoryPriceRequest
)

router = APIRouter(prefix="/api/seatmap", tags=["seatmap"])

# Register the routes and map to the controller functions
router.post("/{showtime_id}", response_model=list[SeatMapResponse])(create_seatmap)
router.get("/{showtime_id}")(get_seatmap)
router.get("/{showtime_id}/available", response_model=list[SeatMapResponse])(get_available_seats)
router.get("/{showtime_id}/category/{category}", response_model=CategoryAvailabilityResponse)(get_category_availability)
router.post("/{showtime_id}/book", response_model=list[SeatMapResponse])(book_seats)
router.post("/{showtime_id}/release", response_model=list[SeatMapResponse])(release_seats)
router.put("/{showtime_id}/category/{category}/price", response_model=list[SeatMapResponse])(update_category_price)