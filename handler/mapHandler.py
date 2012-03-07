#!/usr/bin/env python
# encoding: utf-8
"""
mapHandler.py

Created by 刘 智勇 on 2012-02-28.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

from tornado.web import addslash

from baseHandler import BaseHandler
from apps.tools import session;


class MapHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        self.render("map/index.html")

class MapItemHandler(BaseHandler):
    @addslash
    @session
    def get(self, id):
        uid = self.SESSION['uid']
        self.render("map/item.html")
