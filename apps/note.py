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
        kwargs['tid'] = self._get_tid(title)
        if not isinstance(tags, list):tags = [tags]
        if not isinstance(members, list):members = [members]
        return super(NoteAPI, self).create(owner=owner, title=title, content=content, tags=tags, members=members, check=check, **kwargs)
    
    def remove(self, id):
        return super(NoteAPI, self).remove(id)
    
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
        output_map = lambda i: {'id':i['_id'], 'owner':i['owner'], 'tid':i['added'].get('tid', None), 'perm':self._perm(cuid, i['owner']), 'is_own':(cuid==i['owner'] if i['owner'] else True), 'added_id':i['added_id'], 'title':i['title'], 'content':i['content'], 'tags':t._api.id2content(i['tags']), 'members':i.get('members', []), 'created':i['created'].strftime('%Y-%m-%d %H:%M'), 'check':i.get('check', True)}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id, cuid=DEFAULT_CUR_UID):
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1], cuid=cuid))
        return r
    
    def list(self, cuid=DEFAULT_CUR_UID, owner=None, title=None, content=None, tags=None, members=None, check=None):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if title:kwargs['title']=re.compile('.*'+title+'.*')
        if content:kwargs['content']=re.compile('.*'+content+'.*')
        if tags:kwargs['tags'] = {'$all':tags} if isinstance(tags, list) else tags
        if members:kwargs['members'] = {'$all':members} if isinstance(members, list) else members
        if check:kwargs['check']=check
        r = self.find(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l)
        else:
            return (False, r[1])

    
    
    
    
    
    
    
    
    
    
    
    
    
    