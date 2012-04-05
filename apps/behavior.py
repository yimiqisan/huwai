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

from huwai.config import DB_CON, DB_NAME, DEFAULT_CUR_UID
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
    
    def _is_contain(self, owner, she, channel):
        return self.one(owner=owner, she=she, channel=channel)
    
    def create(self, owner, she, channel, switch=False, **kwargs):
        r = self._is_contain(owner, she, channel)
        return r if (r[0] and r[1]) else super(BehaviorAPI, self).create(owner=owner, she=she, channel=channel, switch=switch, **kwargs)
    
    def delete(self, owner, she, channel):
        r = super(BehaviorAPI, self).drops(owner=owner, she=she, channel=channel)
        return (r, None)
    
    def edit(self, owner, she, channel, switch):
        r = self._is_contain(owner, she, channel)
        if (r[0] and r[1]):
            id = r[1]['_id']
            return super(BehaviorAPI, self).edit(id, switch=switch)
        else:
            return (False, 'no exist')
    
    def on(self, owner, she, channel):
        return self.edit(owner, she, channel, True)
    
    def off(self, owner, she, channel):
        return self.edit(owner, she, channel, False)
    
    def _output_map(self, out, cuid):
        ret_d = {'id':out['_id'], 'owner':out['owner'], 'is_own':(cuid==out['owner'] if out['owner'] else True), 'she':out['she'], 'channel':out['channel'], 'switch':out['switch'], 'created':out['created'].strftime('%m-%d %H:%M')}
        for k in out['added']:
            ret_d[k] = out['added'][k]
        return ret_d
    
    def _output_format(self, result=[], cuid=DEFAULT_CUR_UID):
        if isinstance(result, dict):
            return self._output_map(result, cuid)
        return [self._output_map(i, cuid) for i in result]
    
    def list(self, cuid=DEFAULT_CUR_UID, owner=None, she=None, channel=None, switch=None):
        kwargs = {}
        if owner:kwargs['owner'] = owner
        if she:kwargs['she'] = she
        if channel:kwargs['channel'] = channel
        if isinstance(switch, bool):kwargs['switch'] = switch
        r = self.find(**kwargs)
        if r[0]:
            return self._output_format(result=r[1], cuid=cuid)
        else:
            return None
    
    



