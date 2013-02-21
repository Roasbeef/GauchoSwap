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


def db_collection_to_json(collection):
    return (model.to_json() for model in collection)


@get_or_404
def get_all_lectures(json=False):
    all_lectures = Lecture.query.all()
    return db_collection_to_json(all_lectures) if json else (lecture for lecture in all_lectures)

@get_or_404
def get_lecture_sections(lecture_id, json=False):
    sections_for_lecture = Section.query.filter_by(id=lecture_id)
    return db_collection_to_json(sections_for_lecture) if json else (section for section in sections_for_lecture)

@get_or_404
def get_department_lectures(department, json=False):
    lectures = Lecture.query.filter_by(department=department)
    return db_collection_to_json(lectures) if json else (lecture for lecture in lectures)

@get_or_404
def get_all_labs(json=False):
    all_labs = Lab.query.all()
    return db_collection_to_json(all_labs) if json else (lab for lab in all_labs)

@get_or_404
def get_lab_by_department(department, json=''):
    labs = Lab.query.filter_by(department = department).all()
    return (lab.to_json() for lab in labs) if json else (lab for lab in labs)

@get_or_404
def get_lab_by_id(lab_id, json=''):
    lab = Lab.query.filter_by(lab_id = lab_id)
    return lab.to-json() if json else lab
