from flask import (redirect, url_for, session, request, Blueprint, render_template,
                   flash, g)
from gauchoswap import db, course_abrev
from gauchoswap.models import Student

mod = Blueprint('student', __name__, url_prefix='/student')


@mod.route('/<int:student_id>')
def user_profile(student_id):
    student = Student.query.filter_by(id=student_id).first_or_404()

    departments = [(abrv, department) for abrv, department in course_abrev.course_abrv_to_department.iteritems()]
    departments.sort()

    return render_template('student.html', student=student, departments=departments)
