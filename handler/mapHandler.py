#!/usr/bin/env python
# encoding: utf-8
"""
mapHandler.py

Created by 刘 智勇 on 2012-02-28.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""
import json
from tornado.web import addslash

from baseHandler import BaseHandler
from apps.tools import session
from apps.map import Map


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

class AjaxMapHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        pass
    
    @addslash
    @session
    def post(self):
        uid = self.SESSION['uid']
        ps = self.get_argument('points', [(2.0,3.1)])
        print ps
        m = Map()
        #r = m._api.save(uid, u'route', points=ps)
        return self.write(json.dumps({'info':ps}))
    


