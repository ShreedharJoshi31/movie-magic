import json
import googlemaps
from sqlalchemy import create_engine, Column, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize Google Maps client
GOOGLE_MAPS_API_KEY = ""  # Replace with your actual API key
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# Define the database model
Base = declarative_base()

class Theater(Base):
    __tablename__ = 'theaters'
    theater_id = Column(String, primary_key=True)  # UUID as a string
    theater_name = Column(String, nullable=False)
    theater_location = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)  # New column for latitude
    longitude = Column(Float, nullable=True)  # New column for longitude
    accessibility = Column(Boolean, nullable=True)  # New column for accessibility

# Database connection (update with your PostgreSQL credentials)
DATABASE_URL = ""  # Replace with your database URL
engine = create_engine(DATABASE_URL)

# Create the theaters table (if not already created)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Function to get latitude and longitude for a location
def get_lat_lon(location):
    try:
        geocode_result = gmaps.geocode(location)
        if geocode_result:
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            return lat, lng
    except Exception as e:
        print(f"Error fetching geocode for {location}: {e}")
    return None, None

# Fetch all theaters from the database
theaters = session.query(Theater).all()

# Update latitude and longitude for each theater
for theater in theaters:
    if theater.latitude is None or theater.longitude is None:  # Only update if not already set
        print(f"Fetching coordinates for location: {theater.theater_location}")
        latitude, longitude = get_lat_lon(theater.theater_location)
        if latitude is not None and longitude is not None:
            theater.latitude = latitude
            theater.longitude = longitude
            print(f"Updated {theater.theater_name} with lat: {latitude}, lon: {longitude}")
        else:
            print(f"Could not fetch coordinates for {theater.theater_location}")

# Commit the updates to the database
session.commit()

print("Latitude and Longitude updated successfully for all theaters!")