from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from string import *
import re
from operator import itemgetter

class WordCounter: # Looks for single words in article fulltexts
    def __init__(self, phrases, papa_dir):
    # phrases is list of lower-case words to be searched for,
    # papa_dir is string of directory where the txt files to be searched are
    #   (sorted into sub-directory by year: each named "1987" through "2006")
    #   in which female obituaries are named by index: 0.txt, 1.txt, so on.
    #   papa_dir must also contain empty directory named "results".
        self.papa_dir = papa_dir
        self.phrases = phrases
        
        # This dictionary will be used when calculating phrase use/total articles
        self.yearly_female_obit_totals = {1987: 293, 1988: 338, \
                                          1989: 415, 1990: 456, \
                                          1991: 375, 1992: 369, \
                                          1993: 320, 1994: 312, \
                                          1995: 327, 1996: 329, \
                                          1997: 268, 1998: 263, \
                                          1999: 238, 2000: 235, \
                                          2001: 232, 2002: 223, \
                                          2003: 193, 2004: 187, \
                                          2005: 156, 2006: 193}

        # This dictionary will be used when calculating phrase use/total words
        self.yearly_allword_totals = {1987: 93494, 1988: 98204, \
                                          1989: 119915, 1990: 149492, \
                                          1991: 119066, 1992: 136511, \
                                          1993: 120013, 1994: 116375, \
                                          1995: 135716, 1996: 163163, \
                                          1997: 152117, 1998: 174124, \
                                          1999: 143830, 2000: 148206, \
                                          2001: 156630, 2002: 157607, \
                                          2003: 126611, 2004: 123912, \
                                          2005: 105244, 2006: 158888} 
        
      # Create a dictionary mapping phrases to (boolean, int)
      # for marking and counting occurrences of that phrase.
      # bool, number of articles using that phrase, num articles phrase/total num articles,
      #   total phrase uses/total words, total phrase uses
        self.phrase_counter = {}

        self.phrase_fulltext_dict = {} # For .txt's to store relevant fulltext


    def count_words(self):
        self.phrase_counter = \
            {phrase: [0, {year:0 for year in range(1987,2007)}, False] for phrase in self.phrases}
        
      # Create 20 txt files (one per year) associated with each phrase in which
      # to store fulltexts that contain that phrase.
      # Create another 20 for storing just the sentences containing that phrase.
      # Must access using dict[phrase][0][year-1987]
      # and dict[phrase][1][year-1987], respectively.
        line = "year" 
        for phrase in self.phrases:
<<<<<<< HEAD
	    self.phrase_fulltext_dict[phrase] = [[],[]]
            self.phrase_fulltext_dict[phrase][0] = \
                [open(self.papa_dir+'/results/'+phrase+'_full_'+str(i)+'.txt', 'w') for i in range(1987, 2007)]
=======
            self.phrase_fulltext_dict[phrase][0] = \
                [open(self.papa_dir+'/results/'+phrase+'_full_'+str(i)+'.txt', 'w')\
                 for i in range(1987, 2007)]
>>>>>>> 475d63241309e7a435fbf3ce99b60d76d2aa500a
            self.phrase_fulltext_dict[phrase][1] = \
                [open(self.papa_dir+'/results/'+phrase+'_sent_'+str(i)+'.txt', 'w')\
                 for i in range(1987, 2007)]
            line = line +','+phrase+'_cases_per_100k'
        print line

        for year in range(1987, 2007):
            for article_index in range(self.yearly_female_obit_totals[year]):
                current_file = open(self.papa_dir+'/'+str(year)+'/'+str(article_index)+'.txt', 'r')
                fulltext = current_file.read()
                for sentence in sent_tokenize(fulltext):
                    for word in word_tokenize(sentence):
                        word = word.lower()
                        if word in self.phrases:
                            self.phrase_counter[word][0] += 1
                            self.phrase_fulltext_dict[word][1][year-1987].write(sentence+'\n')
                            if not self.phrase_counter[word][2]:
                                self.phrase_counter[word][2] = True
                                self.phrase_fulltext_dict[word][0][year-1987].write(re.sub('\n', ' ', fulltext)+'\n')
                current_file.close()
                # Increment phrase count and reset phrase bool to false
                for phrase in self.phrases:
                    self.phrase_counter[phrase][2] = False

            # Calculate and store phrase-use-rates
            line = str(year)
            for phrase in self.phrases:
                self.phrase_counter[phrase][1][year] = \
                    (self.phrase_counter[phrase][0]/float(self.yearly_allword_totals[year]))*100000
<<<<<<< HEAD
                line = line + ',' + str(self.phrase_counter[phrase][1][year])
=======
                line = line + ',' + self.phrase_counter[phrase][1][year]
>>>>>>> 475d63241309e7a435fbf3ce99b60d76d2aa500a
                self.phrase_counter[phrase][0] = 0
            print line

        # Calculate and print change_ratio and avg_rate
        print "phrase,change_ratio,avg_rate"
        # Calculate change_ratio for each year then get list of phrases sorted that way
        ratio_tuples = []
        for phrase in self.phrases:
            change_ratio = sum([self.phrase_counter[phrase][1][year] for year in range(1997,2007)])/\
                               sum([self.phrase_counter[phrase][1][year] for year in range(1987,1997)])
            ratio_tuples.append((phrase, change_ratio))
        sorted_tuples = sorted(ratio_tuples, key=itemgetter(1))

        # Calculate avg_rate and print change_ratio and avg_rate for each phrase
        for (phrase, change_ratio) in sorted_tuples:
            avg_rate = sum([self.phrase_counter[phrase][1][year] for year in range(1987,2007)]) / 20
            line = phrase+','+str(round(change_ratio, 3))+','+str(round(avg_rate, 1))
            print line

    def count_change_ratio_and_avg_rate(self):
      # Looks at fulltexts of female featured obituaries, 1987-2006.
      # Generates lines to be saved to a csv file with rows "phrase,change_ratio,avg_rate".
      # "phrase" is the word or ngram (so far just word) in question.
      # "change_ratio" is avg use rate in 2nd decade / avg use rate in 1st decade,
      # where use rate is number of occurrrences of the phrase per 100,000 words that year.
      # "avg_rate" is the arithmetic average of the use rates over the 20-year period.

        self.phrase_counter = {phrase: [0, {year:0 for year in range(1987,2007)}] for phrase in self.phrases}
        # Stores [use count, {use rates by year}]
      
        print "phrase,change_ratio,avg_rate"
        
        for year in range(1987, 2007):
            for article_index in range(self.yearly_female_obit_totals[year]):
                current_file = open(self.papa_dir+'/'+str(year)+'/'+str(article_index)+'.txt', 'r')
                fulltext = current_file.read()
                for sentence in sent_tokenize(fulltext):
                    for word in word_tokenize(sentence):
                        word = word.lower()
                        if word in self.phrases:
                            self.phrase_counter[word][0] += 1
                current_file.close()

            # Calculate and store phrase-use-rates
            for phrase in self.phrases:
                self.phrase_counter[phrase][1][year] = (self.phrase_counter[phrase][0]/float(self.yearly_allword_totals[year]))*100000
                self.phrase_counter[phrase][0] = 0

        # Calculate change_ratio for each year then get list of phrases sorted that way
        ratio_tuples = []
        for phrase in self.phrases:
            change_ratio = sum([self.phrase_counter[phrase][1][year] for year in range(1997,2007)])/\
                               sum([self.phrase_counter[phrase][1][year] for year in range(1987,1997)])
            ratio_tuples.append((phrase, change_ratio))
        sorted_tuples = sorted(ratio_tuples, key=itemgetter(1))

        # Calculate avg_rate and print change_ratio and avg_rate for each phrase
        for (phrase, change_ratio) in sorted_tuples:
            avg_rate = sum([self.phrase_counter[phrase][1][year] for year in range(1987,2007)]) / 20
            line = phrase+','+str(round(change_ratio, 3))+','+str(round(avg_rate, 1))
            print line

    def count_total_words(self):
        print "year,word_total,avg_obit_length_in_words"
        for year in range(1987, 2007):
            word_total = 0
            for article_index in range(self.yearly_female_obit_totals[year]):
                current_file = open(self.papa_dir+'/'+str(year)+'/'+str(article_index)+'.txt', 'r')
                fulltext = current_file.read()
                for sentence in sent_tokenize(fulltext):
                    for word in word_tokenize(sentence):
                        word_total += 1
                        current_file.close()
            print str(year)+','+str(word_total)+','+str(word_total/float(self.yearly_female_obit_totals[year]))

                
            
if __name__ == "__main__":
<<<<<<< HEAD
    word_counter = WordCounter(['grandchildren', 'brother', 'sister', 'daughter', 'husband', 'son', 'family', 'wife', 'children', 'friend', 'divorce', 'child', 'married', 'mother', 'father'], "obits_fem")
    word_counter.count_words()
=======
    word_counter = WordCounter(["married", "founded", "research"], "obits_fem")
    word_counter.count_change_ratio_and_avg_rate()
>>>>>>> 475d63241309e7a435fbf3ce99b60d76d2aa500a
