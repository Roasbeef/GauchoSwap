from flask import redirect, url_for, session, request, Blueprint, render_template

from gauchoswap import api

from gauchoswap.models import Offer

mod = Blueprint('frontend', __name__)


@mod.route('/')
def index():
    offers = Offer.query.all()
    return render_template('index.html', offers=offers)

@mod.route('/SwapBlock/<username>/')
def swap_block(username):
    return render_template('swapblock.html', username=username)


@mod.route('/user/<username>')
def user_profile(username):
    return render_template('user.html')
