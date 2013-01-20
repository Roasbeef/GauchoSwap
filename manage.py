from flask.ext.script import Manager, Command
from gauchoswap import app, db
from gauchoswap.models.lecture import Lecture
from gauchoswap.models.section import Section
from gauchoswap.models.student import Student

manager = Manager(app)


@manager.command
def db_create():
    """ Creates the database """
    db.create_all()


@manager.command
def db_drop_all():
    """ Drops errtang """
    db.drop_all()

if __name__ == '__main__':
    manager.run()
