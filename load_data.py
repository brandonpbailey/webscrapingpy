from mongoengine import *
import datetime

connect('brandon',host='mongodb://172.17.0.2:27017/brandon')

class Page(Document):
    title = StringField(max_length=200, required=True)
    date_modified=DateTimeField(default=datetime.datetime.now)

page = Page(title='Test')

page.save()