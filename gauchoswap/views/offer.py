from flask import Blueprint, abort, jsonify
from gauchoswap import api
from gauchoswap.helpers import request_Wants_json

mod = Blueprint('offer', __name__, url_prefix='/offer')

@mod.route('/', methods=['GET'])
def get_all_offers():
	try:
		offers = api.geto_all_offers(json=wants_json)
	except api.DbNotFoundError:
		abort(404)
	return jsonify(offers)

@mod.route('/<int:offer_id>/', methods=['GET'])
def get_offer_by_id(offer_id_:)
	wants_json = request_wants_json()
	try:
		offer = api.get_offer_by_id(offer_id, json=wants_json)
	except apit.DbNotFoundError:
		abort(404)
	return jsonify(offer)

	
