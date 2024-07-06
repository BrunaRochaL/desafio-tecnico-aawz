from sqlalchemy import Column, Integer, String, Date
from database.database import Base

class Seller(Base):
    __tablename__ = 'sellers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    email = Column(String, nullable=False)
    state = Column(String, nullable=False)
