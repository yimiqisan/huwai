#!/usr/bin/env python
# encoding: utf-8
"""
wiki.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime
import time

from huwai.config import DB_CON, DB_NAME, DEFAULT_CUR_UID, PERM_CLASS
from modules import WikiDoc, WikiSectionDoc
from api import API
from perm import Permission

class Wiki(object):
    def __init__(self, api=None):
        self._api = WikiAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None

class WikiAPI(API):
    def __init__(self):
        DB_CON.register([WikiDoc])
        datastore = DB_CON[DB_NAME]
        col_name = WikiDoc.__collection__
        collection = datastore[col_name]
        doc = collection.WikiDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)


class WikiSection(object):
    def __init__(self, api=None):
        self._api = WikiSectionAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None

class WikiSectionAPI(API):
    def __init__(self):
        DB_CON.register([WikiSectionDoc])
        datastore = DB_CON[DB_NAME]
        col_name = WikiSectionDoc.__collection__
        collection = datastore[col_name]
        doc = collection.WikiSectionDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def save(self, owner, title, content, oid, **kwargs):
        return super(WikiSectionAPI, self).create(owner=owner, title=title, content=content, oid=oid, **kwargs)
    
    def remove(self, id):
        return super(WikiSectionAPI, self).remove(id)
    
    def edit(self, id, title=None, content=None, revise=None, oid=None, **kwargs):
        if title:kwargs['title'] = title
        if content:kwargs['content'] = content
        if revise:kwargs['revise'] = revise
        if oid:kwargs['oid'] = oid
        return super(WikiSectionAPI, self).edit(id, **kwargs)
    
    def revise(self, id, content=None):
        if content is None:
            r = self.get(id)
            content = r[1]['content']
        return self.edit(id, content=content)
    
    def _perm(self, cuid, owner):
        if cuid == owner:
            return PERM_CLASS['wFOUNDER']
        p = Permission()
        r = p._api.site_perm(cuid)
        if r:return r
        return PERM_CLASS['NORMAL']
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        now = datetime.now()
        output_map = lambda i: {'id':i['_id'], 'added_id':i['added_id'], 'owner':i['owner'], 'perm':self._perm(cuid, i['owner']), 'is_own':(cuid==i['owner'] if i['owner'] else True), 'nick':i['added'].get('nick', '匿名驴友'), 'content':i['content'], 'revise':i['revise'], 'created':self._escape_created(now, i['created'])}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1]))
        return r














