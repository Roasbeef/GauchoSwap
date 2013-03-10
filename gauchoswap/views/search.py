from flask import Blueprint, abort, jsonify, request, render_template
from gauchoswap import api
from gauchoswap.helpers import request_wants_json

mod = Blueprint('search', __name__, url_prefix='/search')

@mod.route('/student')
def search_students():
    query = request.args.get('q')
    pass

@mod.route('/section')
def search_sections():
    query = request.args.get('q')
    pass

@mod.route('/lab')
def search_labs():
    query = request.args.get('q')
    pass

@mod.route('/lecture')
def search_lectures():
    query = request.args.get('q')
    pass
