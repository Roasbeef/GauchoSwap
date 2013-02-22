from flask import (redirect, url_for, session, request, Blueprint, render_template,
                   flash, g, jsonify, abort)
from gauchoswap import db, api

from gauchoswap.helpers import request_wants_json
from gauchoswap.decorators import login_required

mod = Blueprint('swapblock', __name__, url_prefix='/Swapblock')


@mod.route('/', methods=['GET'])
def all_swapblocks():
    wants_json = request_wants_json()
    blocks = api.get_all_swapblocks(json=wants_json)
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
    params = request.form
    params['student_id'] = g.user.id

    try:
        api.add_class_to_swapblock(**params)
    except api.DbNotFoundError:
        abort(404)

    resp = jsonify(message='success!')
    resp.status_code = 201
    return resp


@mod.route('/drop', methods=['DELETE'])
def delete_from_swapblock():
    params = request.form
    params['student_id'] = g.user.id

    try:
        api.delete_class_from_swapblock(**params)
    except api.DbNotFoundError:
        abort(404)

    resp = jsonify(message='success!')
    resp.status_code = 201
    return resp
