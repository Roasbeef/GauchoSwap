from flask import Blueprint, abort, jsonify
from gauchoswap import api
from gauchoswap.helpers import request_wants_json
mod = Blueprint('section', __name__, url_prefix='/section')


@mod.route('/<int:section_id>/', methods=['GET'])
def get_section_by_id(section_id):
    wants_json = request_wants_json()
    try:
        section = api.get_section_by_id(section_id, json=wants_json)
    except api.DbNotFoundError:
        abort(404)
    return jsonify(section)

@mod.route('/<department>/', methods=['GET'])
def get_section_by_department(department):
    wants_json = request_wants_json()
    try:
        sections = api.get_section_by_department(department, json=wants_json)
    except api.DbNotFoundError:
        abort(404)
    return jsonify(sections)


@mod.route('/', methods=['GET'])
def get_all_sections():
    wants_json = request_wants_json()
    try:
        sections = api.get_all_sections(json=wants_json)
    except api.DbNotFoundError:
        abort(404)
    return jsonify(sections)
