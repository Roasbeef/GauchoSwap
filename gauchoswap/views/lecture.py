from flask import Blueprint, abort, jsonify
from gauchoswap import db, api
from gauchoswap.models import Lab


mod = Blueprint('lecture', __name__, url_prefix='/lecture')


@mod.route('/', methods=['GET'])
def get_all_lectures():

    try:
        lectures = api.get_all_lectures()
    except api.DbLectureError:
        abort(404)

    return jsonify(lectures)


@mod.route('/<int:lecture_id>/sections', methods=['GET'])
def get_sections_for_lecture(lecture_id):

    try:
        sections = api.get_sections_for_lecture(lecture_id)
    except api.DbLectureError:
        abort(404)

    return jsonify(sections)


@mod.route('/<department>/', methods=['GET'])
def get_lecture_by_department(department):

    try:
        lectures = api.get_lecture_by_department(department)
    except api.DbLectureError:
        abort(404)

    return jsonify(lectures)


@mod.route('/<int:lecture_id>', methods=['GET'])
def get_lecture_by_id(lecture_id):

    try:
        lecture = api.get_lecture_by_id(lecture_id)
    except api.DbLectureError:
        abort(404)

    return jsonify(lecture)
