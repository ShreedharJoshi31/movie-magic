from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

# Transaction Table
class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(String, primary_key=True)  # UUID as a string
    user_id = Column(String, nullable=False)  # User ID (could be a UUID or string)
    payment_status = Column(Boolean, nullable=False, default=False)  # True = Paid, False = Pending
    transaction_time = Column(DateTime, default=datetime.now(), nullable=False)

    # Relationship to bookings
    bookings = relationship("Booking", back_populates="transaction")


# Bookings Table
class Booking(Base):
    __tablename__ = 'bookings'

    booking_id = Column(Integer, primary_key=True, autoincrement=True)  # Unique booking ID
    user_id = Column(String, nullable=False)  # User ID (same as in Transaction)
    transaction_id = Column(String, ForeignKey('transactions.transaction_id'), nullable=False)  # FK to Transaction
    user_name = Column(String, nullable=False)  # User's name
    movie_name = Column(String, nullable=False)  # Movie name
    theater = Column(String, nullable=False)  # Theater name
    show_time = Column(DateTime, nullable=False)  # Show date and time
    seat = Column(String, nullable=False)  # Seat number (e.g., A1, B3)
    booking_time = Column(DateTime, default=datetime.now(), nullable=False)  # Booking timestamp

    # Relationship to transaction
    transaction = relationship("Transaction", back_populates="bookings")


# Database connection
engine = create_engine('postgresql://avnadmin:AVNS_B__mg-mo4ERejoa7Rh9@pg-235500ec-shreedharjoshi03-f6ce.b.aivencloud.com:10885/defaultdb', echo=True)  # Update with your database URL

# Create all tables
Base.metadata.create_all(engine)
print("Transaction and Booking tables created successfully!")