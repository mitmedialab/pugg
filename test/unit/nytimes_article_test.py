import unittest
from nytimes_article import *
import datetime
from string import *

class NYTimesArticleTest(unittest.TestCase):
  def testCreateNYTimesArticle(self):
    nytimes_article = NYTimesArticle({'pub_date': "20070601",
     'bylines': 'By PATRICK HEALY and MARC SANTORA|Santora, Marc',
     'headline': 'Aide Says Edwards Misspoke on Reading Classified Iraq Report',
     'filename': 'data/full/2007/06/01/1851335.xml',
     'taxonomic_classifiers': 'Top|Top/News|Top/News/World|Top/News/World/Countries and Territories|Top/News/World/Countries and Territories/Iraq|Top/News/U.S.|Top/News/Washington|Top/News/Washington/Campaign 2004|Top/News/Washington/Campaign 2004/Issues|Top/News/Washington/Campaign 2004/Issues/Foreign Policy|Top/News/Washington/Campaign 2004/Candidates|Top/News/Washington/Campaign 2004/Candidates/John Edwards|Top/News/Washington/Campaign 2008|Top/News/Washington/Campaign 2008/Candidates|Top/News/World/Middle East|Top/Features|Top/Features/Travel|Top/Features/Travel/Guides|Top/Features/Travel/Guides/Destinations|Top/Features/Travel/Guides/Destinations/Middle East|Top/Features/Travel/Guides/Destinations/Middle East/Iraq'})
    self.assertEqual(2, len(nytimes_article.bylines))
    self.assertEqual("patrick healy and marc santora", nytimes_article.byline)
    self.assertEqual('data/full/2007/06/01/1851335.xml', nytimes_article.filename)
    self.assertEqual(21, len(nytimes_article.taxonomic_classifiers))
    self.assertEqual(None, nytimes_article.fulltext)
    self.assertEqual(datetime.date(2007,06,01), nytimes_article.pub_date)

if __name__ == '__main__':
  unittest.main()
