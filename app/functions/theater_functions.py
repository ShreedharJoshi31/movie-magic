from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db  # Import the get_db function
from schemas.models import Theater, Showtime , Movie # SQLAlchemy model
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

def get_theaters_by_location(location: str):
    """
    Fetches theaters by a specific location.

    Args:
    - location: The location (city, area, etc.) to search theaters by.

    Returns:
    - List of theaters that match the specified location, unmarshalled into a dictionary.
    """
    with next(get_db()) as db:
        results = db.execute(
            select(Theater).where(Theater.theater_location == location).limit(10)
        ).scalars().all()
        
        return [theater.__dict__ for theater in results]

def get_nearby_theaters(user_lat: float, user_lon: float, radius_km: float = 10):
    """
    Fetches theaters within a given radius from the user's location.

    Args:
    - user_lat: Latitude of the user's location.
    - user_lon: Longitude of the user's location.
    - radius_km: Radius in kilometers to search for theaters (default is 10 km).

    Returns:
    - List of nearby theaters within the radius, unmarshalled into a dictionary.
    """
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Radius of Earth in kilometers
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    with next(get_db()) as db:
        theaters = db.execute(select(Theater).where(Theater.latitude.isnot(None), Theater.longitude.isnot(None)).limit(10)).scalars().all()
        nearby_theaters = []

        for theater in theaters:
            distance = haversine(user_lat, user_lon, theater.latitude, theater.longitude)
            if distance <= radius_km:
                nearby_theaters.append(theater.__dict__)

        return nearby_theaters
    
def get_accessible_theaters():
    """
    Fetches theaters that are accessible.

    Returns:
    - List of accessible theaters, unmarshalled into a dictionary.
    """
    with next(get_db()) as db:
        results = db.execute(
            select(Theater).where(Theater.accessibility == True).limit(10)
        ).scalars().all()
        
        return [theater.__dict__ for theater in results]
    

def get_showtimes_by_theater(theater_id: str):
    """
    Fetches showtimes for a specific theater.

    Args:
    - theater_id: The ID of the theater to fetch showtimes for.

    Returns:
    - List of showtimes for the given theater, unmarshalled into a dictionary.
    """
    with next(get_db()) as db:
        results = db.execute(
            select(Showtime).where(Showtime.theater_id == theater_id).limit(10)
        ).scalars().all()
        
        return [showtime.__dict__ for showtime in results]
    

def get_movie_showtimes_near_location(movie_name: str, user_lat: float, user_lon: float, start_time: str, end_time: str, radius_km: float = 10):
    """
    Fetches showtimes for a specific movie near a location and within a specific time range.

    Args:
    - movie_name: The name of the movie to search for.
    - user_lat: Latitude of the user's location.
    - user_lon: Longitude of the user's location.
    - start_time: The start of the time range in 'YYYY-MM-DD HH:MM:SS' format.
    - end_time: The end of the time range in 'YYYY-MM-DD HH:MM:SS' format.
    - radius_km: Radius in kilometers to search for theaters (default is 10 km).

    Returns:
    - List of showtimes for the given movie near the location and within the time range.
    """
    # Get nearby theaters
    nearby_theaters = get_nearby_theaters(user_lat, user_lon, radius_km)
    nearby_theater_ids = [theater['theater_id'] for theater in nearby_theaters]

    if not nearby_theater_ids:
        return []

    with next(get_db()) as db:
        # Find the movie by name
        movie = db.execute(
            select(Movie).where(Movie.movie_name == movie_name).limit(20)
        ).scalars().first()

        if not movie:
            return []

        # Query showtimes for the movie in nearby theaters within the time range
        results = db.execute(
            select(Showtime)
            .where(
                Showtime.movie_id == movie.movie_id,
                Showtime.theater_id.in_(nearby_theater_ids),
                Showtime.show_time >= start_time,
                Showtime.show_time <= end_time
            )
        ).scalars().all()
        
        return [showtime.__dict__ for showtime in results]
    
def get_showtimes_by_theater_name(theater_name: str):
    """
    Fetches all showtimes for a specific theater by its name.

    Args:
    - theater_name: The name of the theater to search for.

    Returns:
    - List of showtimes for the given theater, or an empty list if no theater is found.
    """
    with next(get_db()) as db:
        # Find the theater by name
        theater = db.execute(
            select(Theater).where(Theater.theater_name == theater_name).limit(20)
        ).scalars().first()

        if not theater:
            return {"error": f"Theater with name '{theater_name}' not found."}

        # Fetch showtimes for the theater
        showtimes = db.execute(
            select(Showtime).where(Showtime.theater_id == theater.theater_id)
        ).scalars().all()

        # Convert showtimes to dictionary format
        return {
            "theater": theater.__dict__,
            "showtimes": [showtime.__dict__ for showtime in showtimes]
        }