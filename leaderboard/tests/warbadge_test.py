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

    def test_handle(self):
        new_handle = { "handle" : "new_handle" }
        insert = self.app.post("/handle/020000000001", data=new_handle)
        self.assertEqual(insert.status_code, 201)

        iquery = self.app.get("/handle_for_mac/020000000001")
        self.assertEqual(iquery.status_code, 200)
        self.assertEqual(iquery.get_json()['handle'], "new_handle")

        update_handle = { "handle" : "cool_handle" }
        update = self.app.post("/handle/020000000001", data=update_handle)
        self.assertEqual(update.status_code, 201)

        uquery = self.app.get("/handle_for_mac/020000000001")
        self.assertEqual(uquery.status_code, 200)
        self.assertEqual(uquery.get_json()['handle'], "cool_handle")

if __name__ == '__main__':
    unittest.main()
