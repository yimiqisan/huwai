#!/usr/bin/env python
# encoding: utf-8
"""
event.py

Created by 刘 智勇 on 2011-12-20.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime
import time

from huwai.config import DB_CON, DB_NAME, SITE_ID
from modules import EventDoc
from api import API
from behavior import Behavior

class Event(object):
    def __init__(self, id=None, api=None):
        self._api = api if api else EventAPI()
        if id:
            ret = self._api.one(_id=id)
            self.info, self.eid = ret, ret['_id'] if ret else None, None
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None
    
    def whichis(self, id):
        ret = self._api.one(_id=id)
        if ret:
            self.info = ret
            self.eid = self.info['_id']
        else:
            self.eid = self.info = None
    
    def show(self, id=None):
        if id:self.whichis(id)
        return 
    
    def approve_toggle(self, uid, **kwargs):
        b = Behavior()
        r = b._api.state(uid, u'join', self.eid)
        if r[0]:
            id = r[1]['_id']
            kwargs['pass'] = not r[1]['added'].get('pass', False)
            return b._api.edit(id, **kwargs)
        else:
            return (False, 'not exist')

class EventAPI(API):
    def __init__(self):
        DB_CON.register([EventDoc])
        datastore = DB_CON[DB_NAME]
        col_name = EventDoc.__collection__
        collection = datastore[col_name]
        doc = collection.EventDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def save_step_one(self, owner, logo, title, tags, is_merc, level, date, place, schedule_tl, club=None, route=None, spend_tl=None, equip=None, declare_tl=None, attention_tl=None):
        kwargs = {}
        kwargs['club']=club if club else SITE_ID
        if not route:kwargs['route']=route
        if not spend_tl:kwargs['spend_tl']=spend_tl
        if not equip:kwargs['equip']=equip
        if not declare_tl:kwargs['declare_tl']=declare_tl
        if not attention_tl:kwargs['attention_tl']=attention_tl
        return super(EventAPI, self).create(owner=owner, title=title, tags=tags, kind=kind, route=route, date=date, place=place, schedule_tl=schedule_tl, **kwargs)
    
    def save_step_two(self, id, deadline, fr, to, when, where, **linkway):
        self.edit(id, deadline=deadline, fr=fr, to=to, when=when, where=where, **linkway)
    
    def check(self, result, message=None):
        pass
    
    def list(self):
        pass
    
    def extend(self):
        pass
    
    def page(self):
        pass
    
    




