from flask import redirect, url_for, session, requesst, Blueprint, render_template

#from gauchoswamp import db

mod = Blueprint('user', __name__, url_prefix='user')

@mod.route('/user/<username>')
def show_user_profile(username)
	return render_template('user.html')


