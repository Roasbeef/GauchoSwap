from flask import redirect, url_for, session, request, Blueprint, render_template

#from gauchoswap import db
from gauchoswap.models import Lecture

mod = Blueprint('frontend', __name__)


@mod.route('/')
def index():
    return render_template('index.html')

@mod.route('/SwapBlock/<username>/')
def swap_block(username):
    lectures = Lecture.query.all()
    departments = []
    for lecture in lectures:
        if lecture.department not in departments:
            departments.append(lecture.department)
 
    return render_template('swapblock.html', departments=departments)
