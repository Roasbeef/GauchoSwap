from flask import session, request, Blueprint, g, jsonify, abort, current_app
from gauchoswap import db, api
from gauchoswap.helpers import request_wants_json
from gauchoswap.decorators import login_required

import json

mod = Blueprint('swapblock', __name__, url_prefix='/swapblock')


@mod.route('/', methods=['GET'])
def all_swapblocks():
    wants_json = request_wants_json()

    try:
        blocks = api.get_all_swapblocks(json=wants_json)
    except api.DbNotFoundError:
        abort(404, message='There are no swablocks')

    return jsonify({'swapblocks': blocks})


@mod.route('/<int:student_id>', methods=['GET'])
def student_swapblock(student_id):
    wants_json = request_wants_json()

    try:
        swapblock = api.get_student_swapblock(student_id, json=wants_json)
    except api.DbNotFoundError:
        abort(404)

    return jsonify({'swapblock': swapblock})


@mod.route('/add', methods=['POST'])
@login_required
def add_to_swapblock():
    params = json.loads(request.form['params'])

    try:
        api.add_class_to_swapblock(**params)
    except api.DbNotFoundError:
        abort(404)

    resp = jsonify(message='success!')
    resp.status_code = 201
    return resp


@mod.route('/drop', methods=['POST'])
def delete_from_swapblock():
    params = json.loads(request.form['params'])

    try:
        api.delete_class_from_swapblock(**params)
    except api.DbNotFoundError:
        abort(404)

    resp = jsonify(message='success!')
    resp.status_code = 201
    return resp


def get_macro_with_context(template_name, macro_name):
    template = current_app.jinja_env.get_template(template_name)
    module = template.make_module({'session': session, 'g': g})
    macro = getattr(module, macro_name)
    return macro
