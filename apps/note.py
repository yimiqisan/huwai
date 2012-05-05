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
import re

from huwai.config import DB_CON, DB_NAME, DEFAULT_CUR_UID, PERM_CLASS
from modules import NoteDoc
from api import API, Mapping
from tag import Tag
from perm import Permission

class Note(object):
    def __init__(self, api=None):
        self._api = NoteAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None

class NoteAPI(API):
    def __init__(self):
        DB_CON.register([NoteDoc])
        datastore = DB_CON[DB_NAME]
        col_name = NoteDoc.__collection__
        collection = datastore[col_name]
        doc = collection.NoteDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def _get_tid(self, t):
        m = Mapping()
        r = m.do(u'note', t)
        return r[1] if r[0] else r
    
    def save(self, owner, title, content, tags=[], members=[], check=False, **kwargs):
        tid = self._get_tid(title)
        kwargs['tid'] = tid
        if not isinstance(tags, list):tags = [tags]
        if not isinstance(members, list):members = [members]
        return super(NoteAPI, self).create(owner=owner, title=title, content=content, tags=tags, members=members, check=check, channel=u'origin', **kwargs)
    
    def _clue_id(self, cid):
        rid = cid
        while(cid):
            r = self.one(_id=cid)
            if r[0] and r[1]:
                pid = r[1]['pid']
                rid = r[1]['_id']
                if pid:
                    cid = pid
                else:
                    break
            else:
                break
        return rid
    
    def append(self, id, owner, title, content, tags=[], members=[], check=False, **kwargs):
        tid = self._get_tid(title)
        kwargs['tid'] = tid
        if not isinstance(tags, list):tags = [tags]
        if not isinstance(members, list):members = [members]
        r = super(NoteAPI, self).create(owner=owner, title=title, content=content, tags=tags, members=members, check=check, channel=u'append', **kwargs)
        cid = self._clue_id(id)
        if r[0]: self.edit(cid, pid=r[1])
        return r
    
    def remove(self, id, cuid=DEFAULT_CUR_UID):
        r = self.get(id, cuid)
        if (r[0] and r[1]) and r[1]['is_own']:
            pid = r[1].get('pid', None)
            if r[1]['channel'] == u'origin':
                if pid:self.edit(pid, channel=u'origin')
            elif r[1]['channel'] == u'append':
                ra=self.one(pid=r[1]['id'])
                if ra[0] and ra[1]:
                    self.edit(ra[1]['_id'], pid=r[1]['pid'])
            return super(NoteAPI, self).remove(id)
        return None
    
    def edit(self, id, title=None, content=None, tags=None, members=None, **kwargs):
        if title:kwargs['title'] = title
        if content:kwargs['content'] = content
        if tags:kwargs['tags'] = tags
        if members:kwargs['members'] = members
        return super(NoteAPI, self).edit(id, **kwargs)
    
    def _perm(self, cuid, owner):
        if cuid == owner:
            return PERM_CLASS['nFOUNDER']
        p = Permission()
        r = p._api.site_perm(cuid)
        if r:return r
        return PERM_CLASS['NORMAL']
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        now = datetime.now()
        t = Tag()
        output_map = lambda i: {'id':i['_id'], 'owner':i['owner'], 'tid':i['added'].get('tid', None), 'perm':self._perm(cuid, i['owner']), 'is_own':(cuid==i['owner'] if i['owner'] else True), 'nick':i['added'].get('nick', ''), 'pid':i['pid'], 'added_id':i['added_id'], 'title':i['title'], 'content':i['content'], 'channel':i['channel'],'tags':t._api.id2content(i['tags']), 'members':i.get('members', []), 'created':self._escape_created(now, i['created']), 'check':i.get('check', True)}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id, cuid=DEFAULT_CUR_UID):
        r = self.one(_id=id)
        if (r[0] and r[1]):
            return (True, self._output_format(result=r[1], cuid=cuid))
    
    def get_list(self, id, cuid=DEFAULT_CUR_UID):
        l = []
        r = self.one(_id=id)
        if (r[0] and r[1]):
            out = self._output_format(result=r[1], cuid=cuid)
            l.append(out)
        if out['channel'] == u'append':return (True, l)
        while (out['pid']):
            r = self.one(_id=out['pid'])
            if (r[0] and r[1]):
                out = self._output_format(result=r[1], cuid=cuid)
                l.append(out)
            else:
                break
        return (True, l)
    
    def list(self, cuid=DEFAULT_CUR_UID, owner=None, title=None, content=None, tags=None, members=None, channel=None, check=None):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if title:kwargs['title']=re.compile('.*'+title+'.*')
        if content:kwargs['content']=re.compile('.*'+content+'.*')
        if tags:kwargs['tags'] = {'$all':tags} if isinstance(tags, list) else tags
        if members:kwargs['members'] = {'$all':members} if isinstance(members, list) else members
        if channel:kwargs['channel']=channel
        if check:kwargs['check']=check
        r = self.find(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l)
        else:
            return (False, r[1])
    
    def page(self, cuid=DEFAULT_CUR_UID, owner=None, title=None, content=None, tags=None, members=None, channel=None, check=None, page=1, pglen=10, cursor=None, limit=20, order_by='added_id', order=-1):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if title:kwargs['title']=re.compile('.*'+title+'.*')
        if content:kwargs['content']=re.compile('.*'+content+'.*')
        if tags:kwargs['tags'] = {'$all':tags} if isinstance(tags, list) else tags
        if members:kwargs['members'] = {'$all':members} if isinstance(members, list) else members
        if channel:kwargs['channel']=channel
        if check:kwargs['check']=check
        kwargs['page']=page
        kwargs['pglen']=pglen
        if cursor:kwargs['cursor']=cursor
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        r = super(NoteAPI, self).page(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l, r[2])
        else:
            return (False, r[1])
    
    
    
    
    
    
    
    
    
    
    
    
    
    