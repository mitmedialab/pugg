import config
config.PUGG_DB="pugg_test"

import unittest
import sample_class
import test_common 
from mongo_connection import *

class SampleClassTest(unittest.TestCase):
  def setUp(self):
    test_common.CommonSetup.setupMediaCloudFixtures()
    test_common.CommonSetup.setupNYTimesFixtures()
   
  def tearDown(self):
    test_common.CommonSetup.teardownMediaCloudFixtures()
    test_common.CommonSetup.teardownNYTimesFixtures()

  def testSetupTeardown(self):
    self.assertEqual(5, MONGO_DB.mc_articles.count())
    self.assertEqual(39, MONGO_DB.articles.count())

test_common.ALL_TESTS.append(SampleClassTest)

if __name__ == '__main__':
  unittest.main()
