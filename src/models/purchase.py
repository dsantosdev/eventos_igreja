from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.models.event import Base, Event

class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True)
    buyer_name = Column(String, nullable=False)
    purchase_date = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    ticket_quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    event = relationship("Event")

    def __repr__(self):
        return f"<Purchase(buyer_name='{self.buyer_name}', event_id={self.event_id}, ticket_quantity={self.ticket_quantity})>"