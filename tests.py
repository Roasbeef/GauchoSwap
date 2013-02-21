import os
import gauchoswap
import unittest
import tempfile


class GauchoSwapApiTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, gauchoswap.app.config['DATABASE'] = tempfile.mkstemp()
        gauchoswap.app.config['TESTING'] = True
        self.app = gauchoswap.app.test_client()
        gauchoswap.db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(gauchoswap.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
