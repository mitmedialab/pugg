import unittest
import sample_class
import test_common 

class SampleClassTest(unittest.TestCase):
  def setUp(self):
    test_common.CommonSetup.setupMediaCloudFixtures()
    test_common.CommonSetup.setupNYTimesFixtures()
   
  def tearDown(self):
    test_common.CommonSetup.teardownMediaCloudFixtures()
    test_common.CommonSetup.teardownNYTimesFixtures()

  def testSetupTeardown(self):
    self.assertEqual(5, test_common.MONGO_DB.mc_import_articles.count())
    self.assertEqual(39, test_common.MONGO_DB.articles.count())

test_common.ALL_TESTS.append(SampleClassTest)

if __name__ == '__main__':
  unittest.main()
