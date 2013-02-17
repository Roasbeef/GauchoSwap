from gauchoswap import db


class Class(object):
    """ Base db model to be inherited """
    name = db.Column(db.String)
    title = db.Column(db.String)
    department = db.Column(db.String)
    location = db.Column(db.String)
    days = db.Column(db.String)
    time = db.Column(db.String)
    max_spots = db.Column(db.String)
    space = db.Column(db.String)

    def __init__(self, name, title, department, location, days, time, max_spots, space):
        self.name = name
        self.title = title
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
        Class.__init__(self, *args, **kwargs)


class Section(Class, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ta = db.Column(db.String)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))

    def __init__(self, ta, lecture, *args, **kwargs):
        self.ta = ta
        self.lecture = lecture
        Class.__init__(self, *args, **kwargs)


class Lab(Class, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instructor = db.Column(db.String)

    def __init__(self, instructor, *args, **kwargs):
        self.instructor = instructor
        Class.__init__(self, *args, **kwargs)


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum('accepted', 'pending', 'declined'))
    offerer = db.relationship('Student')
    offeree = db.relationship('Student')
    offer_type = db.Column(db.Enum('section', 'lab', 'lecture', 'free for all', name='offer_type'))
    offerer_class = db.relationship()
    offeree_class = db.relationship()  # use HSTORE here?


owned_sections = db.Table('owned_sections',
                          db.Column('swapblock_id', db.Integer, db.ForeignKey('swapblock.id')),
                          db.Column('section_id', db.Integer, db.ForeignKey('section.id'))
                          )

owned_lectures = db.Table('owned_lectures',
                          db.Column('swapblock_id', db.Integer, db.ForeignKey('swapblock.id')),
                          db.Column('lecture_id', db.Integer, db.ForeignKey('lecture.id'))
                          )

owned_labs = db.Table('owned_sections',
                      db.Column('swapblock_id', db.Integer, db.ForeignKey('swapblock.id')),
                      db.Column('lab_id', db.Integer, db.ForeignKey('lab.id'))
                      )

wanted_sections = db.Table('wanted_sections',
                           db.Column('swapblock_id', db.Integer, db.ForeignKey('swapblock.id')),
                           db.Column('section_id', db.Integer, db.ForeignKey('section.id'))
                           )

wanted_lectures = db.Table('wanted_lectures',
                           db.Column('swapblock_id', db.Integer, db.ForeignKey('swapblock.id')),
                           db.Column('lecture_id', db.Integer, db.ForeignKey('lecture.id'))
                           )

wanted_labs = db.Table('wanted_sections',
                       db.Column('swapblock_id', db.Integer, db.ForeignKey('swapblock.id')),
                       db.Column('lab_id', db.Integer, db.ForeignKey('lab.id'))
                       )


class SwapBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owned_sections = db.relationship('Section', secondary=owned_sections,
                                     backref=db.backref('students_who_have', lazy='dynamic'))

    owned_labs = db.relationship('Lab', secondary=owned_labs,
                                 backref=db.backref('students_who_have', lazy='dynamic'))

    owned_lectures = db.relationship('Lecture', secondary=owned_lectures,
                                     backref=db.backref('students_who_have', lazy='dynamic'))

    wanted_sections = db.relationship('Section', secondary=wanted_sections,
                                      backref=db.backref('students_who_want', lazy='dynamic'))

    wanted_labs = db.relationship('Lab', secondary=wanted_labs,
                                  backref=db.backref('students_who_want', lazy='dynamic'))

    wanted_lectures = db.relationship('Lecture', secondary=wanted_lectures,
                                      backref=db.backref('students_who_want', lazy='dynamic'))

    def __init__(self, student):
        self.student = student

    def __repr__(self):
        return "<%s's SwapBlock>" % self.student.name


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    umail_address = db.Column(db.String)
    facebook_id = db.Column(db.String)
    fb_auth_token = db.Column(db.String)
    fb_profile_link = db.Column(db.String)
    fb_picture_link = db.Column(db.String)
    swapblock_id = db.Column(db.Integer, db.ForeignKey('swapblock.id'))
    swapblock = db.relationship('SwapBlock', backref=db.backref('student', uselist=False))

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
