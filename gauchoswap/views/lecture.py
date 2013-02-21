from flask import Blueprint, abort, jsonify
from gauchoswap import db, api
from gauchoswap.models import Lab
from gauchoswap.helpers import request_wants_json


mod = Blueprint('lecture', __name__, url_prefix='/lecture')


@mod.route('/', methods=['GET'])
def get_all_lectures():
    wants_json = request_wants_json()
    try:
        lectures = api.get_all_lectures(json=wants_json)
    except api.DbNotFoundError:
        abort(404)

    return jsonify(lectures)


@mod.route('/<int:lecture_id>/sections', methods=['GET'])
def get_sections_for_lecture(lecture_id):
    wants_json = request_wants_json()
    try:
        sections = api.get_sections_for_lecture(lecture_id, json=wants_json)
    except api.DbNotFoundError:
        abort(404)

    return jsonify(sections)


@mod.route('/<department>/', methods=['GET'])
def get_lecture_by_department(department):
    wants_json = request_wants_json()
    try:
        lectures = api.get_lecture_by_department(department, json=wants_json)
    except api.DbNotFoundError:
        abort(404)

    return jsonify(lectures)


@mod.route('/<int:lecture_id>', methods=['GET'])
def get_lecture_by_id(lecture_id):
    wants_json = request_wants_json()
    try:
        lecture = api.get_lecture_by_id(lecture_id, json=wants_json)
    except api.DbNotFoundError:
        abort(404)

    return jsonify(lecture)
