from gauchoswap import db


class Class(object):
    """ Base db model to be inherited """
    name = db.Column(db.String)
    department = db.Column(db.String)
    location = db.Column(db.String)
    days = db.Column(db.String)
    time = db.Column(db.String)
    max_spots = db.Column(db.String)
    space = db.Column(db.String)

    def __init__(self, name, department, location, days, time, max_spots, space):
        self.name = name
        self.department = department
        self.location = location
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
    name = db.Column(db.String)
    umail_address = db.Column(db.String)
    facebook_id = db.Column(db.Integer)
    fb_auth_token = db.Column(db.Integer)
    fb_profile_link = db.Column(db.Integer)
    fb_picture_link = db.Column(db.Integer)

    def __init__(self, name, umail_address, facebook_id, fb_auth_token, fb_profile_link,
                 fb_picture_link):
        self.name = name
        self.umail_address = umail_address
        self.facebook_id = facebook_id
        self.fb_auth_token = fb_auth_token
        self.fb_profile_link = fb_profile_link
        self.fb_picture_link = fb_picture_link

    def __repr__(self):
        return '<Student %r>' % self.name
