import os

from flask import Flask, render_template
from flask_oauth import OAuth
from flask.ext.sqlalchemy import SQLAlchemy


SECRET_KEY = '2432fkdsajflads9'
DEBUG = True
FACEBOOK_APP_ID = '542774122412862'
FACEBOOK_APP_SECRET = '8125ade96b956dc61982de537d7a6389'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.debug = True
app.secret_key = SECRET_KEY

db = SQLAlchemy(app)
oauth = OAuth()


'''
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
'''
from gauchoswap.views import frontend, account

app.register_blueprint(frontend.mod)
app.register_blueprint(account.mod)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
