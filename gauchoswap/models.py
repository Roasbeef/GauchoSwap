from gauchoswap import db


class Class(object):
    """ Base db model to be inherited """
    name = db.Column(db.String)
    department = db.Column(db.String)
    days = db.Column(db.Date)
    time = db.Column(db.DateTime)
    max_spots = db.Column(db.Integer)
    space = db.Column(db.Integer)

    def __init__(self, name, department, days, time, max_spots, space):
        self.name = name
        self.department = department
        self.days = days
        self.time = time
        self.max_spots = max_spots
        self.space = space

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.name)


class Lecture(Class, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor = db.Column(db.String)
    sections = db.relationship('Section', backref='lecture', lazy='dynamic')

    def __init__(self, professor, *args, **kwargs):
        self.professor = professor
        Class.__init__(*args, **kwargs)


class Section(Class, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ta = db.Column(db.String)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))

    def __init__(self, ta, lecture, *args, **kwargs):
        self.ta = ta
        self.lecture = lecture
        Class.__init__(*args, **kwargs)


class Lab(Class, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instructor = db.Column(db.String)

    def __init__(self, instructor, *args, **kwargs):
        self.instructor = instructor
        Class.__init__(*args, **kwargs)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String)
    name = db.Column(db.String)
    major = db.Column(db.String)
    umail_address = db.Column(db.String)
    #classes
    #labs
    #section

    def __init__(self, year, name, major, umail_address):
        self.year = year
        self.name = name
        self.major = major
        self.umail_address = umail_address

    def __repr__(self):
        return '<Student %r>' % self.name
