from flask import redirect, url_for, session, request, Blueprint, render_template, g

from gauchoswap import api, cache, course_abrev

from gauchoswap.models import Offer

mod = Blueprint('frontend', __name__)


@mod.route('/')
def index():
    page = int(request.args.get('page', 1))
    offers = api.get_all_offers(page=page)
    return render_template('index.html', offers=offers, page=page)
