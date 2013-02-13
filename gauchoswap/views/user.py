from flask import (redirect, url_for, session, request, Blueprint, render_template,
                   flash, g)
from gauchoswap import db, oauth, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, app
from gauchoswap.models import Student, Lecture

mod = Blueprint('swapblock', __name__, url_prefix='/<username>')

@mod.route('/')
def show_user_profile():
    user = Student.query.filter_by(facebook_id=session['fb_id']).first()
    un = user.name
    prof_link = user.fb_profile_link;
    prof_pic = user.fb_picture_link;
    return redirect(url_for('frontend.user_profile', username=un))
