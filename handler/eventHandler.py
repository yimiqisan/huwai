#!/usr/bin/env python
# encoding: utf-8
"""
common.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
from mongokit import *
import datetime
import types 
import pymongo
import uuid

from baseHandler import BaseHandler

class EventHandler(BaseHandler):
    def get(self):
        stra = self.get_spider_events()
        l=len(stra)/2
        entries1=[]
        entries2=[]
        for i in range(l):
            entries1.append(stra[i])
            entries2.append(stra[i+l])
            #handler data for outputing
        self.render("event.html", entries1=entries1, entries2=entries2, entries=stra)

    def get_spider_events(self, page=1, number=8, data="all"):
        conn = Connection()
        conn.register([ActivityData])
        col = conn.test.example
        return list(col.find().sort('rank', pymongo.DESCENDING))

class DBException(Exception):
    def __init__(self, error):
        Exception.__init__(self)
        self.error = error

class ActivityData(Document):
    structure = {
        'title':unicode,
        'link':unicode,
        'imageurl':{"originurl":unicode,"localurl":unicode},
        'organizername':unicode,
        'activityclass':unicode,
        'place':unicode,
        'time':unicode,
        'hotnumber':unicode,
        'uuid':str,
        'date_creation':datetime.datetime,
        'rank':int
    }
    required_fields = ['title','link','imageurl.originurl','imageurl.localurl','organizername','activityclass','place','time','hotnumber']
    default_values = {'uuid':str(uuid.uuid4()), 'rank':0, 'date_creation':datetime.datetime.utcnow}
