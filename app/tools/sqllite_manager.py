"""Manage request postgresql"""
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
    Connection postgreSQL
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
        self.create_tables()

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

    def add_intervention(self, intervention: dict) -> bool:
        """
        method for add one intervention
        """

        # Check is intervention exist
        result = self.session.query(Intervention).filter_by(
            label=intervention['label'],
            description=intervention['description'],
            author=intervention['author'],
            location=intervention['location'],
            date_intervention=intervention['date_intervention'],
        ).all()

        if len(result) == 0:
            add_intervention = Intervention(
                label=intervention['label'],
                description=intervention['description'],
                author=intervention['author'],
                location=intervention['location'],
                date_intervention=intervention['date_intervention'],
            )
            self.session.add(add_intervention)
            self.session.commit()

            return True
        return False
