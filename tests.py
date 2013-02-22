from gauchoswap.models import Lab, Swapblock, Section, Offer, Lecture
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
        lectures = api.get_all_lectures()
        self.assertFalse(list(lectures))

        #now there should be 10 classes
        self.create_test_lectures()
        lectures = api.get_all_lectures()
        self.assertEqual(len(list(lectures)), 10)

    def create_test_sections(self):
        """ Create sections to be used for tests """
        sectionAdd = []

        for i in range(5):
            num = str(i+1)
            sectionAdd.append(Section(ta=num, lecture=None, name=num, title=num, department=num,
                                        location=num, days=num, time=num, max_spots=num, space=num))
        db.session.add_all(sectionAdd)
        db.session.commit()


    def test_get_all_sections(self):
        # Empty db should have nothing
        sections = api.get_all_sections()
        self.assertFalse(list(sections))

        # Create 5 sections where every attribute is the same as the ID
        self.create_test_sections()

        # 5 Sections should have been made, get_all_sections() should get them all
        sections = api.get_all_sections()
        self.assertEqual(len(list(sections)), 5)

    def test_get_section_by_id(self):
        # empty db should have nothing
        sections = api.get_all_sections()
        self.assertFalse(list(sections))

        # Create 5 sections where every attribute is the same as the ID
        self.create_test_sections()

        # Try to get all Sections based on ID
        # Check will be made by comparing Section name to Section ID, which in this test are the same
        for i in range(5):
            section = api.get_section_by_id(i+1)
            self.assertEqual(section.name, str(i+1))

    def test_get_section_by_department(self):
        # empty db should have nothing
        sections = api.get_all_sections()
        self.assertFalse(list(sections))

        # Create 5 sections where every attribute is the same as the ID
        self.create_test_sections()

        # Create 5 more sections
        # Sections will be made in a way that each of the 10 sections will share a department with another section
        sectionAdd = []
        for i in range(5):
            num = str(i+6)
            departmentNum = str(i+1)
            sectionAdd.append(Section(ta=num, lecture=None, name=num, title=num, department=departmentNum,
                                        location=num, days=num, time=num, max_spots=num, space=num))
        db.session.add_all(sectionAdd)
        db.session.commit()

        # Try to get all Sections based on department
        # Check will be made by making sure there are 2 sections in a department, and by checking the name of the department
        # to make sure they match expected values
        for i in range(5):
            sections = api.get_sections_by_department(i+1)
            sectionList = list(sections)
            # Make sure there are 2 sections in department
            self.assertEqual(len(sectionList), 2)
            # Make sure the 2 sections are the one expected
            self.assertEqual(sectionList[0].name, str(i+1))
            self.assertEqual(sectionList[1].name, str(i+6))

if __name__ == '__main__':
    unittest.main()
