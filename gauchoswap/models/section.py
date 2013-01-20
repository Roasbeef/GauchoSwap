from gauchoswap import db


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Date)
    time = db.Column(db.DateTime)
    ta = db.Column(db.String)
    location = db.Column(db.String)
    max_spots = db.Column(db.Integer)
    space = db.Column(db.Integer)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))

    def __init__(self, day, time, ta, location, max_spots, space,
                 lecture_id):
        self.day = day
        self.time = time
        self.ta = ta
        self.location = location
        self.max_spots = max_spots
        self.space = space
        self.lecture_id = lecture_id

    def __repr__(self):
        return '<Section %r>' % self.day
