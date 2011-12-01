#!/usr/bin/env python
# encoding: utf-8
"""
weiboHandler.py

Created by 刘 智勇 on 2011-11-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from baseHandler import BaseHandler
from apps.timeline import TimeLine
from apps.tools import session
from datetime import datetime

class WeiboHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        tl = TimeLine()
        r = tl._api.page(cuid=uid, channel=[u'weibo'])
        if r[0]:
            return self.render("weibo.html", **{'messages': r[1]})
        else:
            return self.render("weibo.html", **{'warning': r[1], 'messages': []})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        c = self.get_argument('content', None)
        n = self.get_secure_cookie("user") if uid else u'匿名驴友'
        tl = TimeLine()
        r = tl._api.save(c, owner=uid, nick=n)
        if r[0]:
            return self.redirect("/weibo")
        else:
            return self.render("weibo.html", **{'warning': r[1], 'messages': []})

class AjaxWeiboNewHandler(BaseHandler):
    @session
    def post(self):
        uid = self.SESSION['uid']
        message = self.preserve(uid)
        if message:
            message["html"] = self.render_string("message.html", message=message, uid=uid)
        else:
            return self.write({'error':'save error'})
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
    
    def preserve(self, uid):
        c = self.get_argument("content")
        tl = TimeLine()
        nick = self.current_user if uid else u'匿名驴友'
        kwargs = {'nick':nick}
        r = tl._api.save(c, owner=uid, channel=u'weibo', **kwargs)
        if r[0]:
            kwargs.update({'id':r[1], 'content':c, 'owner': uid, 'is_own':True})
            return kwargs
        else:
            return None
