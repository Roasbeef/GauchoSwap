from flask import Blueprint

mod = Blueprint('frontend', __name__)


@mod.route('/')
def hello():
    return 'Hello World!'
