from os import listdir
from os.path import isfile, join
from scrapy.selector import Selector
import re
import operator

html_dir = 'html/'

def read_html_files():
    return [file for file in listdir(html_dir) if isfile(join(html_dir, file))]

def extract_title(html_file):
    html = open(html_dir + html_file).read()
    selector = Selector(text=html)
    return selector.css('h1.entry-title::text')[0].extract()

# extract titles from each of the posts
all_titles = [extract_title(html_file) for html_file in read_html_files()]
print "extracted " + str(len(all_titles)) + " blog titles"

# write all titles to file
with open('analytics/output/blog_titles.list', 'w') as f:
    for title in all_titles:
        f.write(title.encode('utf-8') + '\n')

# compute word frequence (normalized -> to lowercase)
def normalize(text):
    text = text.lower()
    return re.sub(r'[^\w\s]', '', text)

word_counts = {}
for title in all_titles:
    words = re.split('\s+', normalize(title))
    for word in words:
        if word not in word_counts:
            word_counts[word] = 1
        else:
            word_counts[word] += 1

# sort by values and write to file
with open('analytics/output/blog_title_word_counts.list', 'w') as f:
    for word in sorted(word_counts, key=word_counts.get, reverse=True):
        f.write(word.encode('utf-8') + '\t' + str(word_counts[word]) + '\n')
        print word, word_counts[word]
