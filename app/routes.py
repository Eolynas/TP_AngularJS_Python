""" this module takes care of the flask routes """
from datetime import datetime

from flask import render_template, jsonify, make_response
from flask import request

from app import app
from app.models.intervention import Intervention
from app.tools import logger
from app.tools.sqllite_manager import SqliteManager
from app.tools.tools import todict


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    """
    Load home page with list intervention
    """

    return render_template('index.html')


@app.route("/interventions", methods=["GET"])
def list_interventions():
    """
    Load home page with list intervention
    """
    sqlite_manager = SqliteManager()
    if request.method == 'GET':
        get_interventions = sqlite_manager.session.query(Intervention).all()
        dict_interventions = todict(get_interventions)

        # Format date
        # for date in dict_interventions:
        #     date['date_intervention']= date['date_intervention'].strftime("%d/%m/%Y %H:%M:%S")

        return make_response(jsonify(dict_interventions), 200)


@app.route("/intervention/add", methods=["POST"])
def add_intervention():
    """
    Load home page
    """
    sqlite_manager = SqliteManager()
    if request.method == 'POST':
        result = request.json
        # Check data resquest post
        # if 'label' in result and 'description' in result and 'author' in result and 'location' in result and 'date_intervention' in result:
        if 'label' in result:
            if result.get('date_intervention'):
                result['date_intervention'] = datetime.strptime(result['date_intervention'], '%d/%m/%Y %H:%M:%S')
            intervention = {
                'label': result.get('label'),
                'description': result.get('description'),
                'author': result.get('author'),
                'location': result.get('location'),
                'date_intervention': result.get('date_intervention')
            }
            res_insert = sqlite_manager.add_intervention(intervention=intervention)
            message = "L'intervetion à bien été enregistré"
            return make_response(jsonify(message), 201)

        message = "Certaines informations sont manquante"
        return make_response(jsonify(message), 404)


@app.route("/intervention/<int:intervention>", methods=["PUT", "DELETE"])
def edit_intervention(intervention):
    """
    Load home page
    """
    sqlite_manager = SqliteManager()
    if request.method == 'PUT':

        print(intervention)
        result = request.json
        # Check if intervention exist
        get_intervention = sqlite_manager.session.query(Intervention).filter_by(intervention_id=intervention)

        if get_intervention.first():

            # Check diff
            dict_update = {}

            try:
                for key, value in todict(get_intervention.first()).items():
                    print(key)
                    if key != 'intervention_id':
                        if value != result[key]:
                            dict_update[key] = result[key]

                if dict_update.get('date_intervention'):
                    dict_update['date_intervention'] = datetime.strptime(dict_update['date_intervention'],
                                                                         '%d/%m/%Y %H:%M:%S')
                get_intervention.update(dict_update)
                sqlite_manager.session.commit()
                sqlite_manager.session.close()

                message = f"L'intervention à bien était modifié"
                logger.info(message)
                return make_response(message, 200)

            except KeyError as e:
                message = f"Une erreur est survenue lors de la modification de l'intervention: {e}"
                logger.error(message)
                return make_response(message, 404)

        message = f"Une erreur est survenue lors de la modification de l'intervention"
        logger.error(message)
        return make_response(message, 404)

    if request.method == 'DELETE':
        get_intervention = sqlite_manager.session.query(Intervention).filter_by(intervention_id=intervention)

        if get_intervention.first():
            sqlite_manager.session.delete(get_intervention.first())
            sqlite_manager.session.commit()
            sqlite_manager.session.close()

            message = f"L'intervention à bien était supprimé"
            logger.info(message)
            return make_response(message, 200)

        message = f"Une erreur est survenue lors de la suppression de l'intervention"
        logger.error(message)
        return make_response(message, 404)
