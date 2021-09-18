""" unit test for app import osmose"""
import json
import os
import unittest
from pathlib import Path
from datetime import datetime
from app import app as flask_app

from app.tools.sqllite_manager import SqliteManager
from app.models.intervention import Intervention


class TestRoutes(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["ENV"] = "test"
        os.environ[
            "URL_DB_TEST"
        ] = f"sqlite:///{os.path.join(Path(__file__).parents[2], 'ticket_test.db')}"
        self.file_csv = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.join("files_test", "sigmat_postgres_test.csv"),
        )
        self.sqllite_manager = SqliteManager()
        self.sqllite_manager.create_tables()
        self.sqllite_manager.clean_all_table()

        app = flask_app
        self.client = app.test_client()

    def test_get_list_all_intervention(self):
        """
        Intervention recovery test
        """
        # Create intervention for edit with request put

        add_intervention_1 = Intervention(
            label='TEST LABEL',
            description='Description',
            author='Eddy',
            location='Le Mans',
            date_intervention=datetime(2021, 10, 10, 10, 0, 0),
        )

        self.sqllite_manager.session.add(add_intervention_1)
        self.sqllite_manager.session.commit()

        # Create intervention for edit with request put

        add_intervention_2 = Intervention(
            label='TEST LABEL 2',
            description='Description',
            author='Bob',
            location='Nantes',
            date_intervention=datetime(2020, 5, 5, 10, 0, 0),
        )

        self.sqllite_manager.session.add(add_intervention_2)
        self.sqllite_manager.session.commit()
        response = self.client.get('/interventions')

        result_list = [
            {
                'label': 'TEST LABEL',
                'description': "Description",
                'author': 'Eddy',
                'location': 'Le Mans',
                # 'date_intervention': '22/09/2021',
            },
            {
                'label': 'TEST LABEL 2',
                'description': "Description",
                'author': 'Bob',
                'location': 'Nantes',
                # 'date_intervention': '22/09/2021',
            }
        ]

        # Testing status code & interventions informations
        self.assertEqual(response.status_code, 200)

        for intervention in response.json:
            self.assertIn(intervention['label'], ['TEST LABEL', 'TEST LABEL 2'])
            self.assertIn(intervention['author'], ['Eddy', 'Bob'])
            self.assertIn(intervention['location'], ['Le Mans', 'Nantes'])
            self.assertEqual(intervention['description'], "Description")

    def test_add_intervention(self):
        """
        Test of the addition of a new intervention
        """

        response = self.client.post(
            '/intervention/add',
            json={
                'label': 'TEST LABEL',
                'description': "Création d'une nouvelle intervention",
                'author': 'Eddy',
                'location': 'Le Mans',
                'date_intervention': '22/09/2021 13:00:00',
            },

        )

        self.assertEqual(response.status_code, 201)

        check_insert = self.sqllite_manager.session.query(Intervention).filter_by(label='TEST LABEL').first()
        self.assertEqual(check_insert.label, 'TEST LABEL')
        self.assertEqual(check_insert.description, "Création d'une nouvelle intervention")
        self.assertEqual(check_insert.author, "Eddy")
        self.assertEqual(check_insert.location, 'Le Mans')
        self.assertEqual(check_insert.date_intervention, datetime.strptime("22/09/2021 13:00:00", '%d/%m/%Y %H:%M:%S'))

    def test_add_intervention_with_error_data_post(self):
        """
        Test of the addition of a new intervention with error data post
        """

        response = self.client.post(
            '/intervention/add',
            json={
                'label': 'TEST LABEL',
                'author': 'Eddy',
                'description': "Création d'une nouvelle intervention"
            },

        )

        self.assertEqual(response.status_code, 404)

    def test_edit_intervention_success(self):
        """
        Test edit intervention
        """

        # Create intervention for edit with request put

        add_intervention = Intervention(
            label='TEST LABEL',
            description='Description',
            author='Eddy',
            location='Le Mans',
            date_intervention=datetime(2021, 10, 10, 10, 0, 0),
        )

        self.sqllite_manager.session.add(add_intervention)
        self.sqllite_manager.session.commit()

        # get id intervention

        intervention_object = self.sqllite_manager.session.query(Intervention).filter_by(label='TEST LABEL').first()
        self.sqllite_manager.session.close()
        response = self.client.put(
            f'/intervention/{intervention_object.intervention_id}',
            json={
                'label': 'TEST LABEL',
                'description': 'Description',
                'author': 'Eddy',
                'location': 'Nantes',
                'date_intervention': '22/09/2021 13:00:00',
            },

        )

        self.assertEqual(response.status_code, 200)

        intervention_object = self.sqllite_manager.session.query(Intervention).filter_by(label='TEST LABEL').first()
        self.assertEqual(intervention_object.location, 'Nantes')

    def test_delete_intervention_success(self):
        """
        Test delete intervention
        """

        # Create intervention for edit with request put

        add_intervention = Intervention(
            label='TEST LABEL',
            description='Description',
            author='Eddy',
            location='Le Mans',
            date_intervention=datetime(2021, 10, 10, 10, 0, 0),
        )

        self.sqllite_manager.session.add(add_intervention)
        self.sqllite_manager.session.commit()

        # get id intervention

        intervention_object = self.sqllite_manager.session.query(Intervention).filter_by(label='TEST LABEL').first()
        self.sqllite_manager.session.close()
        response = self.client.delete(
            f'/intervention/{intervention_object.intervention_id}',
        )

        self.assertEqual(response.status_code, 200)

        intervention_object = self.sqllite_manager.session.query(Intervention).filter_by(label='TEST LABEL').all()
        self.assertEqual(len(intervention_object), 0)

    def test_delete_intervention_with_error(self):
        """
        Test delete intervention with error intervention_id
        """

        # Create intervention for edit with request put

        add_intervention = Intervention(
            label='TEST LABEL',
            description='Description',
            author='Eddy',
            location='Le Mans',
            date_intervention=datetime(2021, 10, 10, 10, 0, 0),
        )

        self.sqllite_manager.session.add(add_intervention)
        self.sqllite_manager.session.commit()

        # get id intervention

        intervention_object = self.sqllite_manager.session.query(Intervention).filter_by(label='TEST LABEL').first()
        self.sqllite_manager.session.close()
        response = self.client.delete(
            f'/intervention/{intervention_object.intervention_id +1}',
        )

        self.assertEqual(response.status_code, 404)

        intervention_object = self.sqllite_manager.session.query(Intervention).filter_by(label='TEST LABEL').all()
        self.assertEqual(len(intervention_object), 1)