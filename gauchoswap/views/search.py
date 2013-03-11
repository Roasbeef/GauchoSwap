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
        datum_list = [dict(name=student.name, id=student.id) for student in all_students]

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
    matched_lectures = []
    matched_lectures.extend(lecture.to_json() for lecture in Lecture.query.filter(Lecture.department.op('ilike')('%{}%'.format(query))).all())
    matched_lectures.extend(lecture.to_json() for lecture in Lecture.query.filter(Lecture.name.op('ilike')('%{}%'.format(query))).all())
    matched_lectures.extend(lecture.to_json() for lecture in Lecture.query.filter(Lecture.title.op('ilike')('%{}%'.format(query))).all())

    return Response(json.dumps(matched_lectures), mimetype='application/json')
