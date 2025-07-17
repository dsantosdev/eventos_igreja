# src/models/participant.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    registration_date = Column(String, nullable=False)

    def __repr__(self):
        return f"<Participant(name='{self.name}', email='{self.email}', event_id={self.event_id})>"