from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class PassengerProfile(Base):
    __tablename__ = "passenger_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    passport_number = Column(String)
    nationality = Column(String)
    date_of_birth = Column(Date)
    
    # Relationships
    user = relationship("User", back_populates="passenger_profile")
    tickets = relationship("Ticket", back_populates="passenger")

