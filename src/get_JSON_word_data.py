import json
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from string import *
import re
from operator import itemgetter

# Draw the Raphael lines, top line and bottom line,
#  to go around the sentence divs and designate the graph.
# heights is a list of the heights of the 20 sentence divs.
# width is the width, in pixels, of the divs.
# spacing is the space, in pixels, between the divs; width
#  of the raphael curves will equal to spacing.
# c_h is the curve height of the raphael curves.
# start_x is the leftmost side of the graph.
# y_topspace is the length, in pixels, of the space I've
#  allotted for all the shit that goes on top of the graph.
# RETURNS tuple (top raphael line, bottom raphael line)
def stringer(heights, width, spacing, c_h, start_x, start_y):
    # Add a curve to top and bottom raphael lines with specified
    #  change in x and y (y specified for top line)
    def curve(chx1, chy1, chx2, chy2, x, yt, yb, rt, rb):
        x += chx1
        yt += chy1
        yb -= chy1
        rt += 'S' + str(x) + ',' + str(yt) + ','
        rb += 'S' + str(x) + ',' + str(yb) + ','
        x += chx2
        yt += chy2
        yb -= chy2
        rt += str(x) + ',' + str(yt)
        rb += str(x) + ',' + str(yb)
        return [x, yt, yb, rt, rb]
    
    # Add a line to top and bottom raphael lines with specified
    #  change in x and y (y specified for top line)
    def line(chx, chy, x, yt, yb, rt, rb):
        x += chx
        yt += chy
        yb -= chy
        rt += 'L' + str(x) + ',' + str(yt)
        rb += 'L' + str(x) + ',' + str(yb)
        return [x, yt, yb, rt, rb]
    
    # Specify curve width of raphael curves.
    c_w = spacing
    
    # Start the raphael lines.
    rt = "M"+str(start_x)+"," + str(start_y-1) # raphael line top
    rb = "M"+str(start_x)+"," + str(start_y) # raphael line bottom
    
    # Initiate the x and y tracker variables.
    x = start_x
    yt =  start_y # y top
    yb =  start_y # y bottom

    diff = heights[0] / 2
    if diff <= (c_h/2):
    # vertical distance too short for connecting line
        [x, yt, yb, rt, rb] = curve(0, diff + (c_h/2), c_w, 0, x, yt, yb, rt, rb)
    else:
        [x, yt, yb, rt, rb] = line(0, diff - (c_h/2), x, yt, yb, rt, rb)
        [x, yt, yb, rt, rb] = curve(0, c_h, c_w, 0, x, yt, yb, rt, rb)
    [x, yt, yb, rt, rb] = line(width - c_w, 0, x, yt, yb, rt, rb)

    # Iterate through heights to draw top and bottom lines.
    for i in range(1, len(heights)):
        diff = (heights[i] - heights[i-1]) / 2
        if abs(diff) < 2*c_h:
            # vertical distance too short for connecting line
            rise = diff/2
            [x, yt, yb, rt, rb] = curve(c_w, 0, 0, rise, x, yt, yb, rt, rb)
            [x, yt, yb, rt, rb] =\
                curve( 0, diff - rise, c_w, 0, x, yt, yb, rt, rb)
        else:
            m = abs(diff)/diff # either 1 or -1 for rise or drop
            vdist = diff - m*20
            [x, yt, yb, rt, rb] = curve(c_w, 0, 0, m*c_h, x, yt, yb, rt, rb)
            [x, yt, yb, rt, rb] = line(0, vdist, x, yt, yb, rt, rb)
            [x, yt, yb, rt, rb] = curve(0, m*c_h, c_w, 0, x, yt, yb, rt, rb)
        [x, yt, yb, rt, rb] = line(width - c_w, 0, x, yt, yb, rt, rb)

    # Finish last piece of raphael lines
    diff = heights[-1] / 2
    extra = heights[-1] % 2
    if diff <= c_h / 2:
    # vertical distance too short for connecting line
        [x, yt, yb, rt, rb] = curve(c_w, 0, 0, -diff-extra, x, yt, yb, rt, rb)
        
    else:
        [x, yt, yb, rt, rb] = curve(c_w, 0, 0, -c_h, x, yt, yb, rt, rb)
        [x, yt, yb, rt, rb] = line(0, -diff+(c_h/2)-extra, x, yt, yb, rt, rb)
    rt += 'L'+str(x)+','+str(start_y-1)
    return [rt, rb]

class WordCounter: # Looks for single words in article fulltexts
    def __init__(self, words, mama_dir, papa_dir, baby_dir, y_topspace, c_h, div_width, div_spacing, start_x):
    # words is dictionary of lower-case words mapped to lists of
    #   words to be searched for.
    # papa_dir is string of directory where the male txt files to be searched are
    #   (sorted into sub-directory by year: each named "1987" through "2006")
    # mama_dir is string of directory where the female txt files to be searched are
    #   (sorted into sub-directory by year: each named "1987" through "2006")
    #   in which female obituaries are named by index: 0.txt, 1.txt, so on.
    # baby_dir is the directory to write results to.
    # y_topspace is the height, in pixels, allotted for all the stuff that goes
    #   above the raphael graph.
    # c_h is the curve height for the raphael graph.
    # div_width is the width of the sentence-holding divs on the graph.
    # div_spacing is the space between the sentence-holding divs.
    # start_x is the x-location, in pixels, where the raphael lines should start.
        self.papa_dir = papa_dir
        self.mama_dir = mama_dir
        self.words = words
        self.baby_dir = baby_dir
        self.y_topspace = y_topspace
        self.c_h = c_h
        self.div_width = div_width
        self.div_spacing = div_spacing
        self.start_x = start_x
        
        # This dictionary will be used when calculating word use/total articles
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
        self.yearly_male_obit_totals = {1987: 1760, \
                                        1988: 2099,\
                                        1989: 2417,\
                                        1990: 2778,\
                                        1991: 2367,\
                                        1992: 1749,\
                                        1993: 1812,\
                                        1994: 1578,\
                                        1995: 1684,\
                                        1996: 1513,\
                                        1997: 1363,\
                                        1998: 1270,\
                                        1999: 1282,\
                                        2000: 1230,\
                                        2001: 1071,\
                                        2002: 1048,\
                                        2003: 915,\
                                        2004: 801,\
                                        2005: 862,\
                                        2006: 850}

        # This dictionary will be used when calculating word use/total words
        self.yearly_female_allword_totals = {1987: 93494, 1988: 98204, \
                                          1989: 119915, 1990: 149492, \
                                          1991: 119066, 1992: 136511, \
                                          1993: 120013, 1994: 116375, \
                                          1995: 135716, 1996: 163163, \
                                          1997: 152117, 1998: 174124, \
                                          1999: 143830, 2000: 148206, \
                                          2001: 156630, 2002: 157607, \
                                          2003: 126611, 2004: 123912, \
                                          2005: 105244, 2006: 158888}

        self.yearly_male_allword_totals = {1987: 621291, 1988: 670803, \
                                           1989: 780828, 1990: 910894, \
                                           1991: 761684, 1992: 690958, \
                                           1993: 711415, 1994: 644288, \
                                           1995: 787010, 1996: 813467, \
                                           1997: 845824, 1998: 876837, \
                                           1999: 868109, 2000: 850447, \
                                           2001: 741087, 2002: 750033, \
                                           2003: 634259, 2004: 592110, \
                                           2005: 678075, 2006: 685394}


    def generate_jsons(self):

        # For font size of links in top bar
        header_font_sizes = {word: 0 for word in self.words}

        # For heights of divs
        heights_dict_fem = {word:[] for word in self.words}
        heights_dict_mal = {word:[] for word in self.words}

        # For use rates per 100,000 words
        rates_dict_fem = {word:[] for word in self.words}
        rates_dict_mal = {word:[] for word in self.words}

        # Dictionary to input into a json
        content_dict = {word:[{'id': 'meta-data', \
                               'raphlines': [], \
                               'caption': '', \
                               'words_included': self.words[word][0], \
                               'midline': 0, \
                               'c_h': self.c_h, \
                               'div_width': self.div_width, \
                               'div_spacing': self.div_spacing, \
                               'word': word.capitalize(), \
                               'y_spacing': self.y_topspace, \
                               'start_x': self.start_x + self.div_spacing, \
                               's_f': 0, \
                               'max_height_fem' : 0, \
                               'max_height_mal' : 0}] for word in self.words}

        # Data for each year
        for word in self.words:
            for i in range(20):
                content_dict[word].append(\
                    {'id': i, \
                     'sentences_fem': [], \
                     'sentences_mal': [], \
                     'heigh_fem': 0, \
                     'heigh_mal': 0, \
                     'rate_fem': 0, \
                     'rate_mal': 0, \
                     'sentence_index': 0, \
                     'start_y': 0})
            for i in range(1, len(self.words[word])):
                content_dict[word][0]['words_included'] +=  ', '+self.words[word][i]

        # Counting up female word uses and storing sentences containing those words
        for year in range(1987, 2007):
            word_count = {word: 0 for word in self.words}
            for article_index in range(self.yearly_female_obit_totals[year]):
                current_file = open(self.mama_dir+'/'+str(year)+'/'+str(article_index)+'.txt', 'r')
                fulltext = current_file.read()
                fulltext_cleaned = re.sub('        ', '', re.sub('\n', ' ', fulltext))
                tok_sent = [sentence for sentence in sent_tokenize(fulltext_cleaned)]
                tok_sent_clone = tok_sent[:]
                # Clean out duplicates
                for i in range(1, len(tok_sent)):
                    if tok_sent_clone[i] == tok_sent_clone[i-1]:
                        tok_sent.remove(tok_sent_clone[i])
                # Find word matches
                for sentence in tok_sent:
                    for word in word_tokenize(sentence):
                        word = word.lower()
                        for key in self.words:
                            if word in self.words[key]:
                                word_count[key] += 1
                                if sentence not in content_dict[key][year - 1986]['sentences_fem']:
                                    content_dict[key][year - 1986]['sentences_fem'].append(sentence)

            # Calculate and store word-use-rates
            for word in self.words:
                use_rate = \
                    (word_count[word]/float(self.yearly_female_allword_totals[year]))*100000
                content_dict[word][year-1986]['rate_fem'] = int(round(use_rate))
                rates_dict_fem[word].append(use_rate)

        # Counting up male word uses and storing sentences containing those words
        for year in range(1987, 2007):
            word_count = {word: 0 for word in self.words}
            for article_index in range(self.yearly_male_obit_totals[year]):
                current_file = open(self.papa_dir+'/'+str(year)+'/'+str(article_index)+'.txt', 'r')
                fulltext = current_file.read()
                fulltext_cleaned = re.sub('        ', '', re.sub('\n', ' ', fulltext))
                tok_sent = [sentence for sentence in sent_tokenize(fulltext_cleaned)]
                tok_sent_clone = tok_sent[:]
                # Clean out duplicates
                for i in range(1, len(tok_sent)):
                    if tok_sent_clone[i] == tok_sent_clone[i-1]:
                        tok_sent.remove(tok_sent_clone[i])
                # Find word matches
                for sentence in tok_sent:
                    for word in word_tokenize(sentence):
                        word = word.lower()
                        for key in self.words:
                            if word in self.words[key]:
                                word_count[key] += 1
                                if sentence not in content_dict[key][year - 1986]['sentences_mal']:
                                    content_dict[key][year - 1986]['sentences_mal'].append(sentence)

            # Calculate and store word-use-rates
            for word in self.words:
                use_rate = \
                    (word_count[word]/float(self.yearly_male_allword_totals[year]))*100000
                content_dict[word][year-1986]['rate_mal'] = int(round(use_rate))
                rates_dict_mal[word].append(use_rate)

        # Generate font sizes and raphael lines for each word.
        for word in self.words:
            # Calculate stretch factor for max sentence div height of 400px
            max_rate_fem = max(rates_dict_fem[word])
            max_rate_mal = max(rates_dict_mal[word])
            max_rate = max_rate_fem + max_rate_mal
            stretch_factor = 400.0/max_rate
            content_dict[word][0]['s_f'] = stretch_factor
            
            # Store heights of divs based on stretch factor
            for i in range(1, 21):
                # Female div heights
                height_fem = int(round((content_dict[word][i]['rate_fem']*stretch_factor)))-self.c_h
                height_fem -= height_fem%2 # For raphael line generator to not tend towards too short
                content_dict[word][i]['height_fem'] = height_fem
                heights_dict_fem[word].append(height_fem)
                # Male div heights
                height_mal = int(round((content_dict[word][i]['rate_mal']*stretch_factor)))-self.c_h
                height_mal -= height_mal%2 # For raphael line generator to not tend towards too short
                content_dict[word][i]['height_mal'] = height_mal
                heights_dict_mal[word].append(height_mal)
                
            # Double-count first sentence in 1987 so that active div won't hide first sentence when fired.
            content_dict[word][1]['sentences_fem'] = [content_dict[word][1]['sentences_fem'][0]] + content_dict[word][1]['sentences_fem']
            content_dict[word][1]['sentences_mal'] = [content_dict[word][1]['sentences_mal'][0]] + content_dict[word][1]['sentences_mal']
            avg_rate = int(round((sum(rates_dict_fem[word]) + sum(rates_dict_mal[word]))/ 40.0))
            font_size = 10 + min(avg_rate/30, 2)*2
            header_font_sizes[word] = font_size
            max_height_fem = max(heights_dict_fem[word])
            content_dict[word][0]["max_height_fem"] = max_height_fem
            content_dict[word][0]["max_height_mal"] = max(heights_dict_mal[word])
            midline = self.y_topspace + max_height_fem + self.c_h
            content_dict[word][0]['midline'] = midline
            for id in range(1, 21):
                content_dict[word][id]['start_y'] = midline - content_dict[word][id]['height_fem'] - self.c_h/2
            raphlist_mal = [height*2 + self.c_h for height in heights_dict_mal[word]]
            raph_mal = stringer(raphlist_mal, self.div_width, \
                                                self.div_spacing, self.c_h, self.start_x, midline)[0]
            raphlist_fem = [height*2 + self.c_h for height in heights_dict_fem[word]]
            raph_fem = stringer(raphlist_fem, self.div_width, \
                                                self.div_spacing, self.c_h, self.start_x, midline)[0]
            content_dict[word][0]['raphlines'] = [raph_mal, raph_fem]

        # Create sorted list of words based on change_ratio_fem/change_ratio_mal
        ratio_tuples = []
        for word in self.words:
            change_ratio_fem = sum([content_dict[word][i]['rate_fem'] for i in range(12, 21)])/\
                               float(sum([content_dict[word][i]['rate_fem'] for i in range(1,11)]))
            change_ratio_mal = sum([content_dict[word][i]['rate_mal'] for i in range(12, 21)])/\
                               float(sum([content_dict[word][i]['rate_mal'] for i in range(1,11)]))
            ratio_tuples.append((word, change_ratio_fem/change_ratio_mal))
        sorted_tuples = sorted(ratio_tuples, key=itemgetter(1))
        sorted_words = [item[0] for item in sorted_tuples]

        # Generate the jsons.
        topbar_datafile = open(self.baby_dir + '/topbar1.json', 'w')
        content = [{'word': word, 'size': header_font_sizes[word]} for word in sorted_words]
        topbar_datafile.write(json.dumps(content, indent=4))
        topbar_datafile.close()
        for word in self.words:
            word_datafile = open(self.baby_dir + '/' + word + '.json', 'w')
            content = content_dict[word]
            word_datafile.write(json.dumps(content, indent=4))
            word_datafile.close()

if __name__ == "__main__":
    #__init__(self, words, mama_dir, papa_dir, baby_dir, y_topspace, c_h, div_width, div_spacing, start_x):
    word_counter = WordCounter({"leadership": ["leader", "administrator", "executive", "chair", "director", "president", "chairwoman", "chairman"], \
"acting": ["actress", "actor", "thespian"], \
"academia": ["professor", "faculty", "lecturer"], \
"assistant": ["assistant", "secretary", "aide"], \
"teaching": ["teacher", "schoolteacher"], \
"law": ["lawyer", "attorney", "defender", "judge"], \
"science": ["science", "scientist", "research"], \
"fashion": ["fashion"], \
"music": ["musician", "composer", "pianist", "opera", "orchestra", "singer"], \
"visual arts" : ["artist", "painter", "photographer", "painted", "sculptor", "curator", "architect", "illustrator"], \
"writing" : ["editor", "publisher", "writer", "author", "novelist"], \
"journalism": ["reporter", "journalist", "columnist"], \
"politics": ["congress", "congresswoman", "congressman", "politics", "political"], \
"business": ["business", "company"], \
"dance": ["dancer", "dance", "ballet"], \
"medicine": ["doctor", "dr", "surgeon"], \
"military": ["military", "army", "navy"]}, "obits_fem", "obits_mal", "json_results", 165, 10, 30, 10, 40)
    word_counter.generate_jsons()

