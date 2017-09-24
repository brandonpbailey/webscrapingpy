from mongoengine import *
from Word import Word
from mongoengine import StringField,ListField,IntField,Document
from lxml.html import fromstring
from advanced_link_crawler import download
from lxml.html.clean import Cleaner

DB_HOST= 'mongodb://172.17.0.2:27017/brandon'

word_fields = {'Word_id':'','Word':'','Language':'','Element':'','Notes':'',
               'Usage':'','Thesaurus':'','Rank':0,'Forms':{},'Meaning':{},
               'Similar Words':{},'Arabic Sound':'', 'English Sound':'','Example':{}}

def mongo_connect(db,user='brandon',password=None):
    connect(db, host=DB_HOST)


def db_save(word):
    word.save()

def db_update(word_id, word):
    word.update()

def remove_tags(table):  # removes the tags I dont want

    c = Cleaner(remove_tags=['h1','u','big','b'])
    return c.clean_html(table)


class Word(Document):
    word_id = StringField(max_length=8,required=True)
    word = ListField(max_length=30,required=True)
    language = StringField(max_length=30,required=True)
    element = StringField(max_length=30,required=True)
    thesaurus = ListField(default=None)
    usage = StringField(default=None,max_length=20)
    rank = IntField(default=None)
    notes = StringField(default=None)
    forms = DictField(default=None)
    meaning = DictField(default=None)
    similar_words = DictField(default=None)
    arabic_sd = StringField(default=None)
    english_sd = StringField(default=None)
    example = DictField(default=None)

def parse_html(url):

    html = fromstring(download(url))  # Fetches the HTML page

    #word_id = url.split("&")[1].split('=')[1]  # just grabbing the word_id from the url
    #print(word_fields['Word_id'])  # for debugging

    div = html.xpath('.//div[@id="intro"]')[0]  # grabs the section of the html page that has the data

    """Drops he Transliteration spans, these are not needed"""
    number_of_pr = div.findall('.//span[@class="tr"]')
    for item in number_of_pr:
        item.drop_tree()

    div = remove_tags(div)  # this gets rid of the tags that are not needed, like i, h1, img
    div[0].drop_tree()  # gets rid of table1, which is not needed

    # Now This loads the htmls sections where the data that needs to be extracted

    word = div[0]
    form = div[1]
    meaning = div[2]
    similiar_words = div[3]

    new_word = get_word_details(word,Word())
    new_word.word_id = get_word_id(url)
    new_word = get_form(form,new_word)
    new_word = get_meaning(meaning,new_word)
"""
    print('Word id:', new_word.word_id)
    print('Word:', new_word.word)
    print('Element:', new_word.element)
    print('Notes:', new_word.notes)
    print('Language:', new_word.language)
    print('Thesaurus:', new_word.thesaurus)
    print('Usage:', new_word.usage)
    print('Rank:', new_word.rank)
    print('Forms:', new_word.forms)

    #return [word,form,meaning,similiar_words, word_id]
"""

def get_word_details(word_details, new_word):

    #print("get_word_details")
    #print(type(word_details),type(new_word))

    c = Cleaner(remove_tags=['td', 'a', 'img', 'span', 'i'])
    word_details = c.clean_html(word_details)
    #print(len(word_details))

    for item in word_details.iterdescendants():
        split_colon = item.text.split(':')
        #print(split_colon[0],split_colon[1])
        if split_colon[0] == 'Word':
            if '\xa0' in split_colon[1]:
                split_colon[1] = split_colon[1].split('\xa0')
                split_colon[1][0] = split_colon[1][0].lstrip()
                split_colon[1][1] = split_colon[1][1].lstrip()
            new_word.word = split_colon[1]
        if split_colon[0] == 'Notes':
            new_word.notes = split_colon[1].lstrip()
        if split_colon[0] == 'Language':
            new_word.language = split_colon[1].lstrip()
            if new_word.language == 'English':
                new_word.word = [new_word.word[0]]
        if split_colon[0] == 'Element':
            new_word.element = split_colon[1].lstrip()
        if split_colon[0] == 'Thesaurus':
            if len(split_colon) == 3:
                new_word.thesaurus = [split_colon[1].lstrip(), split_colon[2].lstrip()]
            else:
                new_word.thesaurus = split_colon[1].lstrip()
        if split_colon[0] == 'Usage':
            new_word.usage = split_colon[1].lstrip()
        if split_colon[0] == 'Rank':
            new_word.rank = split_colon[1].lstrip()

    return new_word


def get_word_id(url):
    return url.split("&")[1].split('=')[1]

def get_form(form,new_word):

    form_dict = {}
    c = Cleaner(remove_tags=['td', 'a', 'img', 'span', 'i'])
    form = c.clean_html(form)
    for item in form.iterdescendants():
        if new_word.language == 'English':
            item = item.text.split()
            #print(item)
            form_dict[item[1]] = item[0]
        else:
            item = str.encode(item.text,'utf-8')
            item = item.split(b'\xc2\xa0')
            item[1] = bytes.decode(item[1],'utf-8').split('  ')
            item = [bytes.decode(item[0],'utf-8').split()[0],item[1][0],item[1][1]]
            #print(item)
            form_dict[item[1]] = [item[0],item[2]]
    new_word.forms = form_dict


    return new_word

def get_meaning(meaning,new_word):

    meaning_dict ={}
    c = Cleaner(remove_tags=['a', 'img', 'span', 'i'])
    meaning = c.clean_html(meaning)
    y = []
    counter = 0
    for item in meaning.iterdescendants():
        if item.tag == 'td':
            if new_word.language == 'English':
                if b'\xa0' in str.encode(item.text,'utf-8'):
                    item = str.encode(item.text,'utf-8').split(b'\xc2\xa0')
                    #print(item[0])
                    item = [bytes.decode(item[0],'utf-8'),bytes.decode(item[1],'utf-8').split()[0]]
                    for i in item:
                        y.append(i)
                #y.append(item.text)
                else:
                    y.append(item.text)
            else:
                #print(counter)
                counter += 1
                if item.text is not None:
                    if counter <= 3:
                        #print(item.text)
                        if b'\xa0' in str.encode(item.text, 'utf-8'):
                            item = str.encode(item.text, 'utf-8').split(b'\xc2\xa0')
                            item = [bytes.decode(item[0], 'utf-8'), bytes.decode(item[1], 'utf-8')]
                            print(item)
                            #meaning_dict[item[1]] = [y.pop(),item[2]]
                        else:
                            #print(item.text)
                            y.append(item.text)
                    else:
                        counter = 0
                        #meaning_dict[y[0]] = [y[1],y[2]]


    #print(y)


    if new_word.language == 'English':
        meaning_dict[y[1]] = [y[0],y[2],y[3]]
    else:
        print(meaning_dict)


        #print(meaning_dict)