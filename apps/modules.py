#!/usr/bin/env python
# encoding: utf-8
"""
modules.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
from datetime import datetime
import uuid

from mongokit import Document, IS

from huwai.config import DB_NAME

class IdDoc(Document):
    __collection__ = 'ids'
    __database__ = DB_NAME

    structure = {
                '_id':unicode,
                'id':int,
    }
    use_schemaless = True
    use_dot_notation=True

class MappingDoc(Document):
    __collection__ = 'mapping'
    __database__ = DB_NAME

    structure = {
                '_id':  unicode,
                'image':unicode,
    }
    use_schemaless = True
    use_dot_notation=True

class UserDoc(Document):
    __collection__ = 'people'
    __database__ = DB_NAME

    structure = {
            '_id': unicode,
            'nick': unicode,
            'password':unicode,
            'email':unicode,
            'domain':unicode,
            'created':datetime,
            'added':dict,
            'added_id':int,
    }
    required_fields = ['_id', 'nick', 'password', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

class TimeLineDoc(Document):
    __collection__ = 'timeline'
    __database__ = DB_NAME
        
    structure = {
            '_id':      unicode,
            'owner':    unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
            'content':  unicode,
            'at_list':  list,
            'topic':    unicode,
            'channel':  IS(u'normal', u'reply', u'weibo', u'map', u'keys'),
    }
    
    required_fields = ['_id', 'created', 'content']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True
