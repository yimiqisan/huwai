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


class TimeLineDoc(Document):
    __collection__ = 'timeline'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'owner':    unicode,
            'column': unicode,
            'subject':  unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': unicode,
            'content':  unicode,
            'at_list':  list,
    }
    
    required_fields = ['_id', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.utcnow}
    
    use_schemaless = True
    use_dot_notation=True

