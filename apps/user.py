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
