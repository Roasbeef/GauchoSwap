from flask import redirect, url_for, session, request, Blueprint, render_template

from gauchoswap import api

from gauchoswap.models import Offer

mod = Blueprint('frontend', __name__)


@mod.route('/')
def index():
    offers = api.get_all_offers()
    return render_template('index.html', offers=offers)
