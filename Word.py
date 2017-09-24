from mongoengine import StringField,ListField,IntField,Document, DictField


class Word(Document):
    word_id = StringField(max_length=8,required=True)
    word = StringField(max_length=30,required=True)
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
