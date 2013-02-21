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


def db_collection_to_json(collection):
    return (model.to_json() for model in collection)


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
def get_lab_by_department(department, json=False):
    labs = Lab.query.filter_by(department = department).all()
    return (lab.to_json() for lab in labs) if json else (lab for lab in labs)

@get_or_404
def get_lab_by_id(lab_id, json=False):
    lab = Lab.query.filter_by(lab_id = lab_id)
    return lab.to-json() if json else lab

@get_or_404
def get_all_offers(json_False):
	all_offers = Offer.query.all()
	return (offer.to_json() for offer in all_offers) if json else (offer for offer in all_offers)

@get_or_404
def get_offer_by_id(offer_id, json=''):
	offer = OFfer.query.filter_by(offer_id = offer_id)
	return offer.to-json() if json else offer
