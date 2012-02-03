#!/usr/bin/env python
# encoding: utf-8
"""
alert.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime
import time

from huwai.config import DB_CON, DB_NAME
from modules import AlertDoc
from api import API
from user import User

class Alert(object):
    def __init__(self, api=None):
        self._api = AlertAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None

class AlertAPI(API):
    DEFAULT_CUR_UID = '948a55d68e1b4317804e4650a9505641'
    def __init__(self):
        DB_CON.register([AlertDoc])
        datastore = DB_CON[DB_NAME]
        col_name = AlertDoc.__collection__
        collection = datastore[col_name]
        doc = collection.AlertDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def incr(self, id):
        try:
            self.collection.update({"_id":id},{"$inc":{"count":1}}, upsert=True)
        except Exception, e:
            logging.info(e)
            return False
        return True

    def _init_alert(self, owner, subject):
        r = self.one(owner=owner, subject=subject)
        if r[0] and r[1]:
            return r[1]['_id']
        else:
            r = self.create(owner=owner, subject=subject, count=0)
            return r[1] if r[0] else None
    
    def on_reply(self, to):
        u = User()
        owner = u._api.nick2id(to)
        id = self._init_alert(owner, u'reply')
        return self.incr(id) if id else False
    
    def on_join(self, to):
        u = User()
        owner = u._api.nick2id(to)
        id = self._init_alert(owner, u'join')
        return self.incr(id) if id else False
    
    def click(self, owner, subject):
        id = self._init_alert(owner, subject)
        return self.edit(id, count=0) if id else (False, None)
    
    def list(self, owner):
        kwargs = {}
        kwargs['owner']=owner
        kwargs['count']={'$gt':0}
        r = self.find(**kwargs)
        ret_l = []
        if r[0]:
            for i in r[1]:
                ret_l.append({'id':i['_id'], 'subject':i['subject'], 'count':i['count']})
            return (True, ret_l)
        return r
    
    