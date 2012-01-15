#!/usr/bin/env python
# encoding: utf-8
"""
common.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import uuid
import json
from tornado.web import addslash

from baseHandler import BaseHandler
from apps.timeline import TimeLine
from apps.pstore import Pstore
from apps.tools import session

class RootHandler(BaseHandler):
    def get(self):
        self.render("index.html")

class TestHandler(BaseHandler):
    @addslash
    def get(self):
        pid = self.get_argument("pid", None)
        self.render("test.html", pid=pid)

class FeedbackHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        tl = TimeLine()
        r = tl._api.list(topic='feedback')
        if r[0]:
            return self.render("feedback.html", messages=r[1])
        else:
            return self.render("feedback.html", warning=r[1])
    
    @addslash
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
    @addslash
    def get(self):
        self.render_alert(u"从前有个山，\n山里有个庙，\n庙里有个页面，\n现在找不到。")
    
class GoogleWebMasterHandler(BaseHandler):
    def get(self):
        self.write('google-site-verification: google9f2d915bcc519f6e.html')

