#!/usr/bin/env python
# encoding: utf-8
"""
common.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import uuid
import json

from baseHandler import BaseHandler
from apps.timeline import TimeLine
from apps.pstore import Pstore
from apps.tools import session

class RootHandler(BaseHandler):
    def get(self):
        self.render("index.html")

class TestHandler(BaseHandler):
    def get(self):
        pid = self.get_argument("pid", None)
        self.render("test.html", pid=pid)

class FeedbackHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        tl = TimeLine()
        r = tl._api.list(topic='feedback')
        if r[0]:
            return self.render("feedback.html", messages=r[1])
        else:
            return self.render("feedback.html", warning=r[1])
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        c = self.get_argument('content', None)
        n = self.get_secure_cookie("user") if uid else u'匿名驴友'
        to = self.get_argument("to")
        tl = TimeLine()
        r = tl._api.save(c, owner=uid, tid=to, channel=u'reply', nick=n)
        if r[0]:
            return self.redirect("/feedback")
        else:
            return self.render("feedback.html", **{'warning': r[1]})

class Error404Handler(BaseHandler):
    def get(self):
        self.render("404.html")
    
class GoogleWebMasterHandler(BaseHandler):
    def get(self):
        self.write('google-site-verification: google9f2d915bcc519f6e.html')

