from flask import (redirect, url_for, session, request, Blueprint, render_template,
                   flash, g)
from gauchoswap import db, course_abrev
from gauchoswap.models import Student

mod = Blueprint('student', __name__, url_prefix='/student')


@mod.route('/<int:student_id>')
def user_profile(student_id):
    student = Student.query.filter_by(id=student_id).first_or_404()
    swapblock = student.swapblock.first()

    owned_classes = []
    wanted_classes = []

    owned_classes.extend(("Lecture", lecture) for lecture in swapblock.owned_lectures)
    owned_classes.extend(("Section", section) for section in swapblock.owned_sections)
    owned_classes.extend(("Lab", lab) for lab in swapblock.owned_labs)

    wanted_classes.extend(("Lecture", lecture) for lecture in swapblock.wanted_lectures)
    wanted_classes.extend(("Section", lecture) for section in swapblock.wanted_sections)
    wanted_classes.extend(("Lab", lecture) for section in swapblock.wanted_labs)

    departments = [(abrv, department) for abrv, department in course_abrev.course_abrv_to_department.iteritems()]
    departments.sort()

    return render_template('student.html', student=student, departments=departments,
                           owned_classes=owned_classes, wanted_classes=wanted_classes)
