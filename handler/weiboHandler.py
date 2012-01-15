#!/usr/bin/env python
# encoding: utf-8
"""
weiboHandler.py

Created by 刘 智勇 on 2011-11-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import json
from tornado.web import addslash

from baseHandler import BaseHandler
from apps.timeline import TimeLine
from apps.tools import session
from datetime import datetime

class WeiboHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        return self.render("weibo/weibo.html")

class AjaxWeiboHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        cursor = self.get_argument('cursor', None)
        maintype = self.get_argument('maintype', None)
#        subtype = self.get_argument('subtype', None)
        if cursor:cursor=int(cursor)
        tl = TimeLine()
        r = tl._api.extend(cuid=uid, channel=[u'weibo'], cursor=cursor, topic=maintype)
        if r[0]:
            htmls = []
            for i in r[1]:
                htmls.append(self.render_string("weibo/message.html", message=i, uid=uid))
            return self.write(json.dumps({'htmls':htmls, 'info':r[1], 'cursor': r[2]}))
        else:
            return self.write({'error':'save error'})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        message = self.preserve(uid)
        if message:
            message["html"] = self.render_string("weibo/message.html", message=message, uid=uid)
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
            kwargs.update({'id':r[1], 'content':c, 'owner': uid, 'is_own':True, 'created':'刚刚'})
            return kwargs
        else:
            return None
