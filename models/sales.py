from config.extensions import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime


class sale(Base):

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, nullable=False)
    product = Column(String, nullable=False)
    category = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    total_sale = Column(Integer, nullable=False)
    load_date = Column(DateTime, default=datetime.now())

