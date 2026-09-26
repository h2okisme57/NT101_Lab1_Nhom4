import unittest
from recursive_json_search import *
from test_data import *


class json_search_test(unittest.TestCase):
    '''test module to test search function in recursive_json_search.py'''

    # ------------------------------------------------------------------
    # Functional tests (a valid role still gets its allowed data: SR-5)
    # ------------------------------------------------------------------
    def test_search_found(self):
        '''key should be found, return list should not be empty'''
        self.assertTrue([] != json_search(key1, data, role="admin"))

    def test_search_not_found(self):
        '''key should not be found, should return an empty list'''
        self.assertTrue([] == json_search(key2, data, role="admin"))

    def test_is_a_list(self):
        '''Should return a list'''
        self.assertIsInstance(json_search(key1, data, role="admin"), list)

    # ------------------------------------------------------------------
    # Security tests
    # ------------------------------------------------------------------
    def test_viewer_cannot_read_apikey(self):
        '''SR-1: viewer must not read apiKey'''
        self.assertEqual([], json_search("apiKey", data, role="viewer"))

    def test_operator_cannot_read_apikey(self):
        '''SR-1: operator must not read apiKey'''
        self.assertEqual([], json_search("apiKey", data, role="operator"))

    def test_viewer_cannot_read_management_ip(self):
        '''SR-2: viewer must not read managementIpAddress'''
        self.assertEqual([], json_search("managementIpAddress", data, role="viewer"))

    def test_no_role_cannot_read_secret(self):
        '''SR-3: a missing/None role is denied by default'''
        self.assertEqual([], json_search("apiKey", data))

    def test_admin_can_read_apikey(self):
        '''SR-1/SR-4: admin still receives the deeply nested apiKey value'''
        self.assertIn({"apiKey": "SNMP-COMMUNITY-STRING-7f3a9c"},
                      json_search("apiKey", data, role="admin"))

    def test_viewer_can_read_issue_summary(self):
        '''SR-5: a viewer keeps read access to issueSummary'''
        self.assertTrue([] != json_search("issueSummary", data, role="viewer"))


if __name__ == '__main__':
    unittest.main()
