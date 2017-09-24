import re
from pprint import pprint
from mongoengine import *
from advanced_link_crawler import download
from lxml.html import fromstring, tostring
from Word import Word
import pyarabic.araby as araby
import unicodedata
connect('brandon',host='mongodb://172.17.0.2:27017/brandon')


#list_of_items = ['Word:','Language:','Element:','Thesaurus:','Usage:','Rank:','Notes:']
table1 = {'Word':'','Language':'','Element':'','Notes':'','Usage':'','Thesaurus':'','Rank':0}
def remove_tags(table):  # removes the tags I dont want

    tags_to_remove = ['.//u','.//i','.//b','.//big','.//img','.//a','.//td','.//span']
    while table.find('.//span[@class="tr"]') is not None:
        table.find('.//span[@class="tr"]').drop_tree()
    for tag in tags_to_remove:
        while table.find(tag) is not None:
            table.find(tag).drop_tag()

    return table


url = 'http://www.egyptianarabicdictionary.com/online/word.php?ui=&id=9970'
html = download(url)
#pprint(html)
html2 = fromstring(html)


#Word Details
"""table = html2.xpath('//table')[2]
remove_tags()
for elements in table.iterdescendants():
    element_list = elements.text.split(':')
    if len(element_list) == 3:
        table1[element_list[0]] = [element_list[1].strip(),element_list[2].strip()]
    else:
        table1[element_list[0]] = element_list[1].strip()

word = Word(word=table1['Word'],language=table1['Language'],
            element=table1['Element'],notes=table1['Notes'],
            usage=table1['Usage'],thesaurus=table1['Thesaurus'],
            rank=int(table1['Rank']))
word.save()"""
output = open('output.txt','a')

#------------------
forms = html2.xpath('//table')[3]
#img = forms.findall('.//img')
#for elements in forms.findall('.//img'):
#    print(elements.values()[2][11:18])
#arabic = forms.findall('.//td[@align="right"]')
#for w in arabic:
#    print(w.text)
    #output.write(w.text)

print("----------------Form-----------")

form_pr = remove_tags(forms)
for element in forms.iterdescendants():
    word = element.text.split()
    print(word[0],word[1],word[2])




# for elements in table.iterdescendants():
#     if elements.text is not None:
#         if elements.text.strip() not in list_of_items:
#             if 'class' in elements.attrib:
#                 if elements.attrib['class'] == 'tr':
#                     print(elements.text)
#             else:
#                 print(elements.text)




"""print(table.getroottree())
test = []
for elements in table.itertext():
    if len(elements) > 1:
        print(len(elements),":",elements)

print(test)"""


###for element in table.iterchildren():
"""    print("Element:",element.tag)
    if element.getchildren() is not None:
        for child_element in element.iterchildren():
            if element.getchildren() is not None:
                print('-',"Child Element:",child_element.tag)
                for sub_element in child_element.iterchildren():
                    if sub_element.getchildren() is not None:
                        print('--', "Sub Element:", sub_element.tag)
                        for sub1_element in sub_element.iterchildren():
                            if sub1_element.getchildren() is not None:
                                print('---', "Sub1 Element:", sub1_element.tag)"""

#trhead_list = html2.xpath('//tr[@class="trhead"]/td/big/b/span[@class="tr"]/text()')
#word = html2.xpath('//tr[@class="trhead"]/td/big/b/span[@class="tr"]/text()')[0]
#note = html2.xpath('//tr[@class="trhead"]/td/text()')[1]
#print("Word:",word)
#print("Note:",note)

#sound_id = re.findall(r'play_sound\(.*?\)',html)
#print(type(sound_id))
#print(len(sound_id))


