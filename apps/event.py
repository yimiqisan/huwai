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

from huwai.config import DB_CON, DB_NAME, DB_SCRAPY_NAME, SITE_ID, DEFAULT_CUR_UID, CLUB_WEBSITE, PERM_CLASS
from modules import EventDoc, EventScrapyDoc
from api import API, Mapping
from behavior import Behavior
from timeline import TimeLine
from tag import Tag
from imap import Map
from perm import Permission


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
    def __init__(self, db_name=DB_NAME):
        DB_CON.register([EventDoc])
        datastore = DB_CON[db_name]
        col_name = EventDoc.__collection__
        collection = datastore[col_name]
        doc = collection.EventDoc()
        API.__init__(self, db_name=db_name, col_name=col_name, collection=collection, doc=doc)
    
    def _tl_save(self, content, owner, tid, channel, **kwargs):
        tl = TimeLine()
        return tl._api.save(content, owner=owner, tid=tid, channel=channel, **kwargs)
    
    def _tl_get(self, id=None):
        if not id:return ''
        tl = TimeLine()
        r = tl._api.get(id)
        if (r[0] and r[1]):return r[1]['content']
        return ''
    
    def _map_save(self, id, owner, place, **kwargs):
        try:
            place = list(eval(place))
        except:
            return place
        m = Map()
        r = m._api.save(owner, u'collect', location=place, link=id, **kwargs)
        if r[0] and r[1]:
            return r[1]
        else:
            return place
    
    def _get_tid(self, t):
        m = Mapping()
        r = m.do(u'event', t)
        return r[1] if r[0] else r
    
    def save_step_one(self, owner, logo, title, tags, is_merc, level, date, day, place, schedule_tl, nick=None, members=None, club=None, route=None, spend_tl=None, equip=None, declare_tl=None, attention_tl=None):
        kwargs = {}
        if nick:kwargs['nick']=nick
        if members:kwargs['members']=members
        kwargs['club']=club if club else SITE_ID
        if route:kwargs['route']=route
        if equip:kwargs['equip']=equip
        r = super(EventAPI, self).create(owner=owner, logo=logo, title=title, tags=tags, is_merc=is_merc, level=level, date=date, day=int(day), place=place, **kwargs)
        if r[0]:self.after_step_one(r[1], title, schedule_tl=schedule_tl, spend_tl=spend_tl, declare_tl=declare_tl, attention_tl=attention_tl)
        return r
    
    def after_step_one(self, id, title, schedule_tl=None, spend_tl=None, declare_tl=None, attention_tl=None, **kwargs):
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
    
    def save_step_two(self, id, owner, deadline, fr, to, when, where, **kwargs):
        where = self._map_save(id, owner, where)
        return self.edit(id, deadline=deadline, fr=fr, to=to, when=when, where=where, check=False, **kwargs)
    
    def check(self, id, check, message=None):
        return self.edit(id, check=check)
    
    def _is_joined(self, eid, cuid=DEFAULT_CUR_UID):
        b = Behavior()
        r = b._api.list(owner=cuid, channel=u'approval', she=eid)
        return (len(r)>0)
    
    def _perm(self, eid, cuid, owner, members):
        p = Permission()
        r = p._api.site_perm(cuid)
        if r:
            return r
        if cuid == owner:
            return PERM_CLASS['eSPONSOR']
        elif cuid in members.values():
            return PERM_CLASS['eASSISTANT']
        b = Behavior()
        r = b._api.list(owner=cuid, channel=u'approval', she=eid)
        if len(r)>0:
            return PERM_CLASS['ePARICIPANT']
        else:
            return PERM_CLASS['NORMAL']
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        now = datetime.now()
        if cuid is None:cuid = DEFAULT_CUR_UID
        merc_f = lambda x: u'商业性质' if x else u'非商业性质'
        club_f = lambda x: u'公开' if x==u'site' else u'xx俱乐部'
        t = Tag()
        output_map = lambda i: {'id':i['_id'], 'owner':i['owner'], 'tid':i['added'].get('tid', None), 'perm':self._perm(i['_id'], cuid, i['owner'], i['members']), 'is_join':self._is_joined(i['_id'], cuid), 'nick':i['added'].get('nick', '匿名驴友'), 'created':i['created'].strftime('%Y-%m-%d %H:%M:%S'), 'logo':i['logo'], 'title':i['title'], 'members':i['members'], 'tags':t._api.id2content(i['tags']), 'club':club_f(i['club']), 'is_merc':merc_f(i['is_merc']), 'level':i['level'], 'route':i['route'], 'place':i['place'], 'date':self._escape_date(now, i['date']), 'schedule_tl':self._tl_get(i['schedule_tl']), 'spend_tl':self._tl_get(i['spend_tl']), 'equip':t._api.id2content(i['equip']), 'declare_tl':self._tl_get(i['declare_tl']), 'attention_tl':self._tl_get(i['attention_tl']), 'deadline':self._escape_date(now, i['deadline']), 'fr':i['fr'], 'to':i['to'], 'when':self._escape_year(now, i['when']), 'where':i['where'], 'check':i['check']}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id, cuid=DEFAULT_CUR_UID):
        r = self.one(_id=id)
        if r[0]:return (True, self._output_format(result=r[1], cuid=cuid))
        return r
    
    def list(self, owner=None, tags=None, cuid=DEFAULT_CUR_UID, club=None, is_merc=None, level=None, date=None, place=None, deadline=None, fr=None, to=None, when=None, check=None):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if tags:kwargs['tags']={'$all':tags} if isinstance(tags, list) else tags
        if club:kwargs['club']=club
        if is_merc:kwargs['is_merc']=is_merc
        if level:kwargs['level']={'in':level}
        if date:kwargs['date']=date
        if place:kwargs['place']=place
        if deadline:kwargs['deadline']={'$gt':deadline}
        if fr:kwargs['fr']={'$gt':fr}
        if to:kwargs['to']={'$gt':to}
        if when:kwargs['when']={'$gt':when}
        if isinstance(check, bool):kwargs['check'] = check
        r = self.find(**kwargs)
        if r[0]:
            return (True, self._output_format(result=r[1], cuid=cuid))
        else:
            return (False, r[1])
    
    def extend(self):
        return super(EventAPI, self).extend()
    
    def page(self, owner=None, tags=None, cuid=DEFAULT_CUR_UID, club=None, is_merc=None, level=None, date=None, place=None, deadline=None, fr=None, to=None, when=None, check=None, page=1, pglen=10, cursor=None, limit=20, order_by='added_id', order=-1):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if tags:kwargs['tags']={'$all':tags} if isinstance(tags, list) else tags
        if club:kwargs['club']=club
        if is_merc:kwargs['is_merc']=is_merc
        if level:kwargs['level']={'in':level}
        if date:kwargs['date']=date
        if place:kwargs['place']=place
        if deadline:kwargs['deadline']={'$gt':deadline}
        if fr:kwargs['fr']={'$gt':fr}
        if to:kwargs['to']={'$gt':to}
        if when:kwargs['when']={'$gt':when}
        if isinstance(check, bool):kwargs['check'] = check
        kwargs['page']=page
        kwargs['pglen']=pglen
        if cursor:kwargs['cursor']=cursor
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        r = super(EventAPI, self).page(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l, r[2])
        else:
            return (False, r[1])

class EventScrapyAPI(API):
    def __init__(self, db_name=DB_SCRAPY_NAME):
        DB_CON.register([EventScrapyDoc])
        datastore = DB_CON[db_name]
        col_name = EventScrapyDoc.__collection__
        collection = datastore[col_name]
        doc = collection.EventScrapyDoc()
        API.__init__(self, db_name=db_name, col_name=col_name, collection=collection, doc=doc)
    
    def _pre_save(self, eid, club):
        r = self.one(eid=eid, club=club)
        return r[1] is not None
    
    def save(self, owner, club, eid, logo, title, tags=None, date=None, day=1, place=None, href=None, deadline=None, created=None, nick=None, **kwargs):
        if self._pre_save(eid, club): return (True, None)
        if tags:tags = tags if isinstance(tags, list) else [tags]
        return super(EventScrapyAPI, self).create(owner=owner, eid=eid, club=club, logo=logo, title=title, tags=tags, date=date, day=day, place=place, href=href, deadline=deadline, created=created, nick=nick, **kwargs)
    
    def check(self, id, check, message=None):
        return self.edit(id, check=check)
    
    def _output_format(self, result=[]):
        now = datetime.now()
        output_map = lambda i: {'id':i['_id'], 'tid':i['_id'], 'owner':i['owner'], 'href':i['href'], 'club':i['club'], 'nick':i.get('nick', '匿名驴友'), 'created':i['created'].strftime('%Y-%m-%d %H:%M:%S'), 'logo':i['logo'], 'title':i['title'], 'tags':i['tags'], 'place':i['place'], 'date':self._escape_date(now, i['date']), 'deadline':self._escape_date(now, i['deadline'])}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id, cuid=DEFAULT_CUR_UID):
        r = self.one(_id=id)
        if r[0]:return (True, self._output_format(result=r[1]))
        return r
    
    def list(self, owner=None, club=None, tags=None, date=None, place=None, deadline=None, check=True):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if club:kwargs['club']=club
        if tags:kwargs['tags']={'$all':tags} if isinstance(tags, list) else tags
        if date:kwargs['date']=date
        if place:kwargs['place']=place
        if deadline:kwargs['deadline']={'$gt':deadline}
        #kwargs['check']=check
        r = self.find(**kwargs)
        if r[0]:
            return (True, self._output_format(result=r[1]))
        else:
            return (False, r[1])
    
    def page(self, owner=None, club=None, tags=None, date=None, place=None, deadline=None, check=True, page=1, pglen=10, cursor=None, limit=20, order_by='added_id', order=-1):
        pass