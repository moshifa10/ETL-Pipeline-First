from config.extensions import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime


class InvaliTransactions(Base):

    __tablename__ = "invalid_transaction"

    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, nullable=False)
    product = Column(String, nullable=True)
    category = Column(String, nullable=True)
    quantity = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    description = Column(String, nullable=False)
    load_date = Column(DateTime, default=datetime.now())

