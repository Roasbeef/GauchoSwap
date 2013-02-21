from gauchoswap import db

from gauchoswap.models import Lab, Lecture, Section, Offer, Swapblock


def get_or_404(f):
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        if result is None:
            raise DbLectureError('Model requested does not exist')
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
