from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base 
from datetime import datetime

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, autoincrement=True)
    seller_cpf = Column(String, ForeignKey('sellers.cpf'), nullable=False)
    value = Column(Float, nullable=False)
    channel = Column(String, nullable=False)
    commission = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    client_type = Column(String, nullable=False)
    currency = Column(String, nullable=False)

    seller = relationship('Seller')