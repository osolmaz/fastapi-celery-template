# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
