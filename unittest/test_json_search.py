import unittest
from recursive_json_search import *
from test_data import *

class json_search_test(unittest.TestCase):
    '''test module to test search function in recursive_json_search.py'''

    def test_search_found(self):
        '''key should be found, return list should not be empty'''
        self.assertTrue([] != json_search(key1, data, role="admin"))

    def test_search_not_found(self):
        '''key should not be found, should return an empty list'''
        self.assertTrue([] == json_search(key2, data, role="admin"))

    def test_is_a_list(self):
        '''Should return a list'''
        self.assertIsInstance(json_search(key1, data, role="admin"), list)

    def test_viewer_cannot_read_apikey(self):
        '''SR-1: viewer must not read apiKey'''
        self.assertEqual([], json_search("apiKey", data, role="viewer"))

    def test_viewer_cannot_read_management_ip(self):
        '''SR-2: viewer must not read managementIpAddress'''
        self.assertEqual([], json_search("managementIpAddress", data, role="viewer"))

    def test_no_role_cannot_read_secret(self):
        '''SR-3: missing role is denied by default'''
        self.assertEqual([], json_search("apiKey", data))

if __name__ == '__main__':
    unittest.main()
