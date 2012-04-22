#!/usr/bin/env python
# encoding: utf-8
"""
album.py

Created by 刘 智勇 on 2012-03-22.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
from datetime import datetime
import re

from huwai.config import DB_CON, DB_NAME, DEFAULT_CUR_UID
from modules import AlbumDoc
from api import API
from perm import Permission

ALLOWED_ALL = 0x01
ALLOWED_FOLLOW = 0x02
ALLOWED_SELF = 0x03

class Album(object):
    def __init__(self, api=None):
        self._api = AlbumAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None

class AlbumAPI(API):
    def __init__(self):
        DB_CON.register([AlbumDoc])
        datastore = DB_CON[DB_NAME]
        col_name = AlbumDoc.__collection__
        collection = datastore[col_name]
        doc = collection.AlbumDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def build(self, owner, title, content, relation=None, tags=[], allowed=ALLOWED_ALL, photos=[], **kwargs):
        return super(AlbumAPI, self).create(owner=owner, title=title, content=content, relation=relation, tags=tags, allowed=allowed, photos=photos, **kwargs)
    
    def remove(self, id):
        return super(AlbumAPI, self).remove(id)
    
    def modify(self, id, title=None, content=None, relation=None, tags=None, allowed=None):
        if title:kwargs['title'] = title
        if content:kwargs['content'] = content
        if relation:kwargs['relation'] = relation
        if tags:kwargs['tags'] = tags
        if allowed:kwargs['allowed'] = allowed
        return super(AlbumAPI, self).edit(id, **kwargs)
    
    def push(self, id, pid):
        return super(AlbumAPI, self).edit(id, photos=pid)
    
    def pop(self, aid, pid):
        pass
    
    def _perm(self, cuid, owner):
        if cuid == owner:
            return PERM_CLASS['wFOUNDER']
        p = Permission()
        r = p._api.site_perm(cuid)
        if r:return r
        return PERM_CLASS['NORMAL']
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        now = datetime.now()
        output_map = lambda i: {'id':i['_id'], 'added_id':i['added_id'], 'owner':i['owner'], 'perm':self._perm(cuid, i['owner']), 'nick':i['added'].get('nick', '匿名驴友'), 'title':i.get('title', None), 'content':i['content'], 'relation':i['relation'], 'tags': i['tags'], 'allowed':i['allowed'], 'photos':i['photos'], 'created':self._escape_created(now, i['created'])}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1]))
        return r
    
    def list(self, cuid=DEFAULT_CUR_UID, owner=None, relation=None, tags=None, allowed=None):
        kwargs = {}
        if owner:kwargs['owner']= owner
        if relation:kwargs['relation']= relation
        if tags:kwargs['tags']={'$in':tags} if isinstance(tags, list) else tags
        if allowed:kwargs['allowed']= allowed
        r = self.find(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l)
        else:
            return (False, r[1])
    
    def page(self, cuid=DEFAULT_CUR_UID, owner=None, relation=None, tags=None, allowed=None, page=1, pglen=10, cursor=None, limit=20, order_by='added_id', order=-1):
        kwargs = {}
        if owner:kwargs['owner']= owner
        if relation:kwargs['relation']= relation
        if tags:kwargs['tags']={'$in':tags} if isinstance(tags, list) else tags
        if allowed:kwargs['allowed']= allowed
        kwargs['page']=page
        kwargs['pglen']=pglen
        if cursor:kwargs['cursor']=cursor
        kwargs['limit']=limit
        kwargs['order_by']=order_by
        kwargs['order']=order
        r = super(AlbumAPI, self).page(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l, r[2])
        else:
            return (False, r[1])
