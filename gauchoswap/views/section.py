from flask import Blueprint, abort, jsonify, request, render_template
from gauchoswap import api
from gauchoswap.helpers import request_wants_json
mod = Blueprint('section', __name__, url_prefix='/section')


@mod.route('/<int:section_id>/', methods=['GET'])
def get_section_by_id(section_id):
    wants_json = request_wants_json()

    try:
        section = api.get_course_by_id('section', section_id, json=wants_json)
    except api.DbNotFoundError:
        abort(404)

    return jsonify({'section': section}) if wants_json else render_template('course_page.html', course=section)


@mod.route('/<department>/', methods=['GET'])
def get_sections_by_department(department):
    page_number = request.args.get('page')
    wants_json = request_wants_json()

    try:
        sections = api.get_courses('section', pagination=page_number is not None, page=page_number,
                                   json=wants_json, department=department)
    except api.DbNotFoundError:
        abort(404)

    return jsonify({'sections': sections})


@mod.route('/', methods=['GET'])
def get_all_sections():
    page_number = request.args.get('page')
    wants_json = request_wants_json()

    try:
        sections = api.get_courses('section', pagination=page_number is not None, page=page_number,
                                   json=wants_json)
    except api.DbNotFoundError:
        abort(404)

    return jsonify({'sections': sections})
