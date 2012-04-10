import unittest
ALL_TESTS=[]
import test_common

from sample_test_case import *
from article_test import *
from article_accessor_test import *
from nytimes_article_accessor_test import *
from nytimes_article_test import *
from name_gender_test import *

runner = unittest.TextTestRunner()
results ={"run":0, "errors":[], "failures":[]}
for test in test_common.ALL_TESTS:
  print "== " + test.__name__ + " == "
  suite = unittest.makeSuite(test,'test')
  result =  runner.run(suite)
  #results["run"].extend(result.run)
  results["run"] += suite.countTestCases()
  results["errors"].extend(result.errors)
  results["failures"].extend(result.failures)
  print ""
  print ""

print "===== SUMMARY ====="
print str(results["run"]) + " Tests Run"
print str(len(results["errors"])) + " Errors"
print str(len(results["failures"])) + " Failures"

for failure in results["failures"]:
  print ""
  print failure
