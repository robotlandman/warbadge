# -*- coding: utf-8 -*-
import unittest
import json

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

    def test_get_handle(self):
        # staff
        mac = "ecfabc12d1e1"
        query = self.app.get("/handle_for_mac/" + mac)
        self.assertEqual(query.status_code, 200)
        self.assertEqual(query.get_data(), '"kencaruso *STAFF"')

        # regular
        mac = "dc4f220ba602"
        query = self.app.get("/handle_for_mac/" + mac)
        self.assertEqual(query.status_code, 200)
        self.assertEqual(query.get_data(), '"jackal"')

        # not found
        mac = "ecfabc12d724"
        query = self.app.get("/handle_for_mac/" + mac)
        self.assertEqual(query.status_code, 200)
        self.assertEqual(query.get_data(), '"--------"')


    def test_handle(self):
        mac = "ecfabc12d724"
        query = self.app.get("/handle_for_mac/" + mac)
        self.assertEqual(query.status_code, 200)
        self.assertEqual(query.get_data(), '"--------"')

        new_handle = json.dumps({ "handle" : "a_handle" }).encode('utf8')
        insert = self.app.post("/handle/" + mac, data=new_handle, headers={'Content-type': 'application/json; charset=utf-8'})
        self.assertEqual(insert.status_code, 201)

        query = self.app.get("/handle_for_mac/" + mac)
        self.assertEqual(query.status_code, 200)
        self.assertEqual(query.get_data(), '"a_handle"')

        update_handle = json.dumps({ "handle" : "moose" }).encode('utf8')
        update = self.app.post("/handle/" + mac, data=update_handle, headers={'Content-type': 'application/json; charset=utf-8'})
        self.assertEqual(update.status_code, 200)

        query = self.app.get("/handle_for_mac/" + mac)
        self.assertEqual(query.status_code, 200)
        self.assertEqual(query.get_data(), '"moose"')

    def test_handle_unicode(self):
        mac = "020000000001"
        query = self.app.get("/handle_for_mac/" + mac)
        self.assertEqual(query.status_code, 200)
        self.assertEqual(query.get_data(), '"--------"')

        unicode_str = u"a_handle☃" 
        new_handle = json.dumps({ "handle" : unicode_str }).encode('utf8')
        insert = self.app.post("/handle/" + mac, data=new_handle, headers={'Content-type': 'application/json; charset=utf-8'})
        self.assertEqual(insert.status_code, 201)

        query = self.app.get("/handle_for_mac/" + mac)
        self.assertEqual(query.status_code, 200)
        # self.assertEqual(query.get_data(), '\"' + unicode_str + '"')

        unicode_str = u"a_moose☃" 
        update_handle = json.dumps({ "handle" : unicode_str }).encode('utf8')
        update = self.app.post("/handle/" + mac, data=new_handle, headers={'Content-type': 'application/json; charset=utf-8'})
        self.assertEqual(update.status_code, 200)

        query = self.app.get("/handle_for_mac/" + mac)
        self.assertEqual(query.status_code, 200)
        # self.assertEqual(query.get_data(), '\"' + unicode_str + '"')

if __name__ == '__main__':
    unittest.main()
