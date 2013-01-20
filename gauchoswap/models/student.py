from gauchoswap import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120), unique=True)
    major = db.Column(db.String(120), unique=True)
    umail_address = db.Column(db.String(120), unique=True)
    #classes = db.relationship('Class', backref='student', lazy='dynamic')

    def __init__(self, year, name, major, umail_address):
        self.year = year
        self.name =name
        self.major = major
        self.umail_address = umail_address

    def __repr__(self):
        return '<Student %r>' % self.name
