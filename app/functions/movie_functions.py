from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db  # Import the get_db function
from schemas.models import Movie, Showtime, Theater  # SQLAlchemy model
from datetime import datetime

def get_movies_by_name(movie_name: str):
    """
    This function fetches the top 5 movies that have a specific name.

    Args:
    - movie_name: The name of the movie to search for.

    Returns:
    - List of top 5 movies that match the given name, unmarshalled into a dictionary.
    """
    with next(get_db()) as db:
        results = db.execute(
            select(Movie).where(Movie.movie_name == movie_name)
            .limit(5)  # Limit to top 5 results
        ).scalars().all()

        # Convert the result to dictionary format
        return [movie.__dict__ for movie in results]

def get_movies_by_description(description: str):
    """
    This function fetches the top 5 movies whose description contains a specific keyword or phrase.

    Args:
    - description: The keyword or phrase to search for in the movie description.

    Returns:
    - List of top 5 movies whose description matches the given keyword or phrase, unmarshalled into a dictionary.
    """
    with next(get_db()) as db:
        results = db.execute(
            select(Movie).where(Movie.movie_description.like(f"%{description}%"))
            .limit(5)  # Limit to top 5 results
        ).scalars().all()
        
        # Convert the result to dictionary format
        return [movie.__dict__ for movie in results]

def get_movies_by_genre(genre: str):
    """
    This function fetches the top 5 movies of a specific genre.

    Args:
    - genre: The genre to filter movies by. Valid genres include:
      - Sci-Fi
      - Romance
      - Action/Sci-Fi
      - Mystery/Thriller
      - Drama/Fantasy
      - Historical Drama
      - Adventure
      - Thriller
      - Comedy/Drama
      - Action/Fantasy
      - Musical/Drama
      - Adventure/Drama
      - Horror
      - Tech Thriller
      - Slice of Life

    Returns:
    - List of top 5 movies that belong to the given genre, unmarshalled into a dictionary.
    """
    with next(get_db()) as db:
        results = db.execute(
            select(Movie).where(Movie.genre == genre)
            .limit(5)  # Limit to top 5 results
        ).scalars().all()
        
        # Convert the result to dictionary format
        return [movie.__dict__ for movie in results]

def get_movies_by_cast(cast: str):
    """
    This function fetches the top 5 movies that feature a specific cast member.

    Args:
    - cast: The name of the cast member to search for.

    Returns:
    - List of top 5 movies that feature the specified cast member, unmarshalled into a dictionary.
    """
    with next(get_db()) as db:
        results = db.execute(
            select(Movie).where(Movie.cast.like(f"%{cast}%"))
            .limit(5)  # Limit to top 5 results
        ).scalars().all()
        
        # Convert the result to dictionary format
        return [movie.__dict__ for movie in results]

def get_movies_by_language(language: str):
    """
    This function fetches the top 5 movies that are in a specific language.

    Args:
    - language: The language to filter movies by.

    Returns:
    - List of top 5 movies that are in the specified language, unmarshalled into a dictionary.
    """
    with next(get_db()) as db:
        results = db.execute(
            select(Movie).where(Movie.language == language)
            .limit(5)  # Limit to top 5 results
        ).scalars().all()
        
        # Convert the result to dictionary format
        return [movie.__dict__ for movie in results]

def get_movies_by_mood(mood: str):
    """
    This function fetches the top 5 movies that match a specific mood or theme.

    Args:
    - mood: The mood or theme to filter movies by. Valid moods include:
      - Intense
      - Romantic
      - Adventurous
      - Suspenseful
      - Emotional
      - Inspiring
      - Exciting
      - Creepy
      - Bittersweet
      - Heroic
      - Uplifting
      - Tense
      - Haunting
      - Engaging
      - Lighthearted

    Returns:
    - List of top 5 movies that match the given mood, unmarshalled into a dictionary.
    """
    with next(get_db()) as db:
        results = db.execute(
            select(Movie).where(Movie.mood == mood)
            .limit(5)  # Limit to top 5 results
        ).scalars().all()
        
        # Convert the result to dictionary format
        return [movie.__dict__ for movie in results]

def get_movies_by_average_rating(min_rating: float, max_rating: float = None):
    """
    This function fetches the top 5 movies that have an average rating within a specific range.

    Args:
    - min_rating: The minimum rating for the movie to be included.
    - max_rating: The optional maximum rating for the movie to be included. If not provided, only the minimum rating is considered.

    Returns:
    - List of top 5 movies that have an average rating within the specified range, unmarshalled into a dictionary.
    """
    with next(get_db()) as db:
        query = select(Movie).where(Movie.average_rating >= min_rating)
        if max_rating is not None:
            query = query.where(Movie.average_rating <= max_rating)
        
        results = db.execute(query.limit(5)).scalars().all()
        
        # Convert the result to dictionary format
        return [movie.__dict__ for movie in results]

def get_movies_by_showtime(start_time: str, end_time: str):
    """
    This function fetches the top 5 movies that have showtimes within a specific time range.

    Args:
    - start_time: The start of the time range in 'YYYY-MM-DD HH:MM:SS' format.
    - end_time: The end of the time range in 'YYYY-MM-DD HH:MM:SS' format.

    Returns:
    - List of top 5 movies with showtimes within the given range, unmarshalled into a dictionary.
    """
    with next(get_db()) as db:
        # Querying the Showtime and Movie tables based on the show_time range
        results = db.execute(
            select(Movie)
            .join(Showtime, Showtime.movie_id == Movie.movie_id)
            .where(Showtime.show_time >= start_time, Showtime.show_time <= end_time)
            .limit(5)  # Limit to top 5 results
        ).scalars().all()
        
        # Convert the result to dictionary format
        return [movie.__dict__ for movie in results]
    
def get_movies_by_name_with_showtimes_and_theatres(movie_name: str):
    """
    This function fetches the top 5 movies that have a specific name along with their showtimes and associated theater details.

    Args:
    - movie_name: The name of the movie to search for.

    Returns:
    - List of top 5 movies that match the given name, including their showtimes and theater details, unmarshalled into a dictionary.
    """
    with next(get_db()) as db:
        # Query to fetch movies, showtimes, and theater details
        results = db.execute(
            select(Movie)
            .join(Showtime, Showtime.movie_id == Movie.movie_id).limit(2)  # Join Movie with Showtime
            .join(Theater, Theater.theater_id == Showtime.theater_id).limit(2)  # Join Showtime with Theater
            .where(Movie.movie_name == movie_name)
            .limit(2)  # Limit to top 5 results
        ).scalars().all()

        # Convert the results to dictionary format including showtimes and theater details
        movies_with_showtimes = []
        for movie in results:
            movies_with_showtimes.append({
                "movie_id": movie.movie_id,
                "movie_name": movie.movie_name,
                "movie_description": movie.movie_description,
                "genre": movie.genre,
                "cast": movie.cast,
                "language": movie.language,
                "mood": movie.mood,
                "average_rating": movie.average_rating,
                "showtimes": [
                    {
                        "showtime_id": showtime.showtime_id,
                        "language": showtime.language,
                        "show_time": showtime.show_time,
                        "theater": {
                            "theater_id": showtime.theater.theater_id,
                            "theater_name": showtime.theater.theater_name,
                            "theater_location": showtime.theater.theater_location
                        }
                    }
                    for showtime in movie.showtimes  # Access the related showtimes
                ]
            })

        return movies_with_showtimes
