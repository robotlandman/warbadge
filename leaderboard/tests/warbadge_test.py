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
        mac = "ecfabc12d1e1"
        query = self.app.get("/handle_for_mac/" + mac)
        self.assertEqual(query.status_code, 200)
        self.assertEqual(query.get_data(), "kencaruso")

        new_handle = { "handle" : "new_handle" }
        insert = self.app.post("/handle/" + mac, data=new_handle, headers={'Content-type': 'application/json'})
        self.assertEqual(insert.status_code, 201)

        query = self.app.get("/handle_for_mac/" + mac)
        self.assertEqual(query.status_code, 200)
        self.assertEqual(query.get_data(), "new_handle")

        update_handle = { "handle" : "kencaruso" }
        update = self.app.post("/handle/" + mac, data=update_handle, headers={'Content-type': 'application/json'})
        self.assertEqual(update.status_code, 200)

        query = self.app.get("/handle_for_mac/" + mac)
        self.assertEqual(query.status_code, 200)
        self.assertEqual(query.get_data(), "kencaruso")

if __name__ == '__main__':
    unittest.main()
