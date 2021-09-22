# TODO: Je suis partie sur ce genre de model car il n'est pas ammener à évoluer.
#    Sur un projet plus "évoluer", j'aurais créé une table Author séparé.

"""Models tables intervention database"""
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
