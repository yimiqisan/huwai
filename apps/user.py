#!/usr/bin/env python
# encoding: utf-8
"""
user.py

Created by 刘 智勇 on 2011-09-28.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""


import logging
import uuid
from datetime import datetime
from md5 import md5

from huwai.config import DB_CON, DB_NAME
from modules import UserDoc
from api import API
from huwai.apps import case

from mail import TmpTable, Mail

class User(object):
    def __init__(self, api=None):
        self._api = api if api else UserAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None
    
    def whois(self, k, v):
        c = self._api.one(**{k:v})
        if c[0] and c[1]:
            self.info = c[1]
            self.uid = self.info['_id']
        else:
            self.uid = self.info = None
    
    def is_invited(self, id):
        t = TmpTable()
        return t._api.check(id)
    
    def invite(self, email):
        m = Mail(email)
        t = TmpTable()
        r = t._api.set(email)
        return m.send('ni hao ma', 'invite', r[1])
    
    def _fire_alert(self, owner, pwd):
        c = case.get_case_object()
        c.fire('a_pwd', owner=owner, pwd=pwd)
    
    def register(self, nick, password=None, **info):
        r = self._api.is_nick_exist(nick)
        if r:return (False, '名号已被占用')
        email = info.get('email', None)
        if email:
            if self._api.is_email_exist(email):return (False, '邮箱已被占用')
        if not password:
            password = self.random_password()
        pwd = unicode(md5(password).hexdigest())
        info.update({'nick':nick, 'password':pwd})
        c = self._api.create(**info)
        if c[0]:
            self.info = info
            self._fire_alert(c[1], password)
        else:
            self.info = None
        return c
    
    def login(self, nick, password):
        r = self._api.is_nick_exist(nick)
        if not r:return (False, '查无此人')
        c = self._api.one(nick=nick)
        password = unicode(md5(password).hexdigest())
        if c[0] and (c[1]['password'] == password):
            self.info = c[1]
            return (True, c[1])
        self.info = None
        return (False, '用户名或密码错误')
    
    def reset_password(self, id, email):
        pwd = self.random_password()
        password = unicode(md5(pwd).hexdigest())
        self._api.edit(id, password=password)
        return (True, pwd)
        
    def random_password(self):
        from string import digits, ascii_letters
        from random import sample
        seed = digits+ascii_letters
        return ''.join(sample(seed, 6))

class UserAPI(API):
    def __init__(self):
        DB_CON.register([UserDoc])
        datastore = DB_CON[DB_NAME]
        col_name = UserDoc.__collection__
        collection = datastore[col_name]
        doc = collection.UserDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def is_nick_exist(self, nick):
        return self.exist("nick", nick)
    
    def is_email_exist(self, email):
        return self.exist("email", email)
    
    def is_nick(self, nick):
        try:
            nick.encode('utf8')
        except UnicodeEncodeError:
            return True
        if len(nick)==32:
            return False
        return True
    
    def change_pwd(self, id, o, n, c):
        self.edit(id, password=n)
    
    def check_email(self):
        pass
    
    def nick2id(self, nick):
        if self.is_nick(nick):
            r = self.one(nick=nick)
            if r[0] and r[1]:
                return r[1]['_id']
            return None
        return nick







        