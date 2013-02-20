from flask import (redirect, url_for, session, request, Blueprint, render_template,
                   flash, g, jsonify)
from gauchoswap import db, oauth, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, app
from gauchoswap.models import Student, Lecture
from gauchoswap.course_abrev import course_abrv_to_department
import os

mod = Blueprint('swapblock', __name__, url_prefix='/SwapBlock')

@mod.route('/')
def get():
    user = Student.query.filter_by(facebook_id=session['fb_id']).first()
    username = user.name   
    return redirect(url_for('frontend.swap_block', username=username))

@mod.route('/add')
def getClasses(department=None,):
    department = request.args.get('department')
    lectures = Lecture.query.filter_by(department=department).all()
    lectureNames = []
    for name in lectures:
        lectureNames.append(name.name)

    lectureLen = len(lectureNames)
    return jsonify(response=lectureNames, length=lectureLen)

@app.context_processor
def department_processor():
    departments = []
    def getClasses(department):
        lecture = Lecture.query.filter_by(department=department).all()
        return lecture
    for abrv, department in course_abrv_to_department.iteritems():
	temp = (abrv, department)
        departments.append(temp)
    departments.sort() 
    return dict(departments=departments, getClasses=getClasses)


     
