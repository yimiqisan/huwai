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
from modules import GuideDoc
from api import API
from tag import Tag
from perm import Permission

class Guide(object):
    def __init__(self, api=None):
        self._api = GuideAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None

class GuideAPI(API):
    def __init__(self):
        DB_CON.register([GuideDoc])
        datastore = DB_CON[DB_NAME]
        col_name = GuideDoc.__collection__
        collection = datastore[col_name]
        doc = collection.GuideDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def save(self, owner, title, href, image=None, tags=[], price=-1.0, **kwargs):
        return super(GuideAPI, self).create(owner=owner, title=title, image=image, tags=tags, price=price, **kwargs)
    
    def _perm(self, cuid, owner):
        if cuid == owner:
            return PERM_CLASS['wFOUNDER']
        p = Permission()
        r = p._api.site_perm(cuid)
        if r:return r
        return PERM_CLASS['NORMAL']
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        now = datetime.now()
        t = Tag()
        output_map = lambda i: {'id':i['_id'], 'added_id':i['added_id'], 'owner':i['owner'], 'perm':self._perm(cuid, i['owner']), 'is_own':(cuid==i['owner'] if i['owner'] else True), 'title':i.get('title', None), 'href':i['href'], 'image':i['image'], 'tags':t._api.id2content(i['tags']), 'price': i['price'], 'created':self._escape_created(now, i['created'])}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1]))
        return r
    
    def list(self, cuid=DEFAULT_CUR_UID, owner=None, title=None, tags=None, pfr=None, pto=None):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if title:kwargs['title'] = re.compile('.*'+title+'.*')
        if tags:kwargs['tags'] = {'$all':tags} if isinstance(tags, list) else tags
        if pfr:kwargs['price']={'$gt':float(pfr)}
        if pto:
            if kwargs.has_key('price'):
                kwargs['price'].update({'$lt':float(pto)})
            else:
                kwargs['price'] = {'$lt':float(pto)}
        r = self.find(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l)
        else:
            return (False, r[1])
    
    def extend(self, cuid=DEFAULT_CUR_UID, owner=None, title=None, tags=None, pfr=None, pto=None, cursor=None, limit=20, order_by='added_id', order=-1):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if title:kwargs['title'] = re.compile('.*'+title+'.*')
        if tags:kwargs['tags'] = {'$all':tags} if isinstance(tags, list) else tags
        if pfr:kwargs['price']={'$gt':float(pfr)}
        if pto:
            if kwargs.has_key('price'):
                kwargs['price'].update({'$lt':float(pto)})
            else:
                kwargs['price'] = {'$lt':float(pto)}
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
    
    def page(self, cuid=DEFAULT_CUR_UID, owner=None, title=None, tags=None, pfr=None, pto=None, page=1, pglen=10, cursor=None, limit=20, order_by='added_id', order=-1):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if title:kwargs['title'] = re.compile('.*'+title+'.*')
        if tags:kwargs['tags'] = {'$all':tags} if isinstance(tags, list) else tags
        if pfr:kwargs['price']={'$gt':float(pfr)}
        if pto:
            if kwargs.has_key('price'):
                kwargs['price'].update({'$lt':float(pto)})
            else:
                kwargs['price'] = {'$lt':float(pto)}
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