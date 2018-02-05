from app import app
import unittest

class FlaskappTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_users_status_code(self):
        result = self.app.get('/api/v1/user')
        self.assertEqual(result.status_code, 200)

