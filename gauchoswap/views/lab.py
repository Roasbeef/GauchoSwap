from flask import Blueprint, abort, jsonify, request, render_template
from gauchoswap.helpers import request_wants_json
from gauchoswap import api

mod = Blueprint('lab', __name__, url_prefix='/lab')


@mod.route('/', methods=['GET'])
def get_all_labs():
    wants_json = request_wants_json
    page_number = request.args.get('page')
    try:
        labs = api.get_courses('lab', pagination=page_number is not None, page=page_number,
                               json=wants_json)
    except api.DbNotFoundError:
        abort(404)

    return jsonify({'labs': labs})


@mod.route('/<department>/', methods=['GET'])
def get_lab_by_department(department):
    wants_json = request_wants_json()
    page_number = request.args.get('page')
    try:
        labs = api.get_courses('lab', pagination=page_number is not None, page=page_number,
                               json=wants_json, department=department)
    except api.DbNotFoundError:
        abort(404)

    return jsonify({'labs': labs})


@mod.route('/<int:lab_id>/', methods=['GET'])
def get_lab_by_id(lab_id):
    wants_json = request_wants_json()
    try:
        lab = api.get_course_by_id('lab', lab_id, json=wants_json)
    except api.DbNotFoundError:
        abort(404)

    return jsonify({'lab': lab}) if wants_json else render_template('couse_page.html', course=lab)
