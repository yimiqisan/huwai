#!/usr/bin/env python
# encoding: utf-8
"""
api.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import logging
import uuid

from huwai.config import DB_CON, DB_NAME
from modules import IdDoc, UserDoc, MediaLineDoc
from tools import trans_64

from api import TimeLineAPI

class TimeLine(object):
    def __init__(self, api=None):
        self._api = api if api else TimeLineAPI()
    
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
        