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


class DbNotFoundError(Exception):
    pass


@get_or_404
def get_all_lectures(json=False):
    all_lectures = Lecture.query.all()
    return (lecture.to_json() for lecture in all_lectures) if json else (lecture for lecture in all_lectures)

@get_or_404
def get_all_sections(json=False):
    all_sections = Section.query.all()
    return (section.to_json() for section in all_sections) if json else (section for section in all_sections)

@get_or_404
def get_section_by_department(department, json=False):
    department_sections = Section.query.filter_by(department=department).all()
    return (section.to_json() for section in department_sections) if json else (section for section in department_sections)

@get_or_404
def get_section_by_id(section_id, json=False):
    id_section = Section.query.filter_by(id=section_id).first()
    return id_section.to_json() if json else id_section
