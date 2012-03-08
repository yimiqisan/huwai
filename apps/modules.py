#!/usr/bin/env python
# encoding: utf-8
"""
modules.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
from datetime import datetime
import uuid

from mongokit import Document, IS, INDEX_GEO2D

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
            '_id':      unicode,
            'nick':     unicode,
            'password': unicode,
            'email':    unicode,
            'domain':   unicode,
            'live':     unicode,
            'created':  datetime,
            'qqid':     unicode,
            'sina_access_token':     unicode,
            'added':    dict,
            'added_id': int,
    }
    
    indexes = [
        {
            'fields':['_id', 'nick'],
            'unique':True,
        },
    ]

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
            'channel':  IS(u'normal', u'reply', u'weibo', u'map', u'keys', u'e_schedule', u'e_spend', u'e_declare', u'e_attention'),
    }
    required_fields = ['_id', 'created', 'content']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

class EventDoc(Document):
    __collection__ = 'event'
    __database__ = DB_NAME
        
    structure = {
            '_id':      unicode,
            'owner':    unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
            'logo':     unicode,
            'title':    unicode,
            'members':  dict,
            'tags':     list,
            'club':     unicode,
            'is_merc':  bool,
            'level':    float,
            'route':    unicode,
            'date':     datetime,
            'place':    unicode,
            
            'schedule_tl':  unicode,
            'spend_tl':     unicode,
            'equip':        list,
            'declare_tl':   unicode,
            'attention_tl': unicode,
            
            'deadline': datetime,
            'fr':       int,
            'to':       int,
            'when':     datetime,
            'where':    unicode,
            
            'check':    bool,
    }
    required_fields = ['_id', 'owner', 'created', 'title', 'tags', 'is_merc', 'level', 'date', 'place']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now(), 'fr':0, 'to':30}
    
    use_schemaless = True
    use_dot_notation=True

class BehaviorDoc(Document):
    __collection__ = 'behavior'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'owner':    unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
            'kind':  IS(u'like', u'join', u'follow'),
            'mark':  unicode,
    }
    required_fields = ['_id', 'created', 'kind', 'mark']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True
    
class TmpTableDoc(Document):
    __collection__ = 'tmptable'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'email':    unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
    }
    required_fields = ['_id', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

class AlertDoc(Document):
    __collection__ = 'alert'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'owner':    unicode,
            'subject':  IS(u'reply', u'join', u'follow', u'at', u'rpat'),
            'count':    int,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
    }
    required_fields = ['_id', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

class MapDoc(Document):
    __collection__ = 'map'
    __database__ = DB_NAME
    
    structure = {
            '_id':          unicode,
            'owner':        unicode,
            'location':     list,
            'points':       list,
            'subject':      IS(u'weibo', u'route', u'place'),
            'created':      datetime,
            'added':        dict,
            'added_id':     int,
    }
    indexes = [
        {
            'fields':[('location', INDEX_GEO2D)],
        },
    ]
    required_fields = ['_id', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True
    
    
    
    
    