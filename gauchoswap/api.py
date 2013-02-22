from gauchoswap import db

from gauchoswap.models import Lab, Lecture, Section, Offer, Swapblock, Student


def get_or_404(f):
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        if result is None:
            raise DbNotFoundError('Model requested does not exist')
        else:
            return result
    return wrapper


class UserDoesNotHavePermissionError(Exception):
    pass


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
def get_sections_by_department(department, json=False):
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
    lectures = Lecture.query.filter_by(department=department).first()
    return db_collection_to_json(lectures) if json else (lecture for lecture in lectures)


@get_or_404
def get_all_labs(json=False):
    all_labs = Lab.query.all()
    return db_collection_to_json(all_labs) if json else (lab for lab in all_labs)


@get_or_404
def get_lab_by_department(department, json=False):
    labs = Lab.query.filter_by(department=department).all()
    return (lab.to_json() for lab in labs) if json else (lab for lab in labs)


@get_or_404
def get_lab_by_id(lab_id, json=False):
    lab = Lab.query.filter_by(lab_id=lab_id).first()
    return lab.to_json() if json else lab


@get_or_404
def get_all_offers(json=False):
    all_offers = Offer.query.all()
    return db_collection_to_json(all_offers) if json else (offer for offer in all_offers)


@get_or_404
def get_offer_by_id(offer_id, json=False):
    offer = Offer.query.filter_by(offer_id=offer_id).first()
    return offer.to_json() if json else offer


@get_or_404
def get_all_swapblocks(json=False):
    swapblocks = Swapblock.query.all()
    return db_collection_to_json(swapblocks) if json else (sb for sb in swapblocks)


@get_or_404
def get_student_swapblock(student_id, json=False):
    student = Student.query.filter_by(id=student_id).first()
    block = student.swapblock

    return block.to_json() if json else block


def add_class_to_swapblock(**params):
    class_dict = {'lecture': Lecture, 'lab': Lab, 'section': Section}
    student_id = params['student_id']
    class_type = params['class_type']
    class_id = params['class_id']
    have_class = params['have_class']

    student = Student.query.filter_by(id=student_id)
    course = class_dict[class_type].query.filter_by(id=class_id)

    if have_class and class_type == 'lecture':
        student.swapblock.owned_lectures.append(course)
    elif have_class and class_type == 'lab':
        student.swapblock.owned_labs.append(course)
    elif have_class and class_type == 'section':
        student.swapblock.owned_sections.append(course)

    if not have_class and class_type == 'lecture':
        student.swapblock.wanted_lectures.append(course)
    elif not have_class and class_type == 'lab':
        student.swapblock.wanted_labs.append(course)
    elif not have_class and class_type == 'section':
        student.swapblock.wanted_sections.append(course)


def delete_class_from_swapblock(**params):
    class_dict = {'lecture': Lecture, 'lab': Lab, 'section': Section}
    student_id = params['student_id']
    class_type = params['class_type']
    class_id = params['class_id']
    have_class = params['have_class']

    student = Student.query.filter_by(id=student_id).first()
    course = class_dict[class_type].query.filter_by(id=class_id).first()

    if have_class and class_type == 'lecture':
        student.swapblock.owned_lectures.remove(course)
    elif have_class and class_type == 'lab':
        student.swapblock.owned_labs.remove(course)
    elif have_class and class_type == 'section':
        student.swapblock.owned_sections.remove(course)

    if not have_class and class_type == 'lecture':
        student.swapblock.wanted_lectures.remove(course)
    elif not have_class and class_type == 'lab':
        student.swapblock.wanted_labs.remove(course)
    elif not have_class and class_type == 'section':
        student.swapblock.wanted_sections.remove(course)


def create_offer(**params):
    offerer_id = params['offerer_id']
    offeree_id = params['offeree_id']
    offer_type = params['offer_type']
    offerer_class_id = params['offerer_class_id']
    offeree_class_id = params['offeree_class_id']

    offer = Offer(offerer_id=offerer_id, offeree_id=offeree_id, offer_type=offer_type,
                  offerer_class_id=offerer_class_id, offeree_class_id=offeree_class_id)

    db.session.add(offer)
    db.session.commit()


@get_or_404
def accept_offer(student_id, offer_id):
    offer = Offer.query.filter_by(id=offer_id).first()

    if student_id != offer.offeree_id:
        raise UserDoesNotHavePermissionError("You don't own that offer")

    offer.status = 'accepted'

    db.session.commit()


@get_or_404
def reject_offer(student_id, offer_id):
    offer = Offer.query.filter_by(id=offer_id).first()

    if student_id != offer.offeree_id:
        raise UserDoesNotHavePermissionError("You don't own that offer")

    offer.status = 'rejected'

    db.session.commit()
