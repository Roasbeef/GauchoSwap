from flask.ext.script import Manager, Command
from gauchoswap import app, db
from gauchoswap.models import Class, Lecture, Section, Student, Lab

manager = Manager(app)


@manager.command
def db_create():
    """ Creates the database """
    db.create_all()
    print 'table created!'


@manager.command
def db_drop_all():
    """ Drops errtang """
    db.drop_all()

if __name__ == '__main__':
    manager.run()
