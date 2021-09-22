# TODO: La calss SqliteManager me permet d'initialiser la connection à la DB
#   Les méthodes clean_table / create_table / delete_table sont surtout là pour les test ou pour la 1er utilisation
#   Normalement je fais toutes mes requetes Sql ici, mais vu que l'application est petite, elles sont directement dans les routes

"""Manage request SQLAlchemy"""
import os
from pathlib import Path

from sqlalchemy import MetaData, create_engine, delete
from sqlalchemy.orm import sessionmaker

from app.models import Base
from app.models.intervention import Intervention
from app.tools import config


class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class SqliteManager:
    """
    Connection database
    """

    def __init__(self):
        """
        init class
        """
        if os.environ.get("ENV") == "test":
            db_url = os.environ.get("URL_DB_TEST")
        else:
            db_url = f"sqlite:///{os.path.join(Path(__file__).parents[2], 'ticket.db')}"
        self.engine = create_engine(db_url)
        self.conn = self.engine.connect()
        self.metadata = MetaData()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.Base = Base

    def create_tables(self):
        """
        Create all table in DB
        """
        self.Base.metadata.create_all(self.engine)

    def delete_all_table(self):
        """
        Delete all table in DB
        """
        self.Base.metadata.drop_all(self.engine)

    def clean_all_table(self):
        """
        Delete all data in the table
        """
        delete_table_sigmat = delete(Intervention)

        connection = self.engine.connect()
        connection.execute(delete_table_sigmat)
