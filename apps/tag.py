#!/usr/bin/env python
# encoding: utf-8
"""
tag.py

Created by 刘 智勇 on 2012-03-22.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
from datetime import datetime
import re

from huwai.config import DB_CON, DB_NAME, DEFAULT_CUR_UID
from modules import TagDoc
from api import API

TAG_TYPE = {
    'event':u'活动',
    'equip':u'装备',
    'place':u'地点',
    'appraise':u'评价',
    'brand':u'品牌'
}

class Tag(object):
    def __init__(self, api=None):
        self._api = TagAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None

class TagAPI(API):
    def __init__(self):
        DB_CON.register([TagDoc])
        datastore = DB_CON[DB_NAME]
        col_name = TagDoc.__collection__
        collection = datastore[col_name]
        doc = collection.TagDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def add(self, owner, content, relation_l=[], **kwargs):
        r = self.one(content=content)
        if r[0] and r[1]:
            return super(TagAPI, self).edit(r[1]['_id'], relation_l=relation_l, **kwargs)
        return super(TagAPI, self).create(owner=owner, content=content, relation_l=relation_l, **kwargs)
    
    def madd(self, owner, content, relation_l=None, **kwargs):
        tl = content.split(',')
        if not isinstance(relation_l, list):
            relation_l = [relation_l]
        for t in tl:
            r = self.add(owner, t, relation_l, **kwargs)
            if not r[0]:return r
        return (True, None)
    
    def remove(self, id):
        if not id:return(False, None)
        return super(TagAPI, self).remove(id)
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        now = datetime.now()
        output_map = lambda i: {'id':i['_id'], 'owner':i['owner'], 'is_own':(cuid==i['owner'] if i['owner'] else True), 'added_id':i['added_id'], 'content':i['content'], 'relation':i.get('relation_l', []), 'created':i['created'].strftime('%Y-%m-%d %H:%M')}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1]))
        return r
    
    def contact(self, rel, id=None, content=None):
        pass
    
    def disconnect(self, rel, id=None, content=None):
        pass
    
    def list(self, cuid=DEFAULT_CUR_UID, owner=None, content=None, rels=None, hot=-1):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if content:kwargs['content']=re.compile('.*'+content+'.*')
        if rels:kwargs['relation_l'] = {'$all':rels} if isinstance(rels, list) else rels
        r = self.find(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l)
        else:
            return (False, r[1])







