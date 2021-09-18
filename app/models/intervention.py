"""Models of the tables Sigmat of the postgres database"""
from sqlalchemy import Column, DateTime, Integer, String, Text

from app.models import Base


class Intervention(Base):
    """
    Model table Sigmat
    """

    __tablename__ = "intervention"

    intervention_id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(255))
    description = Column(Text)
    author = Column(String())
    location = Column(String())
    date_intervention = Column(DateTime)
