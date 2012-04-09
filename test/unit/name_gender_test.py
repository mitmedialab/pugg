import unittest
import test_common
from name_gender import *

class NameGenderTest(unittest.TestCase):
  def setUp(self):
    self.name_gender = NameGender("test/fixtures/female_names.csv", "test/fixtures/male_names.csv")
  def testEstimateGender(self):
    #obvious cases
    self.assertEqual("F", self.name_gender.estimate_gender("Elizabeth"))
    self.assertEqual("M", self.name_gender.estimate_gender("Duncan"))
    self.assertEqual("M", self.name_gender.estimate_gender("duncan"))
    self.assertEqual("M", self.name_gender.estimate_gender("dUNCAN"))

    #overlapping cases
    self.assertEqual("M", self.name_gender.estimate_gender("Clair"))
    self.assertEqual("M", self.name_gender.estimate_gender("Pat"))
    self.assertEqual("F", self.name_gender.estimate_gender("Jean"))

test_common.ALL_TESTS.append(NameGenderTest)

if __name__ == '__main__':
  unittest.main()
