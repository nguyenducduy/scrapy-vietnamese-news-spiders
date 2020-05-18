# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pprint import pprint
from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

DB_NAME = 'corpus'
COLLECTION_NAME = 'test_news'


def pagination(page_size, page_num):
    skips = page_size * (page_num - 1)
    cursor = db[COLLECTION_NAME].find().skip(skips).limit(page_size)

    return [x for x in cursor]


# connect to db
client = MongoClient('mongodb://127.0.0.1:27017')
db = client[DB_NAME]

# tokenzier abbr
punkt_param = PunktParameters()
abbreviation = ['g.m.t', 'e.g', 'dr', 'dr', 'vs', "000", 'mr', 'mrs', 'prof', 'inc', 'tp', 'ts', 'ths', 'th', 'vs', 'tp', 'k.l', 'a.w.a.k.e', 'a.i', '</i', 'g.w', 'ass', 'u.n.c.l.e', 't.e.s.t',
                'ths', 'd.c', 've…', 'ts', 'f.t', 'b.b', 'z.e', 's.g', 'm.p', 'g.u.y', 'l.c', 'g.i', 'j.f', 'r.r', 'v.i', 'm.h', 'a.s', 'bs', 'c.k', 'aug', 't.d.q', 'b…', 'ph', 'j.k', 'e.l', 'o.t', 's.a']
punkt_param.abbrev_types = set(abbreviation)
tokenizer = PunktSentenceTokenizer(punkt_param)

# remove missing title record
db[COLLECTION_NAME].delete_many({"title": ""})

# open file to write
with open('corpus.txt', 'a') as myFile:
    # get total doc in collection

    # loop paging
    for item in pagination(5, 1):
        myFile.write("%s\n" % item['title'])
        for x in tokenizer.tokenize(item['body']):
            myFile.write("%s\n" % x)
