from gauchoswap import db


class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    department = db.Column(db.String)
    days = db.Column(db.Date)
    time = db.Column(db.DateTime)
    professor = db.Column(db.String)
    location = db.Column(db.String)
    max_spots = db.Column(db.Integer)
    space = db.Column(db.Integer)
    sections = db.relationship('Section', backref='lecture', lazy='dynamic')

    def __init__(self, name, department, days, time, professor, location,
                 max_spots, space, sections):
        self.name = name
        self.department = department
        self.days = days
        self.time = time
        self.professor = professor
        self.location = location
        self.max_spots = max_spots
        self.space = space
        self.sections = sections

    def __repr__(self):
        return '<Lecture %r>' % self.name
