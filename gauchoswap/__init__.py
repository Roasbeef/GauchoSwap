import os

from flask import Flask, render_template, g, session
from flask.ext.sqlalchemy import SQLAlchemy

from views import frontend


app = Flask('gauchospace')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.debug = os.environ.get('DEBUG')

db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

app.register_blueprint(frontend.mod)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
