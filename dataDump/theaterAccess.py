import random
from sqlalchemy import create_engine, Column, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database model
Base = declarative_base()

class Theater(Base):
    __tablename__ = 'theaters'
    theater_id = Column(String, primary_key=True)  # UUID as a string
    theater_name = Column(String, nullable=False)
    theater_location = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)  # Latitude column
    longitude = Column(Float, nullable=True)  # Longitude column
    accessibility = Column(Boolean, nullable=True)  # Accessibility column

# Database connection (update with your PostgreSQL credentials)
DATABASE_URL = "postgresql://avnadmin:AVNS_B__mg-mo4ERejoa7Rh9@pg-235500ec-shreedharjoshi03-f6ce.b.aivencloud.com:10885/defaultdb"  # Replace with your database URL
engine = create_engine(DATABASE_URL)

# Create the theaters table (if not already created)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Fetch all theaters from the database
theaters = session.query(Theater).all()

# Randomly assign 50% of theaters as accessible
for theater in theaters:
    theater.accessibility = random.choice([True, False])  # Randomly assign True or False

# Commit the updates to the database
session.commit()

print("Accessibility updated successfully for all theaters!")