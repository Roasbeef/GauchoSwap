from flask import Blueprint
from gauchoswap.helpers import request_wants_json
mod = Blueprint('lab', __name__, url_prefix='/lab')

def get_all_labs():
    try:
        labs = api.get_all_labs()
    except api.DbNotFoundError:
        abort(404)
        
    return jsonify(labs)

@mod.route('/<department>/', methods=['GET'])
def get_lab_by_department(department):
    wants_json = request_wants_json();
    try:
        labs = api.get_lab_by_department(department, json=wants_json)
    except api.DbNotFoundError:
        abort(404)

    return jsonify(labs)

@mod.route('/<int:lab_id>/', methonds=['GET'])
def get_lab_by_id(lab_id):
     wants_json = request_wants_json();
    try:
        lab = api.get_lab_by_id(lab_id, json=wants_json)
    except api.DbNotFoundError:
        abort(404)

    return jsonify(lab)
