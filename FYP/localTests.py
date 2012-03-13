import unittest
from travel_app import *
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

class LocalTests(unittest.TestCase):

    def testJson(self):
        result = UserStats.makeJSON(self, {})
        assertEqual(1,1);
        
if __name__ == '__main__':
    unittest.main()