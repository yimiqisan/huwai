#!/usr/bin/env python
# encoding: utf-8
"""
api.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime

from huwai.config import DB_CON, DB_NAME
from modules import TimeLineDoc
from api import API

class TimeLine(object):
    def __init__(self, api=None):
        self._api = TimeLineAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None


class TimeLineAPI(API):
    def __init__(self):
        DB_CON.register([TimeLineDoc])
        datastore = DB_CON[DB_NAME]
        col_name = TimeLineDoc.__collection__
        collection = datastore[col_name]
        doc = collection.TimeLineDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def _flt_tpc(self, c):
        c = c.strip()
        t = tid = None
        if c.startswith('#')and(c.count('#')>1):
            l = c.split('#')
            for i in l:
                if (i!=''):t = i;break
            m = Mapping()
            r = m.do(t)
            if not r[0]:return r
            tid = r[1]
        return tid
    
    def _flt_at(self, c):
        l = c.split(u' ')
        at_l = []
        for i in l:
            if i.count('@')==1:
                s = i.find('@')+1
                at_l.append(i[s:])
            elif i.count('@')>1:
                s = i.find('@')+1
                t_l = i[s:].split('@')
                at_l.extend(t_l)
        return list(set(at_l))
    
    def save(self, content, owner=None, tid=None, channel=u'normal', **kwargs):
        if tid is None:tid = self._flt_tpc(content)
        at_list = self._flt_at(content)
        return super(TimeLineAPI, self).create(owner=owner, content=content, at_list=at_list, topic=tid, channel=channel, **kwargs)
    
    def list(self, owner=None, topic=None, channel=None, at=None):
        kwargs = {}
        if owner:kwargs['owner']=owner
#        if topic:kwargs['topic']=topic
        if at:kwargs['at_list']=at
        if channel:kwargs['channel']=channel#{'$in':channel}
        r = self.find(**kwargs)
        if r[0]:
            l = [{'id':i['_id'], 'nick':i['added'].get('nick', '匿名驴友'), 'content':i['content'], 'created':i['created'].strftime('%Y-%m-%d %X')} for i in r[1]]
            return (True, l)
        else:
            return (False, r[1])
    
    def extend(self, owner=None, topic=None, channel=None, at=None, cursor=None, limit=20, order_by='added_id', order=-1):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if topic:kwargs['topic']=topic
        if at:kwargs['at_list']=at
        if channel:kwargs['channel']={'$in':channel}
        if cursor:kwargs['cursor']=cursor
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        r = super(TimeLineAPI, self).extend(**kwargs)
        if r[0]:
            l = [{'id':i['_id'], 'nick':i['added'].get('nick', '匿名驴友'), 'content':i['content'], 'created':i['created'].strftime('%Y-%m-%d %X')} for i in r[1]]
            return (True, l)
        else:
            return (False, r[1])
    
    def page(self, owner=None, topic=None, channel=None, at=None, page=1, pglen=10, cursor=None, limit=20, order_by='added_id', order=-1):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if topic:kwargs['topic']=topic
        if at:kwargs['at_list']=at
        if channel:kwargs['channel']={'$in':channel}
        kwargs['page']=page
        kwargs['pglen']=pglen
        if cursor:kwargs['cursor']=cursor
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        r = super(TimeLineAPI, self).page(**kwargs)
        if r[0]:
            l = [{'id':i['_id'], 'nick':i['added'].get('nick', '匿名驴友'), 'content':i['content'], 'created':i['created'].strftime('%Y-%m-%d %X')} for i in r[1]]
            return (True, l, r[2])
        else:
            return (False, r[1])
        
        
