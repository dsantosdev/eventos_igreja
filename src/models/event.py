from sqlalchemy import Column, Integer, String
from src.database.db_manager import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(String, nullable=False)
    location = Column(String, nullable=False)

    def __repr__(self):
        return f"<Event(name='{self.name}', date='{self.date}', location='{self.location}')>"