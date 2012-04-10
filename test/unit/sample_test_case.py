import unittest
import sample_class
import test_common 
from mongo_connection import *

class SampleClassTest(unittest.TestCase):
  def setUp(self):
    test_common.CommonSetup.setupMongoDBFixtures()
   
  def tearDown(self):
    test_common.CommonSetup.teardownMongoDBFixtures()

  def testSetupTeardown(self):
    self.assertEqual(5, MONGO_DB.mc_articles.count())

test_common.ALL_TESTS.append(SampleClassTest)

if __name__ == '__main__':
  unittest.main()
