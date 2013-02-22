from flask import Blueprint, abort, jsonify, g, request
from gauchoswap import api
from gauchoswap.helpers import request_wants_json

from decorators import login_required

mod = Blueprint('offer', __name__, url_prefix='/offer')


@mod.route('/', methods=['GET', 'POST'])
@login_required
def add_or_get_offers():
    wants_json = request_wants_json()
    try:
        if request.method == 'GET':
            offers = api.get_all_offers(json=wants_json)
            return jsonify({'offer': offers})
        elif request.method == 'POST':
            params = request.form
            params['student_id'] = g.user.id
            api.create_offer(**params)
            resp = jsonify(message='success!')
            resp.status_code = 201
            return resp
    except api.DbNotFoundError:
        abort(404)


@mod.route('/<int:offer_id>/', methods=['GET'])
@login_required
def get_offer_by_id(offer_id):
    wants_json = request_wants_json()
    try:
        offer = api.get_offer_by_id(offer_id, json=wants_json)
        return jsonify({'offer': offer})
    except api.DbNotFoundError:
        abort(404)
