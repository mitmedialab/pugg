import unittest
import test_common
from name_gender import *

class NameGenderTest(unittest.TestCase):
  def setUp(self):
    self.name_gender = NameGender("test/fixtures/female_names.csv", "test/fixtures/male_names.csv")

  def testEstimateGender(self):
    #obvious cases
    self.assertEqual(None, self.name_gender.estimate_gender("SlithyTove"))
    self.assertEqual("F", self.name_gender.estimate_gender("Elizabeth"))
    self.assertEqual("M", self.name_gender.estimate_gender("Duncan"))
    self.assertEqual("M", self.name_gender.estimate_gender("duncan"))
    self.assertEqual("M", self.name_gender.estimate_gender("dUNCAN"))

    #overlapping cases
    self.assertEqual("M", self.name_gender.estimate_gender("Clair"))
    self.assertEqual(None, self.name_gender.estimate_gender("Pat"))
    self.assertEqual("F", self.name_gender.estimate_gender("Jean"))

    self.assertEqual("M", self.name_gender.estimate_gender("gerald eskenazi"))
    self.assertEqual("F", self.name_gender.estimate_gender("georgia dulleo"))
    self.assertEqual("F", self.name_gender.estimate_gender("patricia malarcher"))

  def testCheckGender(self):
    self.assertEqual(None, self.name_gender.check_gender("SlithyTove"))
    self.assertEqual("F", self.name_gender.check_gender("Elizabeth"))
    self.assertEqual("M", self.name_gender.check_gender("Duncan"))
    #overlapping cases
    self.assertEqual(None, self.name_gender.check_gender("Clair"))
    self.assertEqual(None, self.name_gender.check_gender("Pat"))
    self.assertEqual(None, self.name_gender.check_gender("Jean"))

test_common.ALL_TESTS.append(NameGenderTest)

if __name__ == '__main__':
  unittest.main()
