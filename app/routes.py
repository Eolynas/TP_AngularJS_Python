""" this module takes care of the flask routes """
from datetime import datetime

from flask import render_template, jsonify, make_response
from flask import request

from app import app
from app.models.intervention import Intervention
from app.tools import logger
from app.tools.sqllite_manager import SqliteManager
from app.tools.tools import todict, get_status


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
        sqlite_manager.session.close()

        dict_interventions = todict(get_interventions)
        list_interventions = []
        for intervention in dict_interventions:
            intervention = get_status(intervention)
            list_interventions.append(intervention)

        return make_response(jsonify(dict_interventions), 200)


@app.route("/interventions", methods=["POST"])
def add_intervention():
    """
    route for add intervention
    """
    sqlite_manager = SqliteManager()
    result = request.json
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

        add_intervention = Intervention(
            label=intervention['label'],
            description=intervention['description'],
            author=intervention['author'],
            location=intervention['location'],
            date_intervention=intervention['date_intervention'],
        )
        sqlite_manager.session.add(add_intervention)
        sqlite_manager.session.commit()
        new_intervention = add_intervention.intervention_id
        sqlite_manager.session.close()

        if new_intervention:
            new_intervention = sqlite_manager.session.query(Intervention).filter_by(intervention_id=new_intervention).first()
            sqlite_manager.session.close()

            # Check status:
            intervention = get_status(todict(new_intervention))

            return make_response(jsonify(intervention), 201)

        # TODO: status code 400 car je suppose que c'est le client qui fait une erreur en envoyant la meme chose
        message = "L'intervention existe deja"
        return make_response(jsonify(message), 400)

    message = "Le libellé de l'intervention est manquant"
    return make_response(jsonify(message), 404)


@app.route("/interventions/<int:intervention>", methods=["PUT"])
def edit_intervention(intervention):
    """
    Load home page
    """
    sqlite_manager = SqliteManager()

    result = request.json
    # Check if intervention exist
    get_intervention = sqlite_manager.session.query(Intervention).filter_by(intervention_id=intervention)

    if get_intervention.first():

        # Check diff
        dict_update = {}

        try:
            for key, value in todict(get_intervention.first()).items():
                if key != 'intervention_id':
                    if value != result[key]:
                        dict_update[key] = result[key]

            if dict_update.get('date_intervention'):
                dict_update['date_intervention'] = datetime.strptime(dict_update['date_intervention'],
                                                                     '%d/%m/%Y %H:%M:%S')
            get_intervention.update(dict_update)
            sqlite_manager.session.commit()
            sqlite_manager.session.close()

            message = f"L'intervention à bien été modifié"
            logger.info(message)
            interventions = get_status(todict(sqlite_manager.session.query(Intervention).filter_by(intervention_id=intervention).first()))
            sqlite_manager.session.close()

            return make_response(jsonify(interventions), 200)

        except KeyError as e:
            message = f"Une erreur est survenue lors de la modification de l'intervention: {e}"
            logger.error(message)
            return make_response(message, 404)

    message = f"Une erreur est survenue lors de la modification de l'intervention"
    logger.error(message)
    return make_response(message, 404)


@app.route("/interventions/<int:intervention>", methods=["DELETE"])
def delete_intervention(intervention):
    """
    Route for delete intervention
    """

    sqlite_manager = SqliteManager()
    get_intervention = sqlite_manager.session.query(Intervention).filter_by(intervention_id=intervention)

    if get_intervention.first():
        sqlite_manager.session.delete(get_intervention.first())
        sqlite_manager.session.commit()
        sqlite_manager.session.close()

        message = f"L'intervention à bien était supprimé"
        logger.info(message)
        return make_response(message, 204)

    message = f"Une erreur est survenue lors de la suppression de l'intervention"
    logger.error(message)
    return make_response(message, 404)
