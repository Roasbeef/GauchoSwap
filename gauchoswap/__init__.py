import os

from flask import Flask, render_template, session, g
from flask_oauth import OAuth
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

from gauchoswap.helpers import request_wants_json


SECRET_KEY = '2432fkdsajflads9'
DEBUG = True
FACEBOOK_APP_ID = '542774122412862'
FACEBOOK_APP_SECRET = '8125ade96b956dc61982de537d7a6389'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
app.debug = True
app.secret_key = SECRET_KEY

db = SQLAlchemy(app)
cache = Cache()
cache.init_app(app, config={'CACHE_TYPE': 'simple'})
oauth = OAuth()

from gauchoswap.models import Student


@app.errorhandler(404)
def not_found(error):
    return 'Ooops', 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return 'My bad', 500


@app.before_request
def load_user():
    if session.get('fb_id') is not None:
        user = Student.query.filter_by(facebook_id=session.get('fb_id')).first()
        g.user = user

from gauchoswap.views import (frontend, account, swapblock, user, lecture, section,
                              lab, offer)

app.register_blueprint(frontend.mod)
app.register_blueprint(account.mod)
app.register_blueprint(swapblock.mod)
app.register_blueprint(user.mod)
app.register_blueprint(lecture.mod)
app.register_blueprint(lab.mod)
app.register_blueprint(section.mod)
app.register_blueprint(offer.mod)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
