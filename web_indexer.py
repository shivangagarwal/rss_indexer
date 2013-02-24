import requests
import nltk
from BeautifulSoup import BeautifulSoup


neglect_word_list = []
rss_feed_list = []
url_title_dict = {}
word_count_url_dict = {}

def read_stop_word_file():
    """This function will read the stop_words.txt file from the current folder
    and populate the global neglect_word_list
    """
    stop_words_file = open('stop_words.txt', 'r')
    word_lines = stop_words_file.readlines()
    stop_words_file.close()
    for word in word_lines:
	neglect_word_list.append(word.strip())

def read_rss_feed_file():
    """This function reads the rss feed list and generated the rss list and populate
    the global rss_feed_list
    """
    rss_file = open('feeds.txt','r')
    rss_lines = rss_file.readlines()
    rss_file.close()
    for rss in rss_lines:
	rss_feed_list.append(rss.strip())


def index_url_title(rss_urls):
    """
    This function reads the rss feed urls and makes a dict of urls and title
    which we will be using for the mapping
    """
    for url in rss_urls:
	print "    Getting feed from url:%s" %(url)
	r = requests.get(url = url)
	if r.ok:
	    prettify_content = BeautifulSoup(r.content)
	    items = prettify_content.findAll('item')
	    for item in items:
		prettify_item = BeautifulSoup("%s" %(item))
		link = get_link("%s" %(prettify_item))
		if link not in url_title_dict:
		    url_title_dict[link] = prettify_item.find('title').renderContents().strip()

def get_link(item_string):
    """This function takes the prettified item as a string object and e)tracts out the link from it
    """
    start_index = item_string.find("<link />") + len("<link />")
    end_index = item_string.find("<", start_index)
    return item_string[start_index:end_index].strip()


def process_article_data(url):
    r = requests.get(url = url)
    if r.ok:
	word_list = nltk.clean_html(BeautifulSoup(r.content).find('body').renderContents()).split()
	for word in word_list:
	    word = word.strip().lower()
	    if len(word) != 0:
		if word not in neglect_word_list:
		#process only if it is a valid word
		    if word in word_count_url_dict:
			url_count_list = word_count_url_dict[word]
			present = False
			for x in url_count_list:
			    if x['url'] == url:
				x['count'] = x['count'] + 1
				present = True
			if not present:
			    url_count_list.append({'url':url, 'count':1})
		    else:
			word_count_url_dict[word] = [{'url':url, 'count':1}]


def get_result(lookup_word):
    """Prints the result from the dicts
    """
    if lookup_word in word_count_url_dict:
	urls = word_count_url_dict[lookup_word]
	print "We found %s articles with the word '%s'\n" %(len(urls), lookup_word)
	i = 1
	for url_map in urls[:10]:
	    print "%s) '%s' [search term occurs %s times] '%s'" %(i, url_title_dict[url_map['url']], url_map['count'],url_map['url'])
	    i = i +1
    else:
	print "Lookup Word not found..."
    print "\n"


def initialize_indexer():
    """Intitializes the indexer and gets all the words and counts 
    """
    print "Reading the stop words file..."
    read_stop_word_file()
    print "Done"
    print "Reading the rss feed file"
    read_rss_feed_file()
    print "Done"
    print "Reading the rss feeds and generating the title/url map..."
    index_url_title(rss_urls = rss_feed_list)
    print "Done"
    print "Reading Single articles and dumping its word data..."
    print "Total urls to Dump Data: %s" %(len(url_title_dict))
    i =1
    for url in url_title_dict:
	print "    %s. Dumping Data for url: %s" %(i, url)
	i = i+1
	process_article_data(url)
    from operator import itemgetter
    for word in word_count_url_dict:
	word_count_url_dict[word].sort(key=itemgetter('count'), reverse=True)
    print "Done"


if __name__ == '__main__':
    #intialize the web indexer and read the rss feed list and stop words
    initialize_indexer()
    while True:
	input_line = raw_input("Please enter a single search term [enter to break]:")
	input_line = input_line.strip().lower()
	if len(input_line) > 0:
	    get_result(lookup_word=input_line)
	else:
	    print "Please enter a valid search string"
	    