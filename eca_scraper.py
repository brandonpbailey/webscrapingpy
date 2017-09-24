from advanced_link_crawler import download
from lxml.html import fromstring, tostring
from lxml.html.clean import Cleaner
from arabic_vocab_util import Word, word_fields
from arabic_vocab_util import mongo_connect, parse_html

c = Cleaner(remove_tags=[])
mongo_connect(db='brandon') #connects to Mongo DB

parse_html('http://www.egyptianarabicdictionary.com/online/word.php?ui=&id=4000')
#parse_html('http://www.egyptianarabicdictionary.com/online/word.php?ui=&id=9670')
