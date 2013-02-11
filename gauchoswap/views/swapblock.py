from flask import (redirect, url_for, session, request, Blueprint, render_template,
                   flash, g)
from gauchoswap import db, oauth, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from gauchoswap.models import Student

mod = Blueprint('swapblock', __name__, url_prefix='/swapblock')

@mod.route('/')
def get():
   user = Student.query.filter_by(facebook_id=session['fb_id']).first()
   username = user.name
   return redirect(url_for('frontend.swap_block', username=username)) 
