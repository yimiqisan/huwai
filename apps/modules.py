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

class UserDoc(Document):
    __collection__ = 'people'
    __database__ = DB_NAME

    structure = {
            '_id': unicode,
            'nick': unicode,
            'password':unicode,
            'email':unicode,
            'created':datetime,
            'added':dict,
            'added_id':unicode,
    }
    required_fields = ['_id', 'nick', 'password', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.utcnow}
    
    use_schemaless = True
    use_dot_notation=True


class SNSLineDoc(Document):
    __collection__ = 'sns_tl'
    __database__ = DB_NAME

    structure = {
            '_id': unicode,
            'said': unicode,
            'to': list,
            'about': unicode,
            'created':datetime,
            'o':unicode,    #owner
            't':IS(u'reply', u'quote', u'share'),   #type
            'c':IS(u'weibo', u'event', u'know', u'map', u'circle'), #column
            'added':dict,
            'added_id':unicode,
    }
    required_fields = ['_id',  'created', 'o', 't', 'c']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.utcnow, 't':u'reply'}
    
    use_schemaless = True
    use_dot_notation=True

class MediaLineDoc(Document):
    __collection__ = 'media_tl'
    __database__ = DB_NAME

    structure = {
            '_id': unicode,
            'said': unicode,
            'to': list,
            'about': unicode,
            'created':datetime,
            'o':unicode,    #owner
            't':IS(u'words', u'map', u'music', u'video', u'picture', u'href'),  #type
            'c':IS(u'weibo', u'event', u'know', u'map', u'circle'), #column
            'added':dict,
            'added_id':unicode,
    }
    required_fields = ['_id', 'created', 'o', 't', 'c']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.utcnow, 't':u'words'}
    
    use_schemaless = True
    use_dot_notation=True
    
    
class UserLineDoc(Document):
    __collection__ = 'user_tl'
    __database__ = DB_NAME

    structure = {
            '_id': unicode,
            'channel': IS(u'origin', u'sns'),
            'said': unicode,
            'to': list,
            'about': unicode,
            'created':datetime,
            'o':unicode,    #owner
            't':unicode,    #type
            'c':unicode,    #column
            'added':dict,
            'added_id':unicode,
    }
    required_fields = ['_id',  'created', 'o', 't', 'c']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.utcnow}
    
    use_schemaless = True
    use_dot_notation=True
