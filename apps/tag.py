#!/usr/bin/env python
# encoding: utf-8
"""
tag.py

Created by 刘 智勇 on 2012-03-22.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging

from huwai.config import DB_CON, DB_NAME
from modules import TagDoc
from api import API

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
    
    def add(self):
        return super(TagAPI, self).create()
    
    def remove(self, id):
        return super(TimeLineAPI, self).remove(id)
    
    def _output_format(self, result=[]):
        now = datetime.now()
        output_map = lambda i: {'id':i['_id'], 'added_id':i['added_id'], 'content':i['content'], 'relation':i.get('relation_l', []), 'created':self._escape_created(now, i['created'])}
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
    
    def list(self, content=None, rels=None, hot=-1):
        kwargs = {}
#        if owner:kwargs['owner']=owner
        r = self.find(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            l = self._output_format(**kw)
            return (True, l)
        else:
            return (False, r[1])
