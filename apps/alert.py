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
import user

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

    def _init_alert(self, owner, subject, nature=u'alert', **kwargs):
        r = self.one(owner=owner, subject=subject)
        if r[0] and r[1]:
            return r[1]['_id']
        else:
            r = self.create(owner=owner, subject=subject, count=0, **kwargs)
            return r[1] if r[0] else None
    
    def on_weibo_at(self, to):
        u = user.User()
        owner = u._api.nick2id(to)
        id = self._init_alert(owner, u'weibo_at')
        return self.incr(id) if id else False
    
    def on_weibo_ra(self, to):
        u = user.User()
        owner = u._api.nick2id(to)
        id = self._init_alert(owner, u'weibo_ra')
        return self.incr(id) if id else False
    
    def on_weibo_fl(self, to):
        ''' weibo_fl '''
        pass
    
    def on_account_ml(self):
        ''' account_ml '''
        pass
    
    def on_account_pw(self):
        ''' account_pw '''
        pass
    
    def on_account_iv(self):
        ''' account_iv '''
        pass
    
    def on_event_ckfb(self, owner):
        id = self._init_alert(owner, u'event_ckfb', u'error')
        return self.incr(id) if id else False
    
    def on_event_jnfb(self, owner):
        id = self._init_alert(owner, u'event_jnfb', u'error')
        return self.incr(id) if id else False
    
    def on_event_ckps(self, owner):
        id = self._init_alert(owner, u'event_ckps', u'success')
        return self.incr(id) if id else False
    
    def on_event_jnps(self, owner):
        id = self._init_alert(owner, u'event_jnps', u'success')
        return self.incr(id) if id else False
    
    def on_event_jncf(self, owner):
        id = self._init_alert(owner, u'event_jncf', u'confirm')
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
    
    