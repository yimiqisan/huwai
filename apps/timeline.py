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
import time

from huwai.config import DB_CON, DB_NAME, DEFAULT_CUR_UID, PERM_CLASS
from modules import TimeLineDoc
from api import API, Mapping, Added_id
from huwai.apps import case
from perm import Permission

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
    
    def _flt_tpc(self, c, k):
        c = c.strip()
        t = tid = None
        if not k:k=u'weibo'
        if c.startswith('#')and(c.count('#')>1):
            l = c.split('#')
            for i in l:
                if (i!=''):t = i;break
            m = Mapping()
            r = m.do(k, t)
            if not r[0]:return r
            tid = r[1]
        return tid

    def _get_nick(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):return r[1]['added'].get('nick', None)
        return None
    
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
    
    def _fire_alert(self, channel, tid, at_list):
        c = case.get_case_object()
        if channel == u'reply':
            for at in at_list:c.fire('a_weibo_ra', to=at)
        else:
            for at in at_list:c.fire('a_weibo_at', to=at)
    
    def _fire_sina(self, owner, content):
        c = case.get_case_object()
        c.fire('s_update', uid=owner, content=content)
    
    def save(self, content, owner=None, tid=None, channel=u'normal', **kwargs):
        if tid:
            a = Added_id(tid)
            a.incr()
        else:
            kind = kwargs.get('kind', u'event')
            tid = self._flt_tpc(content, kind)
        at_list = self._flt_at(content)
        self._fire_alert(channel, tid, at_list)
        #self._fire_sina(owner, content)
        return super(TimeLineAPI, self).create(owner=owner, content=content, at_list=at_list, topic=tid, channel=channel, **kwargs)
    
    def remove(self, id):
        r = self.get(id)
        if r[0] and r[1] and (r[1]['channel'] == u'reply'):
            a = Added_id(r[1]['tid'])
            a.decr()
        return super(TimeLineAPI, self).remove(id)
    
    def _count(self, tid):
        if not tid:return 0
        a = Added_id(tid)
        c = a.count()
        return c if (c>0) else 0
    
    def _perm(self, cuid, owner):
        if cuid == owner:
            return PERM_CLASS['wFOUNDER']
        p = Permission()
        r = p._api.site_perm(cuid)
        if r:return r
        return PERM_CLASS['NORMAL']
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        now = datetime.now()
        output_map = lambda i: {'id':i['_id'], 'added_id':i['added_id'], 'owner':i['owner'], 'perm':self._perm(cuid, i['owner']), 'is_own':(cuid==i['owner'] if i['owner'] else True), 'nick':i['added'].get('nick', '匿名驴友'), 'tid':i.get('topic', None), 'content':i['content'], 'channel':i['channel'], 'count': self._count(i['_id']), 'created':self._escape_created(now, i['created'])}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1]))
        return r
    
    def get_rpat_org(self, owner=None, topic=None, channel=None, at=None):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if topic:kwargs['topic']=topic
        if at:kwargs['at_list']=at
        if channel:kwargs['channel']={'$in':channel}
        r = self.find(**kwargs)
        if r[0]:
            l = []
            for i in r[1]:
                if i['topic'] not in l:l.append(i['topic'])
            ll = []
            for i in l:
                j = self.get(i)[1]
                if j:ll.append(j)
            return (True, ll)
        else:
            return r
    
    def get_rp_org(self, owner=None, topic=None, channel=None, at=None):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if topic:kwargs['topic']=topic
        if at:kwargs['at_list']=at
        if channel:kwargs['channel']={'$in':channel}
        r = self.find(**kwargs)
        if r[0]:
            al = [i['_id'] for i in r[1]]
        else:
            return r
        r = self.find(channel={'$in':[u'reply']}, topic={'$in':al})
        if r[0]:
            l = []
            for i in r[1]:
                if i['topic'] not in l:l.append(i['topic'])
            return (True, [self.get(i)[1] for i in l])
        else:
            return r
    
    def list(self, cuid=DEFAULT_CUR_UID, owner=None, topic=None, channel=None, at=None):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if topic:kwargs['topic'] = {'$in':topic} if isinstance(topic, list) else topic
        if at:kwargs['at_list']=at
        if channel:kwargs['channel']={'$in':channel}
        r = self.find(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l)
        else:
            return (False, r[1])
    
    def extend(self, cuid=DEFAULT_CUR_UID, owner=None, topic=None, channel=None, at=None, cursor=None, limit=20, order_by='added_id', order=-1):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if topic:kwargs['topic'] = {'$in':topic} if isinstance(topic, list) else topic
        if at:kwargs['at_list']=at
        if channel:kwargs['channel']={'$in':channel}
        if cursor:kwargs['cursor']=cursor
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        r = super(TimeLineAPI, self).extend(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            added_id = min(l[0]['added_id'], l[-1]['added_id']) if len(l)!=0 else -1
            return (True, l, added_id)
        else:
            return (False, r[1])
    
    def page(self, cuid=DEFAULT_CUR_UID, owner=None, topic=None, channel=None, at=None, page=1, pglen=10, cursor=None, limit=20, order_by='added_id', order=-1):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if topic:kwargs['topic'] = {'$in':topic} if isinstance(topic, list) else topic
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
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l, r[2])
        else:
            return (False, r[1])
        
    def abbr(self, cuid=DEFAULT_CUR_UID, owner=None, topic=None, channel=None, at=None, order_by='added_id', order=-1):
        kwargs = {}
        if topic:kwargs['topic'] = {'$in':topic} if isinstance(topic, list) else topic
        if channel:kwargs['channel']={'$in':channel}
        c = super(TimeLineAPI, self).count(**kwargs)
        if c == 0:
            return (False, u'抢沙发啦', False)
        elif c == 1:
            rt = self.extend(cuid=cuid, topic=topic, channel=channel, limit=1, order=1)
            return (rt[1][0]['content'], '点击留言', False)
        elif c== 2:
            rt = self.extend(cuid=cuid, topic=topic, channel=channel, limit=2, order=1)
            return (rt[1][0]['content'], '共2条留言', rt[1][1]['content'])
        elif c>2:
            rt = self.extend(cuid=cuid, topic=topic, channel=channel, limit=1, order=1)
            rb = self.extend(cuid=cuid, topic=topic, channel=channel, limit=1, order=-1)
            return (rt[1][0]['content'], '共'+str(c)+'条留言', rb[1][0]['content'])
        else:
            return c
