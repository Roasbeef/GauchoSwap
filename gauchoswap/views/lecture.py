from flask import Blueprint, abort, jsonify, request, render_template
from gauchoswap import db, api
from gauchoswap.helpers import request_wants_json


mod = Blueprint('lecture', __name__, url_prefix='/lecture')


@mod.route('/', methods=['GET'])
def get_all_lectures():
    page_number = request.args.get('page')
    wants_json = request_wants_json()

    try:
        lectures = api.get_courses(class_type='lecture', pagination=page_number is not None,
                                   page=page_number, json=wants_json)
    except api.DbNotFoundError:
        abort(404)

    return jsonify({'lectures': lectures}) if wants_json else render_template('lecture.html', lectures=lectures)


@mod.route('/<int:lecture_id>/sections', methods=['GET'])
def get_sections_for_lecture(lecture_id):
    wants_json = request_wants_json()

    try:
        sections = api.get_sections_for_lecture(lecture_id, json=wants_json)
    except api.DbNotFoundError:
        abort(404)

    return jsonify({'section': sections}) if wants_json else render_template('section.html', sections=sections)


@mod.route('/<department>/', methods=['GET'])
def get_lecture_by_department(department):
    page_number = request.args.get('page')
    wants_json = request_wants_json()

    try:
        lectures = api.get_courses(class_type='lecture', pagination=page_number is not None,
                                   page=page_number, json=wants_json, department=department)
    except api.DbNotFoundError:
        abort(404)

    return jsonify({'lectures': lectures})


@mod.route('/<int:lecture_id>', methods=['GET'])
def get_lecture_by_id(lecture_id):
    wants_json = request_wants_json()

    try:
        lecture = api.get_course_by_id('lecture', lecture_id, json=wants_json)
    except api.DbNotFoundError:
        abort(404)

    return jsonify({'lecture': lecture}) if wants_json else render_template('course_page.html', course=lecture)
