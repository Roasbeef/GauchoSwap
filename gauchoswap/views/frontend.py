from flask import redirect, url_for, session, request, Blueprint, render_template

#from gauchoswap import db


mod = Blueprint('frontend', __name__)




@mod.route('/')
def index():
    return render_template('index.html')
