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
from api import API, Mapping
from behavior import Behavior
from timeline import TimeLine


class Event(object):
    def __init__(self, id=None, api=None):
        self._api = api if api else EventAPI()
        if id:
            ret = self._api.one(_id=id)
            self.info, self.eid = (ret[1], ret[1]['_id']) if ret[0] else (None, None)
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None
    
    def whichis(self, id):
        ret = self._api.one(_id=id)
        if ret[0]:
            self.info = ret[1]
            self.eid = self.info['_id']
        else:
            self.eid = self.info = None
    
    def show(self, id=None):
        if id:self.whichis(id)
        return 
    
class EventAPI(API):
    def __init__(self):
        DB_CON.register([EventDoc])
        datastore = DB_CON[DB_NAME]
        col_name = EventDoc.__collection__
        collection = datastore[col_name]
        doc = collection.EventDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def _tl_save(self, content, owner, tid, channel, **kwargs):
        tl = TimeLine()
        return tl._api.save(content, owner=owner, tid=tid, channel=channel, **kwargs)
    
    def _tl_get(self, id=None):
        if not id:return ''
        tl = TimeLine()
        r = tl._api.get(id)
        if (r[0] and r[1]):return r[1]['content']
        return ''
    
    def _get_tid(self, t):
        m = Mapping()
        r = m.do(t)
        return r[1] if r[0] else r
    
    def save_step_one(self, owner, logo, title, tags, is_merc, level, date, place, schedule_tl, nick=None, members=None, club=None, route=None, spend_tl=None, equip=None, declare_tl=None, attention_tl=None):
        kwargs = {}
        if nick:kwargs['nick']=nick
        if members:kwargs['members']=members
        kwargs['club']=club if club else SITE_ID
        if route:kwargs['route']=route
        if equip:kwargs['equip']=equip
        r = super(EventAPI, self).create(owner=owner, logo=logo, title=title, tags=tags, is_merc=is_merc, level=level, place=place, date=date, **kwargs)
        if r[0]:self.after_step_one(r[1], title, schedule_tl=schedule_tl, spend_tl=spend_tl, declare_tl=declare_tl, attention_tl=attention_tl)
        return r
    
    def after_step_one(self, id, title, schedule_tl=None, spend_tl=None, declare_tl=None, attention_tl=None):
        kwargs = {}
        tid = self._get_tid(title)
        kwargs['tid']=tid
        if schedule_tl:
            r=self._tl_save(schedule_tl, id, tid, u'e_schedule')
            if r[0]:kwargs['schedule_tl']=r[1]
        if spend_tl:
            r=self._tl_save(spend_tl, id, tid, u'e_spend')
            if r[0]:kwargs['spend_tl']=r[1]
        if declare_tl:
            r=self._tl_save(declare_tl, id, tid, u'e_declare')
            if r[0]:kwargs['declare_tl']=r[1]
        if attention_tl:
            r=self._tl_save(attention_tl, id, tid, u'e_attention')
            if r[0]:kwargs['attention_tl']=r[1]
        self.edit(id, **kwargs)
    
    def save_step_two(self, id, deadline, fr, to, when, where, **kwargs):
        return self.edit(id, deadline=deadline, fr=fr, to=to, when=when, where=where, check=False, **kwargs)
    
    def check(self, id, check, message=None):
        return self.edit(id, check=check)
    
    def _is_joined(self, cuid, eid):
        b = Behavior()
        r = b._api.one(owner=cuid, kind=u'join', mark=eid)
        return (r[0] and r[1])
    
    def _output_format(self, owner=None, result=[]):
        merc_f = lambda x: u'商业性质' if x else u'非商业性质'
        output_map = lambda i: {'id':i['_id'], 'owner':i['owner'], 'tid':i['added']['tid'], 'is_join':self._is_joined(i['owner'], i['_id']), 'nick':i['added'].get('nick', '匿名驴友'), 'created':i['created'], 'logo':i['logo'], 'title':i['title'], 'members':i['members'], 'tags':i['tags'], 'club':i['club'], 'is_merc':merc_f(i['is_merc']), 'level':i['level'], 'route':i['route'], 'place':i['place'], 'date':i['date'], 'schedule_tl':self._tl_get(i['schedule_tl']), 'spend_tl':self._tl_get(i['spend_tl']), 'equip':i['equip'], 'declare_tl':self._tl_get(i['declare_tl']), 'attention_tl':self._tl_get(i['attention_tl']), 'deadline':i['deadline'], 'fr':i['fr'], 'to':i['to'], 'when':i['when'], 'where':i['where']}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        r = self.one(_id=id)
        if r[0]:return (True, self._output_format(result=r[1]))
        return r
    
    def list(self, owner=None, tags=None, club=None, is_merc=None, level=None, date=None, place=None, deadline=None, fr=None, to=None, when=None, check=True):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if tags:kwargs['tags']={'in':tags}
        if club:kwargs['club']=club
        if is_merc:kwargs['is_merc']=is_merc
        if level:kwargs['level']={'in':level}
        if date:kwargs['date']=date
        if place:kwargs['place']=place
        if deadline:kwargs['deadline']={'$gt':deadline}
        if fr:kwargs['fr']={'$gt':fr}
        if to:kwargs['to']={'$gt':to}
        if when:kwargs['when']={'$gt':when}
        kwargs['check']=check
        r = self.find(**kwargs)
        if r[0]:
            return (True, self._output_format(result=r[1]))
        else:
            return (False, r[1])

    def extend(self):
        return super(EventAPI, self).extend()
    
    def page(self):
        return super(EventAPI, self).page()
    
