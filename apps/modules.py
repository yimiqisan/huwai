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

from huwai.config import DB_NAME, DB_SCRAPY_NAME, SITE_ID

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
            '_id':      unicode,
            'channel':  IS(u'event', u'note'),
            'image':    unicode,
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

class PermissionDoc(Document):
    __collection__ = 'permission'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'owner':    unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
            'channel':  IS(u'site', u'club', u'event'),
            'cid':      unicode,
            'value':    int,
    }
    required_fields = ['_id', 'created']
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
            'channel':  IS(u'normal', u'reply', u'weibo', u'club', u'event', u'album', u'map', u'keys', u'e_schedule', u'e_spend', u'e_declare', u'e_attention'),
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
            'day':      int,
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
    required_fields = ['_id', 'owner', 'created', 'title', 'tags', 'date']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now(), 'fr':0, 'to':30, 'date':datetime.now(), 'deadline':datetime.now(), 'when':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

class EventScrapyDoc(Document):
    __collection__ = 'eventscrapy'
    __database__ = DB_SCRAPY_NAME
        
    structure = {
            '_id':      unicode,
            'owner':    unicode,
            'eid':      unicode,
            'club':     unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
            
            'logo':     unicode,
            'title':    unicode,
            'tags':     list,
            'date':     datetime,
            'day':      int,
            'place':    unicode,
            'href':     unicode,
            'nick':     unicode,
            
            'deadline': datetime,
            'check':    bool,
    }
    required_fields = ['_id', 'owner', 'created', 'title', 'date']
    default_values = {'_id':uuid.uuid4().hex, 'owner': SITE_ID, 'created':datetime.now(), 'date':datetime.now(), 'deadline':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True

class NoteDoc(Document):
    __collection__ = 'note'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'owner':    unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
            'title':    unicode,
            'content':  unicode,
            'tags':     list,
            'members':  list,
            'pid':      unicode,
            'channel':  IS(u'origin', u'append'),
            'check':    bool,
    }
    required_fields = ['_id', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
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
            'she':      unicode,
            'channel':  IS(u'approval', u'attention'),
            'switch':   bool,
    }
    required_fields = ['_id', 'created', 'owner', 'she']
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
            'subject':  IS(u'weibo_at', u'weibo_ra', u'weibo_fl', u'account_ml', u'account_pw', u'account_iv', u'event_ckfb', u'event_jnfb', u'event_ckps', u'event_jnps', u'event_jncf'),
            'nature':   IS(u'alert', u'error', u'success', u'confirm'),
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
            'subject':      IS(u'weibo', u'route', u'place', u'collect'),
            'location':     list,
            'polyline':     unicode,
            'link':         unicode,
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

class RoleDoc(Document):
    __collection__ = 'role'
    __database__ = DB_NAME
    
    structure = {
            '_id':          unicode,
            'user':         unicode,
            'subject':      IS(u'site', u'club', u'event', u'album', u'weibo'),
            'xid':          unicode,
            'created':      datetime,
            'added':        dict,
            'added_id':     int,
    }
    required_fields = ['_id', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True
    
class TagDoc(Document):
    __collection__ = 'tag'
    __database__ = DB_NAME
    
    structure = {
            '_id':          unicode,
            'owner':        unicode,
            'content':      unicode,
            'relation_l':   list,
            'created':      datetime,
            'added':        dict,
            'added_id':     int,
    }
    required_fields = ['_id', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True
    
class AlbumDoc(Document):
    __collection__ = 'album'
    __database__ = DB_NAME
    
    structure = {
            '_id':          unicode,
            'owner':        unicode,
            'title':        unicode,
            'content':      unicode,
            'relation':     unicode,
            'tags':         list,
            'allowed':      int,
            'photos':       list,
            'created':      datetime,
            'added':        dict,
            'added_id':     int,
    }
    required_fields = ['_id', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True
    
class GuideDoc(Document):
    __collection__ = 'guide'
    __database__ = DB_NAME
    
    structure = {
            '_id':          unicode,
            'owner':        unicode,
            'created':      datetime,
            'added':        dict,
            'added_id':     int,
            'title':        unicode,
            'href':         unicode,
            'image':        unicode,
            'tags':         list,
            'price':        float,
    }
    required_fields = ['_id', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True
    
    
    
    
    