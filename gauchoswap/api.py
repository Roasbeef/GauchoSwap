from gauchoswap import db, cache

from gauchoswap.models import Lab, Lecture, Section, Offer, Swapblock, Student


def get_or_404(f):
    def wrapper(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
        except Exception as e:
            raise DbNotFoundError('Model requested does not exist: %s' % e)
        if result is None:
            raise DbNotFoundError('Model requested does not exist:')
        else:
            return result
    return wrapper


class UserDoesNotHavePermissionError(Exception):
    pass


class DbNotFoundError(Exception):
    pass

CLASS_DICT = {'lecture': Lecture, 'lab': Lab, 'section': Section}


@get_or_404
def get_courses(class_type, pagination=False, page=1, json=False, department=''):
    course_query = CLASS_DICT[class_type].query if not department else CLASS_DICT[class_type].query.filter_by(department=department)
    courses = course_query.paginate(page).items if pagination else course_query.all()

    return [course if not json else course.to_json for course in courses]


@get_or_404
def get_course_by_id(class_type, course_id, json=False):
    course = CLASS_DICT[class_type].query.get(course_id)
    return course


@get_or_404
def get_lecture_sections(lecture_id, json=False):
    sections = Section.query.filter_by(id=lecture_id)
    return [section.to_json if json else section for section in sections]


@get_or_404
def get_all_offers(json=False, page=1):
    all_offers = Offer.query.paginate(page=page, per_page=10).items
    return [offer.to_json if json else offer for offer in all_offers]


@get_or_404
def get_offer_by_id(offer_id, json=False):
    offer = Offer.query.filter_by(offer_id=offer_id).first()
    return offer.to_json() if json else offer


@get_or_404
def get_all_swapblocks(json=False):
    swapblocks = Swapblock.query.all()
    return [swapblock.to_json if json else swapblock for swapblock in swapblocks]


@get_or_404
def get_student_swapblock(student_id, json=False):
    student = Student.query.filter_by(id=student_id).first()
    block = student.swapblock.first()

    return block.to_json() if json else block


def add_class_to_swapblock(**params):
    student_id = params['student_id']
    class_type = params['class_type']
    class_id = params['class_id']
    have_class = params['have_class']

    student = Student.query.filter_by(id=student_id).first()
    course = CLASS_DICT[class_type].query.filter_by(id=class_id).first()

    if have_class and class_type == 'lecture':
        student.swapblock.first().owned_lectures.append(course)
    elif have_class and class_type == 'lab':
        student.swapblock.first().owned_labs.append(course)
    elif have_class and class_type == 'section':
        student.swapblock.first().owned_sections.append(course)

    if not have_class and class_type == 'lecture':
        student.swapblock.first().wanted_lectures.append(course)
    elif not have_class and class_type == 'lab':
        student.swapblock.first().wanted_labs.append(course)
    elif not have_class and class_type == 'section':
        student.swapblock.first().wanted_sections.append(course)


def delete_class_from_swapblock(**params):
    student_id = params['student_id']
    class_type = params['class_type']
    class_id = params['class_id']
    have_class = params['have_class']

    student = Student.query.filter_by(id=student_id).first()
    course = CLASS_DICT[class_type].query.filter_by(id=class_id).first()

    if have_class and class_type == 'lecture':
        student.swapblock.first().owned_lectures.remove(course)
    elif have_class and class_type == 'lab':
        student.swapblock.first().owned_labs.remove(course)
    elif have_class and class_type == 'section':
        student.swapblock.first().owned_sections.remove(course)

    if not have_class and class_type == 'lecture':
        student.swapblock.first().wanted_lectures.remove(course)
    elif not have_class and class_type == 'lab':
        student.swapblock.first().wanted_labs.remove(course)
    elif not have_class and class_type == 'section':
        student.swapblock.first().wanted_sections.remove(course)


def create_offer(**params):
    offerer_id = params['offerer_id']
    offeree_id = params['offeree_id']
    offer_type = params['offer_type']
    offerer_class_id = params['offerer_class_id']
    offeree_class_id = params['offeree_class_id']

    student1 = Student.query.filter_by(id=offerer_id).first()
    student2 = Student.query.filter_by(id=offeree_id).first()

    offer = Offer(offerer_id=offerer_id, offeree_id=offeree_id, offer_type=offer_type,
                  offerer_class_id=offerer_class_id, offeree_class_id=offeree_class_id)

    student1.requested_offers.append(offer)
    student2.recieved_offers.append(offer)

    db.session.add(offer)
    db.session.commit()


def accept_offer(student_id, offer_id):
    offer = Offer.query.filter_by(id=offer_id).first()

    if student_id != offer.offeree_id:
        raise UserDoesNotHavePermissionError("You don't own that offer")

    offer.status = 'accepted'

    db.session.commit()


def reject_offer(student_id, offer_id):
    offer = Offer.query.filter_by(id=offer_id).first()

    if student_id != offer.offeree_id:
        raise UserDoesNotHavePermissionError("You don't own that offer")

    offer.status = 'rejected'

    db.session.commit()
