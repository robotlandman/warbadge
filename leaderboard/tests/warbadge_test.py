import unittest

from warbadge_app.app import app


class WarbadgeTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_index_page(self):
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200) 

    def test_scoreboard(self):
        result = self.app.get("/scoreboard")
        self.assertEqual(result.status_code, 200) 

    def test_stats(self):
        result = self.app.get("/stats")
        self.assertEqual(result.status_code, 200) 

if __name__ == '__main__':
    unittest.main()