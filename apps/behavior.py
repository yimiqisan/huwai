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
    
    def state(self, owner, kind, mark):
        return self.one(owner=owner, kind=kind, mark=mark)
    
    def ok(self, owner, kind, mark, **kwargs):
        r = self.state(owner, kind, mark)
        return r if r[0] else self.create(owner=owner, kind=kind, mark=mark, **kwargs)
    
    def edit(self, owner, kind, mark, **kwargs):
        r = self.state(owner, kind, mark)
        if r[0]:
            id = r[1]['_id']
            return super(BehaviorAPI, self).edit(id, **kwargs)
        else:
            return (False, 'no exist')
    
    def cancel(self, owner, kind, mark):
        return self.drops(owner=owner, kind=kind, mark=mark)


