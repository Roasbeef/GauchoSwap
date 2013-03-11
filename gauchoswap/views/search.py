from flask import Blueprint, abort, jsonify, request, render_template, Response
from gauchoswap import api
from gauchoswap.helpers import request_wants_json
from gauchoswap.models import Student, Lecture, Lab, Section

import json

mod = Blueprint('search', __name__, url_prefix='/search')


@mod.route('/student')
def search_students():
    query = request.args.get('q')

    if query is None:
        all_students = Student.query.all()
        datum_list = [student.name for student in all_students]

        return Response(json.dumps(datum_list), mimetype='application/json')


@mod.route('/section')
def search_sections():
    query = request.args.get('q')
    pass

@mod.route('/lab')
def search_labs():
    query = request.args.get('q')
    pass

@mod.route('/lecture')
def search_lectures():
    query = request.args.get('q')
    pass
