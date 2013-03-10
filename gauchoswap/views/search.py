from flask import Blueprint, abort, jsonify, request, render_template
from gauchoswap import api
from gauchoswap.helpers import request_wants_json

mod = Blueprint('search', __name__, url_prefix='/search')
