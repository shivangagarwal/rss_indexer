RSS Feed Indexer and Searcher

External Libraries Used:

BeautifulSoup: This parses the RSS XML file into a python format
Request Package: This is the package used to make get requests on the particular urls and getting their content
nltk: The natural language processing package, it is used to parse the html and making it into a readable format

ThoughtProcess:
The solution is a synchronous solution in which we are extracting urls and title from the rss urls and dumping them into a dict: url_title_dict
After this dict formation we are dumping the data from each url that we got, and generating a map of word to the number of occurrences in the each url: word_count_url_dict
The format of the single entity in this dissect is: {word: [{'url':url1, count:count1}, {'url':url2, count:count2}É]}

Input: 
	feeds.txt: file containing the rss feed urls which we need to parse
	stop_words.txt:Containing the words which needs to be ignored

For getting the search result for the word: we do a lookup into the word_url_count_dict and retrieve title from url_title_dict
