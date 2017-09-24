from pprint import pprint
from lxml import etree, html
from io import StringIO, BytesIO
from advanced_link_crawler import download
from requests.utils import get_encodings_from_content
from codecs import StreamRecoder
import codecs
from lxml.html.clean import Cleaner

word_fields = {'Word_id':'','Word':'','Language':'','Element':'','Notes':'',
               'Usage':'','Thesaurus':'','Rank':0,'Forms':{},'Meaning':{},
               'Similar Words':{},'Arabic Sound':'', 'English Sound':'','Example':{}}

url = 'http://www.lisaanmasry.com/online/word.php?ui=&id=307'
html = download(url)
pprint(html)
'''
with open("test.html") as f:
    a = f.read()

html2 = etree.HTML(new_html)
result = etree.tostring(html2, encoding='unicode', pretty_print=True, method="html")

print(result)
'''