#!/usr/bin/env python
# encoding: utf-8
"""
behavior.py

Created by 刘 智勇 on 2011-12-21.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime
import time

from huwai.config import DB_CON, DB_NAME
from modules import BehaviorDoc
from api import API

class Behavior(object):
    def __init__(self, api=None):
        self._api = BehaviorAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None

class BehaviorAPI(API):
    def __init__(self):
        DB_CON.register([BehaviorDoc])
        datastore = DB_CON[DB_NAME]
        col_name = BehaviorDoc.__collection__
        collection = datastore[col_name]
        doc = collection.BehaviorDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def _output_map(self, input):
        ret_d = {'id':input['_id'], 'owner':input['owner'], 'kind':input['kind'], 'mark':input['mark'], 'created':input['created']}
        for k, v in input['added']:
            ret_d[k] = v
        return ret_d
    
    def _output_format(self, result=[]):
        if isinstance(result, dict):
            return self._output_map(result)
        return map(self._output_map, result)
    
    def state(self, owner, kind, mark):
        return self.one(owner=owner, kind=kind, mark=mark)
    
    def ok(self, owner, kind, mark, **kwargs):
        r = self.state(owner, kind, mark)
        return r if (r[0] and r[1]) else self.create(owner=owner, kind=kind, mark=mark, **kwargs)
    
    def edit(self, owner, kind, mark, **kwargs):
        r = self.state(owner, kind, mark)
        if (r[0] and r[1]):
            id = r[1]['_id']
            return super(BehaviorAPI, self).edit(id, **kwargs)
        else:
            return (False, 'no exist')
    
    def cancel(self, owner, kind, mark):
        return self.drops(owner=owner, kind=kind, mark=mark)
    
    def list(self, owner=None, kind=None, mark=None):
        kwargs = {}
        if owner:kwargs['owner'] = owner
        if kind:kwargs['kind'] = kind
        if mark:kwargs['mark'] = mark
        r = self.find(**kwargs)
        if r[0]:
            return self._output_format(result=r[1])
        else:
            return None

