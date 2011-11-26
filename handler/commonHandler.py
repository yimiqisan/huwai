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
from apps.tools import session

class RootHandler(BaseHandler):
    def get(self):
        self.redirect("/event")
        #self.render("index.html")

class TestHandler(BaseHandler):
    def get(self):
        self.render("test.html")

class AjaxReplyHandler(BaseHandler):
    CHANNEL = u'reply'
    def get(self):
        tid = self.get_argument("id")
        tl = TimeLine()
        r = tl._api.list(topic=tid, channel=self.CHANNEL)
        if r[0]:
            htmls = []
            for i in r[1]:
                htmls.append(self.render_string("reply.html", reply=i))
            return self.write(json.dumps(htmls))
        else:
            return self.write({'error':'save error'})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        message = self.preserve(uid)
        if message:
            message["html"] = self.render_string("message.html", message=message)
        else:
            return self.write({'error':'save error'})
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
    
    def preserve(self, uid):
        to = self.get_argument("to")
        c = self.get_argument("content")
        tl = TimeLine()
        nick = self.current_user if self.current_user else '匿名驴友'
        kwargs = {'nick':nick}
        r = tl._api.save(c, owner=uid, tid=to, channel=self.CHANNEL, **kwargs)
        if r[0]:
            kwargs.update({'id':r[1], 'content':c, 'owner': uid})
            return kwargs
        else:
            return None
    
class AjaxRemoveHandler(BaseHandler):
    @session
    def post(self):
        tl = TimeLine()
        uid = self.SESSION['uid']
        rid = self.get_argument("id", None)
        tl._api.remove(rid)
        self.write('ok')

class FeedbackHandler(BaseHandler):
    def get(self):
        tl = TimeLine()
        r = tl._api.list(topic='feedback')
        if r[0]:
            return self.render("feedback.html", **{'messages': r[1]})
        else:
            return self.render("feedback.html", **{'warning': r[1]})
    
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






