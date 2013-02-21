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

if __name__ == '__main__':
    unittest.main()
