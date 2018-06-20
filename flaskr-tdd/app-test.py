from app import app

import unittest

class BasicTestCase(unittest.TestCase):

    def test_index(self):
        test_client = app.test_client(self)
        response = test_client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, World!')


if __name__ == '__main__':
    unittest.main()