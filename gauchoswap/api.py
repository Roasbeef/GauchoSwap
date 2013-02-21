from gauchoswap import db

from gauchoswap.models import Lab, Lecture, Section, Offer, Swapblock


def get_or_404(f):
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        if result is None:
            raise DbNotFoundError('Model requested does not exist')
        else:
            return result
    return wrapper


class DbLectureError(Exception):
    pass


@get_or_404
def get_all_lectures(json=False):
    all_lectures = Lecture.query.all()
    return (lecture.to_json() for lecture in all_lectures) if json else (lecture for lecture in all_lectures)

@get_or_404
def get_all_labs(json=False):
    all_labs = Lab.query.all()
    return (lab.to_json() for lab in all_labs) if json else (lab for lab in all_labs)

@get_or_404
def get_lab_by_department(department, json=''):
    labs = Lab.query.filter_by(department = department).all()
    return (lab.to_json() for lab in labs) if json else (lab for lab in labs)

@get_or_404
def get_lab_by_id(lab_id, json=''):
    lab = Lab.query.filter_by(lab_id = lab_id)
    return lab.to-json() if json else lab


    
