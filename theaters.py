import json
import uuid
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database model
Base = declarative_base()

class Theater(Base):
    __tablename__ = 'theaters'
    theater_id = Column(String, primary_key=True)  # UUID as a string
    theater_name = Column(String, nullable=False)
    theater_location = Column(String, nullable=False)

# Database connection (update with your PostgreSQL credentials)
DATABASE_URL = "postgresql://avnadmin:AVNS_B__mg-mo4ERejoa7Rh9@pg-235500ec-shreedharjoshi03-f6ce.b.aivencloud.com:10885/defaultdb"
engine = create_engine(DATABASE_URL)

# Create the theaters table
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Read the JSON file
with open('theaters.json', 'r') as file:
    theaters_data = json.load(file)

# Insert data into the database
for theater in theaters_data:
    theater_entry = Theater(
        theater_id=theater['theater_id'],
        theater_name=theater['theater_name'],
        theater_location=theater['theater_location']
    )
    session.add(theater_entry)

# Commit the session
session.commit()

print(f"{len(theaters_data)} theaters inserted successfully!")