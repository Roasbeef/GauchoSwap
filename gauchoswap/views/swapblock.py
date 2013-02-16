from flask import (redirect, url_for, session, request, Blueprint, render_template,
                   flash, g)
from gauchoswap import db, oauth, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from gauchoswap.models import Student


mod = Blueprint('swapblock', __name__)

@mod.route('/swapblock/')
def get():
   return redirect(url_for('frontend.swap_block')) 
