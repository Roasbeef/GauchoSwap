from flask import (redirect, url_for, session, request, Blueprint, render_template,
                   flash, g, abort, jsonify)
from gauchoswap import db, api
from gauchoswap.helpers import request_wants_json

from gauchoswap.decorators import login_required
from gauchoswap.models import Student, Offer
import json

mod = Blueprint('offer', __name__, url_prefix='/offer')


@mod.route('/', methods=['GET', 'POST'])
@login_required
def add_or_get_offers():
    wants_json = request_wants_json()
    params = json.loads(request.form['params'])
    try:
        if request.method == 'GET':
            offers = api.get_all_offers(json=wants_json)
            return jsonify({'offer': offers})
        elif request.method == 'POST':
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


@mod.route('/accept', methods=['PUT'])
@login_required
def accept_offer():
    offer_id = request.form['offer_id']
    try:
        api.accept_offer(g.user.id, offer_id)
        resp = jsonify(message='success!')
        resp.status_code = 201
        return resp
    except api.UserDoesNotHavePermissionError:
        resp = jsonify(message='You did not recieve that offer')
        resp.status_code = 401
        return resp


@mod.route('/reject', methods=['PUT'])
@login_required
def reject_offer():
    offer_id = request.form['offer_id']
    try:
        api.reject_offer(g.user.id, offer_id)
        resp = jsonify(message='success!')
        resp.status_code = 201
        return resp
    except api.UserDoesNotHavePermissionError:
        resp = jsonify(message='You did not recieve that offer')
        resp.status_code = 401
        return resp


@mod.route('/student_offers/<int:student_id>/')
def user_offers(student_id):
    if g.user.id != student_id:
        abort(403)
    student = db.session.query(Student).filter_by(id=student_id).first()
    requested_offers = db.session.query(Offer).filter_by(offerer_id=student_id).all()
    received_offers = db.session.query(Offer).filter_by(offeree_id=student_id).all()
    #requested_offers = [offer for offer in student.requested_offers]
    #received_offers = [offer for offer in student.recieved_offers]
    return render_template('offer.html', student=student, requested_offers=requested_offers, received_offers=received_offers)
