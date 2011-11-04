#!/usr/bin/env python
# encoding: utf-8
"""
user.py

Created by 刘 智勇 on 2011-09-28.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import UserAPI


class User(object):
    def __init__(self, api=None):
        self._api = api if api else UserAPI()
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None
    
    def whois(self, k, v):
        ret = self._api.one(**{key:value})
        if ret:
            self.info = ret
            self.uid = self.info['_id']
        else:
            self.uid = self.info = None
    
    def register(self, nick, password):
        r = self._api.is_nick_exist(nick)
        if r:return (False, '名号已被占用')
        info = {'nick':nick, 'password':password}
        c = self._api.create(**info)
        if c[0]:
            self.info = info
            return (True, info)
        else:
            self.info = None
            return c
    
    def login(self, nick, password):
        r = self._api.is_nick_exist(nick)
        if not r:return (False, '查无此人')
        c = self._api.one(nick=nick)
        if c[0] and (c[1]['password'] == password):
            self.info = c[1]
            return (True, c[1])
        self.info = None
        return (False, '用户名或密码错误')










        