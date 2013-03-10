from gauchoswap.models import Lab, Swapblock, Section, Offer, Lecture, Student
from gauchoswap import api, db
from flask.ext.testing import TestCase

import gauchoswap
import unittest
import string
import random


class GauchoSwapApiTestCase(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        app = gauchoswap.app
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_test_lectures(self):
        ''' used for general counts/exists tests '''
        random_string = lambda x: ''.join(random.choice(string.lowercase) for i in range(9))
        random_test_lectures = [Lecture(*random_string('')) for i in range(10)]

        db.session.add_all(random_test_lectures)
        db.session.commit()

    def test_get_all_lectures(self):
        #empty db should be nothing
        lectures = api.get_courses('lecture')
        self.assertFalse(list(lectures))

        #now there should be 10 classes
        self.create_test_lectures()
        lectures = api.get_courses('lecture')
        self.assertEqual(len(list(lectures)), 10)

    def create_test_sections(self):
        """ Create sections to be used for tests """
        sectionAdd = []

        for i in range(5):
            num = str(i + 1)
            sectionAdd.append(Section(ta=num, lecture=None, name=num, title=num, department=num,
                                      location=num, days=num, time=num, max_spots=num, space=num))
        db.session.add_all(sectionAdd)
        db.session.commit()

    def test_get_all_sections(self):
        # Empty db should have nothing
        sections = api.get_courses('section')
        self.assertFalse(list(sections))

        # Create 5 sections where every attribute is the same as the ID
        self.create_test_sections()

        # 5 Sections should have been made, get_all_sections() should get them all
        sections = api.get_courses('section')
        self.assertEqual(len(list(sections)), 5)

    def test_get_section_by_id(self):
        # empty db should have nothing
        sections = api.get_courses('section')
        self.assertFalse(list(sections))

        # Create 5 sections where every attribute is the same as the ID
        self.create_test_sections()

        # Try to get all Sections based on ID
        # Check will be made by comparing Section name to Section ID, which in this test are the same
        for i in range(5):
            section = api.get_course_by_id('section', i + 1)
            self.assertEqual(section.name, str(i + 1))

    def test_get_section_by_department(self):
        # empty db should have nothing
        sections = api.get_courses('section')
        self.assertFalse(list(sections))

        # Create 5 sections where every attribute is the same as the ID
        self.create_test_sections()

        # Create 5 more sections
        # Sections will be made in a way that each of the 10 sections will share a department with another section
        sectionAdd = []
        for i in range(5):
            num = str(i + 6)
            departmentNum = str(i + 1)
            sectionAdd.append(Section(ta=num, lecture=None, name=num, title=num, department=departmentNum,
                                      location=num, days=num, time=num, max_spots=num, space=num))
        db.session.add_all(sectionAdd)
        db.session.commit()

        # Try to get all Sections based on department
        # Check will be made by making sure there are 2 sections in a department, and by checking the name of the department
        # to make sure they match expected values
        for i in range(5):
            sections = api.get_courses('section', department=str(i + 1))
            sectionList = list(sections)
            # Make sure there are 2 sections in department
            self.assertEqual(len(sectionList), 2)
            # Make sure the 2 sections are the one expected
            self.assertEqual(sectionList[0].name, str(i + 1))
            self.assertEqual(sectionList[1].name, str(i + 6))

    def test_student_swapblock(self):
        #initial setup
        student = Student(name='test', umail_address='test', facebook_id='test', fb_auth_token='test',
                          fb_profile_link='test', fb_picture_link='test')
        swap_block = Swapblock(student)

        db.session.add(student)
        db.session.add(swap_block)
        db.session.commit()

        test_block = api.get_student_swapblock(student.id)

        self.assertEqual(test_block.student.name, swap_block.student.name)

        self.assertRaises(api.DbNotFoundError, api.get_student_swapblock, 10000)

    def test_add_and_delete_wanted_section(self):
        student = Student(name='test', umail_address='test', facebook_id='test', fb_auth_token='test',
                          fb_profile_link='test', fb_picture_link='test')
        section2 = Section(ta='test', lecture=None, name='test', title='test', department='test',
                           location='test', days='test', time='test', max_spots='test', space='test')
        section1 = Section(ta='test', lecture=None, name='test', title='test', department='test',
                           location='test', days='test', time='test', max_spots='test', space='test')
        swapblock = Swapblock(student)

        db.session.add(student)
        db.session.add(section2)
        db.session.add(section1)
        db.session.add(swapblock)
        db.session.commit()

        params = {}
        params['student_id'] = student.id
        params['class_type'] = 'section'
        params['class_id'] = section1.id
        params['have_class'] = False

        api.add_class_to_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().wanted_sections), 1)

        params['class_id'] = section2.id

        api.add_class_to_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().wanted_sections), 2)

        api.delete_class_from_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().wanted_sections), 1)

    def test_add_and_wanted_lecture(self):
        student = Student(name='test', umail_address='test', facebook_id='test', fb_auth_token='test',
                          fb_profile_link='test', fb_picture_link='test')
        lecture2 = Lecture(professor='test', name='test', title='test', department='test',
                           location='test', days='test', time='test', max_spots='test', space='test')
        lecture1 = Lecture(professor='test', name='test', title='test', department='test',
                           location='test', days='test', time='test', max_spots='test', space='test')
        swapblock = Swapblock(student)

        db.session.add(student)
        db.session.add(lecture2)
        db.session.add(lecture1)
        db.session.add(swapblock)
        db.session.commit()

        params = {}
        params['student_id'] = student.id
        params['class_type'] = 'lecture'
        params['class_id'] = lecture1.id
        params['have_class'] = False

        api.add_class_to_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().wanted_lectures), 1)

        params['class_id'] = lecture2.id

        api.add_class_to_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().wanted_lectures), 2)

        api.delete_class_from_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().wanted_lectures), 1)

    def test_add_wanted_lab(self):
        student = Student(name='test', umail_address='test', facebook_id='test', fb_auth_token='test',
                          fb_profile_link='test', fb_picture_link='test')
        lab2 = Lab(instructor='test', name='test', title='test', department='test',
                   location='test', days='test', time='test', max_spots='test', space='test')
        lab1 = Lab(instructor='test', name='test', title='test', department='test',
                   location='test', days='test', time='test', max_spots='test', space='test')
        swapblock = Swapblock(student)

        db.session.add(student)
        db.session.add(lab2)
        db.session.add(lab1)
        db.session.add(swapblock)
        db.session.commit()

        params = {}
        params['student_id'] = student.id
        params['class_type'] = 'lab'
        params['class_id'] = lab2.id
        params['have_class'] = False

        api.add_class_to_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().wanted_labs), 1)

        params['class_id'] = lab1.id

        api.add_class_to_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().wanted_labs), 2)

        api.delete_class_from_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().wanted_labs), 1)

    def test_add_and_delete_owned_section(self):
        student = Student(name='test', umail_address='test', facebook_id='test', fb_auth_token='test',
                          fb_profile_link='test', fb_picture_link='test')
        section2 = Section(ta='test', lecture=None, name='test', title='test', department='test',
                           location='test', days='test', time='test', max_spots='test', space='test')
        section1 = Section(ta='test', lecture=None, name='test', title='test', department='test',
                           location='test', days='test', time='test', max_spots='test', space='test')
        swapblock = Swapblock(student)

        db.session.add(student)
        db.session.add(section2)
        db.session.add(section1)
        db.session.add(swapblock)
        db.session.commit()

        params = {}
        params['student_id'] = student.id
        params['class_type'] = 'section'
        params['class_id'] = section1.id
        params['have_class'] = True

        api.add_class_to_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().owned_sections), 1)

        params['class_id'] = section2.id

        api.add_class_to_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().owned_sections), 2)

        api.delete_class_from_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().owned_sections), 1)

    def test_add_and_delete_owned_lecture(self):
        student = Student(name='test', umail_address='test', facebook_id='test', fb_auth_token='test',
                          fb_profile_link='test', fb_picture_link='test')
        lecture2 = Lecture(professor='test', name='test', title='test', department='test',
                           location='test', days='test', time='test', max_spots='test', space='test')
        lecture1 = Lecture(professor='test', name='test', title='test', department='test',
                           location='test', days='test', time='test', max_spots='test', space='test')
        swapblock = Swapblock(student)

        db.session.add(student)
        db.session.add(lecture2)
        db.session.add(lecture1)
        db.session.add(swapblock)
        db.session.commit()

        params = {}
        params['student_id'] = student.id
        params['class_type'] = 'lecture'
        params['class_id'] = lecture1.id
        params['have_class'] = True

        api.add_class_to_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().owned_lectures), 1)

        params['class_id'] = lecture2.id

        api.add_class_to_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().owned_lectures), 2)

        api.delete_class_from_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().owned_lectures), 1)

    def test_add_owned_lab(self):
        student = Student(name='test', umail_address='test', facebook_id='test', fb_auth_token='test',
                          fb_profile_link='test', fb_picture_link='test')
        lab2 = Lab(instructor='test', name='test', title='test', department='test',
                   location='test', days='test', time='test', max_spots='test', space='test')
        lab1 = Lab(instructor='test', name='test', title='test', department='test',
                   location='test', days='test', time='test', max_spots='test', space='test')
        swapblock = Swapblock(student)

        db.session.add(student)
        db.session.add(lab2)
        db.session.add(lab1)
        db.session.add(swapblock)
        db.session.commit()

        params = {}
        params['student_id'] = student.id
        params['class_type'] = 'lab'
        params['class_id'] = lab2.id
        params['have_class'] = True

        api.add_class_to_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().owned_labs), 1)

        params['class_id'] = lab1.id

        api.add_class_to_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().owned_labs), 2)

        api.delete_class_from_swapblock(**params)

        self.assertEqual(len(student.swapblock.first().owned_labs), 1)

    def test_create_offer(self):
        student1 = Student(name='test', umail_address='test', facebook_id='test', fb_auth_token='test',
                           fb_profile_link='test', fb_picture_link='test')
        student2 = Student(name='test', umail_address='test', facebook_id='test', fb_auth_token='test',
                           fb_profile_link='test', fb_picture_link='test')
        lab1 = Lab(instructor='test', name='test', title='test', department='test',
                   location='test', days='test', time='test', max_spots='test', space='test')
        lab2 = Lab(instructor='test', name='test', title='test', department='test',
                   location='test', days='test', time='test', max_spots='test', space='test')

        db.session.add(student1)
        db.session.add(student2)
        db.session.add(lab1)
        db.session.add(lab2)
        db.session.commit()

        params = {}
        params['offerer_id'] = student1.id
        params['offeree_id'] = student2.id
        params['offer_type'] = 'lab'
        params['offerer_class_id'] = lab1.id
        params['offeree_class_id'] = lab2.id

        api.create_offer(**params)

        self.assertEqual(student1.requested_offers[0].offeree_id, student2.id)
        self.assertEqual(student2.recieved_offers[0].offerer_id, student1.id)

    def test_accept_offer(self):
        student1 = Student(name='test', umail_address='test', facebook_id='test', fb_auth_token='test',
                           fb_profile_link='test', fb_picture_link='test')
        student2 = Student(name='test', umail_address='test', facebook_id='test', fb_auth_token='test',
                           fb_profile_link='test', fb_picture_link='test')
        lab1 = Lab(instructor='test', name='test', title='test', department='test',
                   location='test', days='test', time='test', max_spots='test', space='test')
        lab2 = Lab(instructor='test', name='test', title='test', department='test',
                   location='test', days='test', time='test', max_spots='test', space='test')

        db.session.add(student1)
        db.session.add(student2)
        db.session.add(lab1)
        db.session.add(lab2)
        db.session.commit()

        params = {}
        params['offerer_id'] = student1.id
        params['offeree_id'] = student2.id
        params['offer_type'] = 'lab'
        params['offerer_class_id'] = lab1.id
        params['offeree_class_id'] = lab2.id

        api.create_offer(**params)

        offer_id = student1.requested_offers[0].id

        api.accept_offer(student2.id, offer_id)

        self.assertEqual(student1.requested_offers[0].status, 'accepted')

    '''
    def test_reject_offer(self):
        student1 = Student(name='test', umail_address='test', facebook_id='test', fb_auth_token='test',
                           fb_profile_link='test', fb_picture_link='test')
        student2 = Student(name='test', umail_address='test', facebook_id='test', fb_auth_token='test',
                           fb_profile_link='test', fb_picture_link='test')
        lab1 = Lab(instructor='test', name='test', title='test', department='test',
                   location='test', days='test', time='test', max_spots='test', space='test')
        lab2 = Lab(instructor='test', name='test', title='test', department='test',
                   location='test', days='test', time='test', max_spots='test', space='test')

        db.session.add(student1)
        db.session.add(student2)
        db.session.add(lab1)
        db.session.add(lab2)
        db.session.commit()

        params = {}
        params['offerer_id'] = student1.id
        params['offeree_id'] = student2.id
        params['offer_type'] = 'lab'
        params['offerer_class_id'] = lab1.id
        params['offeree_class_id'] = lab2.id

        api.create_offer(**params)

        offer_id = student1.requested_offers[0].id

        api.reject_offer(student2.id, offer_id)

        self.assertEqual(student1.requested_offers[0].status, 'declined')
    '''

if __name__ == '__main__':
    unittest.main()
