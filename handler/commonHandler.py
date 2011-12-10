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

class AjaxReplyHandler(BaseHandler):
    CHANNEL = u'reply'
    @session
    def get(self):
        uid = self.SESSION['uid']
        tid = self.get_argument("id")
        tl = TimeLine()
        r = tl._api.list(cuid=uid, topic=tid, channel=self.CHANNEL)
        if r[0]:
            htmls = []
            for i in r[1]:
                htmls.append(self.render_string("reply.html", reply=i, uid=uid))
            return self.write(json.dumps(htmls))
        else:
            return self.write({'error':'save error'})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        reply = self.preserve(uid)
        if reply:
            reply["html"] = self.render_string("reply.html", reply=reply)
        else:
            return self.write({'error':'save error'})
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(reply)
    
    def preserve(self, uid):
        to = self.get_argument("to")
        c = self.get_argument("content")
        tl = TimeLine()
        nick = self.current_user if self.current_user else '匿名驴友'
        kwargs = {'nick':nick}
        r = tl._api.save(c, owner=uid, tid=to, channel=self.CHANNEL, **kwargs)
        if r[0]:
            kwargs.update({'id':r[1], 'content':c, 'owner': uid, 'is_own':True})
            return kwargs
        else:
            return None
    
class AjaxRemoveHandler(BaseHandler):
    @session
    def post(self):
        tl = TimeLine()
        uid = self.SESSION['uid']
        rid = self.get_argument("id", None)
        r = tl._api.remove(rid)
        self.write('ok')

class UploadImageHandler(BaseHandler):
    @session
    def get(self):
        pid = self.get_argument("pid", None)
        self.render('upload_image.html', pid=pid)
    
    def post(self):
        p = Pstore()
        u = self.request.files['attach'][0]
        pid = str(p.put(u['body']))
        self.redirect('/upload_image?pid='+pid)

class ShowImageHandler(BaseHandler):
    def get(self, id):
        print id
        p = Pstore()
        d = p.get_by_id(id)
        self.write(d.read())

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

