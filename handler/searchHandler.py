#!/usr/bin/env python
# encoding: utf-8
"""
albumHandler.py

Created by 刘 智勇 on 2012-03-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import json
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from huwai.apps.tools import session

class SearchHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        return self.render("search/index.html")

