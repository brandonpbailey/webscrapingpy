import crawl_site
from link_crawler import link_crawler
from advanced_link_crawler import download
from lxml.html import fromstring, tostring
import re
import cssselect


url = 'http://example.webscraping.com/places/default/view/United-Kingdom-239'
html = download(url)
tree = fromstring(html)
table = tree.xpath('//table')[0]
table.getchildren()
