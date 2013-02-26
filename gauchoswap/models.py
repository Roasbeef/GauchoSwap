from gauchoswap import db
import datetime


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

    def to_json(self):
        return {'name': self.name, 'title': self.title, 'department': self.department,
                'location': self.location, 'days': self.days, 'time': self.time,
                'max_spots': self.max_spots, 'space': self.space}


class Lecture(Class, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor = db.Column(db.String)
    sections = db.relationship('Section', backref='lecture', lazy='dynamic')

    def __init__(self, professor, *args, **kwargs):
        self.professor = professor
        Class.__init__(self, *args, **kwargs)

    def to_json(self):
        base_class_json = super(Class, self).to_json()
        base_class_json.extend({'professor': self.professor})


class Section(Class, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ta = db.Column(db.String)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))

    def __init__(self, ta, lecture, *args, **kwargs):
        self.ta = ta
        self.lecture = lecture
        Class.__init__(self, *args, **kwargs)

    def to_json(self):
        base_class_json = super(Class, self).to_json()
        base_class_json.extend({'ta': self.ta}, {'lecture': self.lecture.title})


class Lab(Class, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instructor = db.Column(db.String)

    def __init__(self, instructor, *args, **kwargs):
        self.instructor = instructor
        Class.__init__(self, *args, **kwargs)

    def to_json(self):
        base_class_json = super(Class, self).to_json()
        base_class_json.extend({'instructor': self.instructor})


requested_offers = db.Table('requested_offers',
                            db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                            db.Column('offer_id', db.Integer, db.ForeignKey('offer.id'))
                            )

recieved_offers = db.Table('recieved_offers',
                           db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                           db.Column('offer_id', db.Integer, db.ForeignKey('offer.id'))
                           )


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum('accepted', 'pending', 'declined', name='status'))

    created_at = db.Column(db.Date, default=datetime.datetime.now)

    offerer_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    offeree_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    offer_type = db.Column(db.Enum('section', 'lab', 'lecture', name='offer_type'))
    offerer_class_id = db.Column(db.String)
    offeree_class_id = db.Column(db.String)

    def __init__(self, offerer_id, offeree_id, offer_type, offerer_class_id, offeree_class_id):
        self.offerer_id = offerer_id
        self.offeree_id = offeree_id
        self.offer_type = offer_type
        self.offerer_class_id = offerer_class_id
        self.offeree_class_id = offeree_class_id
        self.status = 'pending'

    def describe(self):
        class_map = {'section': Section, 'lab': Lab, 'lecture': Lecture}

        offerer_class = class_map[self.offer_type].query.filter_by(id=self.offerer_class_id).first()
        offeree_class = class_map[self.offer_type].query.filter_by(id=self.offeree_class_id).first()

        return '%s wants to swap %s for %s with %s' % (self.offerer.name, offerer_class.title,
                                                       offeree_class.title, self.offeree.name)

    def to_json(self):
        class_map = {'section': Section, 'lab': Lab, 'lecture': Lecture}

        offerer_class = class_map[self.offer_type].query.filter_by(id=self.offerer_class_id).first()
        offeree_class = class_map[self.offer_type].query.filter_by(id=self.offeree_class_id).first()

        return {'offerer': self.offerer.name, 'offeree': self.offeree.name, 'type': self.offer_type,
                'offerer class': offerer_class.name, 'offeree class': offeree_class.name,
                'offer status': self.status}


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date, default=datetime.datetime.now)
    name = db.Column(db.String)
    umail_address = db.Column(db.String)
    facebook_id = db.Column(db.String)
    fb_auth_token = db.Column(db.String)
    fb_profile_link = db.Column(db.String)
    fb_picture_link = db.Column(db.String)
    swapblock = db.relationship('Swapblock', backref=db.backref('student', uselist=False), lazy='dynamic')
    requested_offers = db.relationship('Offer', secondary=requested_offers,
                                       primaryjoin="Offer.offerer_id==Student.id",
                                       backref=db.backref('offerer', uselist=False))
    recieved_offers = db.relationship('Offer', secondary=recieved_offers,
                                      primaryjoin="Offer.offeree_id==Student.id",
                                      backref=db.backref('offeree', uselist=False))

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

    def to_json(self):
        return {'name': self.name}


owned_sections = db.Table('owned_sections',
                          db.Column('swapblock_id', db.Integer, db.ForeignKey('swapblock.id')),
                          db.Column('section_id', db.Integer, db.ForeignKey('section.id'))
                          )

owned_lectures = db.Table('owned_lectures',
                          db.Column('swapblock_id', db.Integer, db.ForeignKey('swapblock.id')),
                          db.Column('lecture_id', db.Integer, db.ForeignKey('lecture.id'))
                          )

owned_labs = db.Table('owned_labs',
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

wanted_labs = db.Table('wanted_labs',
                       db.Column('swapblock_id', db.Integer, db.ForeignKey('swapblock.id')),
                       db.Column('lab_id', db.Integer, db.ForeignKey('lab.id'))
                       )


class Swapblock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
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

    def to_json(self):
        return {'student': self.student.name,
                'owned_sections': [section.to_json() for section in self.owned_sections],
                'owned_labs': [lab.to_json() for lab in self.owned_labs],
                'owned_lectures': [lecture.to_json() for lecture in self.owned_lectures],
                'wanted_sections': [section.to_json() for section in self.wanted_sections],
                'wanted_labs': [lab.to_json() for lab in self.wanted_labs],
                'wanted_lectures': [lecture.to_json() for lecture in self.wanted_lectures],
                }
