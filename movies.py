import json
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database model
Base = declarative_base()

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

# Database connection (update with your PostgreSQL credentials)
DATABASE_URL = "postgresql://avnadmin:AVNS_B__mg-mo4ERejoa7Rh9@pg-235500ec-shreedharjoshi03-f6ce.b.aivencloud.com:10885/defaultdb"
engine = create_engine(DATABASE_URL)

# Create the movies table
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Read the JSON file
with open('movies.json', 'r') as file:
    movies_data = json.load(file)

# Insert data into the database
for movie in movies_data:
    movie_entry = Movie(
        movie_id=movie['movie_id'],
        movie_name=movie['movie_name'],
        movie_description=movie['movie_description'],
        genre=movie['genre'],
        cast=movie['cast'],
        language=movie['language'],
        mood=movie['mood'],
        average_rating=movie['average_rating']
    )
    session.add(movie_entry)

# Commit the session
session.commit()

print("Movies data inserted successfully!")