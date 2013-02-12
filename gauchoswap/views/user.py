from flask import redirect, url_for, session, request, Blueprint, render_template

#from gauchoswamp import db

mod = Blueprint('user', __name__, url_prefix='/user')

@mod.route('/')
def show_user_profile():
        user = 'Roman Kazarin' 
	return redirect(url_for('frontend.user_profile', username=user))




