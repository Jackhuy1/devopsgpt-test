import unittest
from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Classic Snake Game', response.data)

    def test_static_file(self):
        response = self.app.get('/static/style.css')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'body', response.data)

if __name__ == '__main__':
    unittest.main()
