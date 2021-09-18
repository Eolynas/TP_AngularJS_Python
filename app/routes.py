""" this module takes care of the flask routes """
from datetime import datetime
import os

from flask import render_template, jsonify, escape, make_response
from flask import request

from app import app

from app.tools.sqllite_manager import SqliteManager
from datetime import datetime


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    """
    Load home page
    """
    return 'Hello World!'


@app.route("/intervention/add", methods=["POST"])
def add_intervention():
    """
    Load home page
    """
    sqlite_manager = SqliteManager()
    if request.method == 'POST':
        result = request.json
        # Check data resquest post
        if 'label' in result and 'description' in result and 'author' in result and 'location' in result and 'date_intervention' in result:
            result['date_intervention'] = datetime.strptime(result['date_intervention'], '%d/%m/%Y %H:%M:%S')
            res_insert = sqlite_manager.add_intervention(intervention=result)
            message = "L'intervetion à bien été enregistré"
            return make_response(jsonify(message), 201)

        message = "Certaines informations sont manquante"
        return make_response(jsonify(message), 404)
