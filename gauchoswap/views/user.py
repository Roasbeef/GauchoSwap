from flask import (redirect, url_for, session, request, Blueprint, render_template,
                   flash, g)
from gauchoswap import db, oauth, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, app, course_abrev
from gauchoswap.models import Student, Lecture

mod = Blueprint('user', __name__, url_prefix='/user')

@mod.route('/')
def show_user_profile():
    user = Student.query.filter_by(facebook_id=session['fb_id']).first()
    un = user.name
    prof_link = user.fb_profile_link
    prof_pic = user.fb_picture_link
    departments = [(abrv, department) for abrv, department in course_abrev.course_abrv_to_department.iteritems()]
    departments.sort()
    return render_template('user.html', username=un, departments=departments)

@mod.route('/SwapBlock')
def show_block():
    departments = [(abrv, department) for abrv, department in course_abrev.course_abrv_to_department.iteritems()]
    departments.sort()
    return render_template('swapblock.html', departments=departments)
