from flask import (redirect, url_for, session, request, Blueprint, render_template,
                   flash, g)
from gauchoswap import db, oauth, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from gauchoswap.models import Student, Lecture

mod = Blueprint('swapblock', __name__, url_prefix='/SwapBlock')

@mod.route('/')
def get():
    user = Student.query.filter_by(facebook_id=session['fb_id']).first()
    username = user.name
    lectures = Lecture.query.filter_by(id=1).first()
    #departments = []
    #for lecture in lectures:
        #for department in lecture.department:
            #if department not in departments:
	        #departments.append(department)
    departments = "hello" 
    return redirect(url_for('frontend.swap_block', username=username, departments=departments)) 
