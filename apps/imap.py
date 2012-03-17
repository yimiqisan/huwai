#!/usr/bin/env python
# encoding: utf-8
"""
map.py

Created by 刘 智勇 on 2012-03-07.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime
import time

from huwai.config import DB_CON, DB_NAME, DEFAULT_CUR_UID
from modules import MapDoc
from api import API

class Map(object):
    def __init__(self, id=None, api=None):
        self._api = api if api else MapAPI()
        if id:
            ret = self._api.one(_id=id)
            self.info, self.eid = (ret[1], ret[1]['_id']) if ret[0] else (None, None)
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None
    
class MapAPI(API):
    def __init__(self):
        DB_CON.register([MapDoc])
        datastore = DB_CON[DB_NAME]
        col_name = MapDoc.__collection__
        collection = datastore[col_name]
        doc = collection.MapDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def save(self, owner, subject, location=None, polyline=None, link=None, **kwargs):
        return super(MapAPI, self).create(owner=owner, subject=subject, location=location, polyline=polyline, link=link, **kwargs)
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        now = datetime.now()
        output_map = lambda i: {'id':i['_id'], 'added_id':i['added_id'], 'owner':i['owner'], 'is_own':(cuid==i['owner'] if i['owner'] else True), 'created':self._escape_created(now, i['created']), 'subject':i['subject'], 'link':i['link'], 'polyline':i['polyline'], 'location':i['location']}
        if isinstance(result, dict):
            return output_map(result)
        return map(output_map, result)
    
    def get(self, id):
        r = self.one(_id=id)
        if (r[0] and r[1]):return (True, self._output_format(result=r[1]))
        return r
    
    def near(self, cuid=DEFAULT_CUR_UID, near=[]):
        r = self.find(**{"location": {"$near": near}})
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l)
        else:
            return (False, r[1])
    
    def list(self, cuid=DEFAULT_CUR_UID, owner=None, subject=None, location=None):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if subject:kwargs['subject']={'$in':subject}
        if topic:kwargs['topic'] = {'$in':topic} if isinstance(topic, list) else topic
        r = self.find(**kwargs)
        if r[0]:
            kw = {'result':r[1]}
            if cuid:kw['cuid']=cuid
            l = self._output_format(**kw)
            return (True, l)
        else:
            return (False, r[1])
    
    
    
    