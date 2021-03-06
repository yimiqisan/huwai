#!/usr/bin/env python
# encoding: utf-8
"""
ajaxHandler.py

Created by 刘 智勇 on 2011-12-22.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import uuid
import json

from baseHandler import BaseHandler
from huwai.apps.timeline import TimeLine
from huwai.apps.behavior import Behavior
from huwai.apps.pstore import Pstore
from huwai.apps.tools import session


class AjaxReplyHandler(BaseHandler):
    CHANNEL = u'reply'
    @session
    def get(self):
        uid = self.SESSION['uid']
        tid = self.get_argument("id")
        cursor = self.get_argument('cursor', None)
        if cursor:cursor=int(cursor)
        tl = TimeLine()
        r = tl._api.extend(cuid=uid, channel=[u'reply'], topic=tid, cursor=cursor, limit=10)
        if r[0]:
            htmls = []
            for i in r[1]:
                htmls.append(self.render_string("weibo/reply.html", reply=i, uid=uid))
            return self.write(json.dumps({'htmls':htmls, 'info':r[1], 'cursor': r[2]}))
        else:
            return self.write({'error':'save error'})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        reply = self.preserve(uid)
        if reply:
            reply["html"] = self.render_string("weibo/reply.html", reply=reply)
        else:
            return self.write(json.dumps({'error':'save error'}))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(json.dumps(reply))
    
    @session
    def preserve(self, uid):
        uid = self.SESSION['uid']
        to = self.get_argument("to")
        c = self.get_argument("content")
        tl = TimeLine()
        nick = self.current_user if uid else '匿名驴友'
        kwargs = {'nick':nick}
        r = tl._api.save(c, owner=uid, tid=to, channel=self.CHANNEL, **kwargs)
        if r[0]:
            kwargs.update({'id':r[1], 'content':c, 'owner': uid, 'is_own':True, 'tid': to, 'created':'刚刚'})
            return kwargs
        else:
            return None

class AjaxNewReplyHandler(BaseHandler):
    CHANNEL = u'reply'
    @session
    def get(self):
        uid = self.SESSION['uid']
        tid = self.get_argument("id")
        limit = int(self.get_argument("limit", 10))
        cursor = self.get_argument('cursor', None)
        if cursor:cursor=int(cursor)
        tl = TimeLine()
        r = tl._api.extend(cuid=uid, channel=[u'reply'], topic=tid, cursor=cursor, limit=limit)
        if r[0]:
            htmls = []
            for i in r[1]:
                htmls.append(self.render_string("util/reply.html", reply=i, uid=uid))
            return self.write(json.dumps({'htmls':htmls, 'info':r[1], 'cursor': r[2]}))
        else:
            return self.write({'error':'save error'})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        reply = self.preserve(uid)
        if reply:
            reply["html"] = self.render_string("util/reply.html", reply=reply)
        else:
            return self.write(json.dumps({'error':'save error'}))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(json.dumps(reply))
    
    @session
    def preserve(self, uid):
        uid = self.SESSION['uid']
        to = self.get_argument("to")
        c = self.get_argument("content")
        tl = TimeLine()
        nick = self.current_user if uid else '匿名驴友'
        kwargs = {'nick':nick}
        r = tl._api.save(c, owner=uid, tid=to, channel=self.CHANNEL, **kwargs)
        if r[0]:
            kwargs.update({'id':r[1], 'content':c, 'owner': uid, 'is_own':True, 'tid': to, 'created':'刚刚'})
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
        self.write(json.dumps('ok'))

class AjaxToggleStateHandler(BaseHandler):
    @session
    def post(self):
        uid = self.SESSION['uid']
        b = Behavior()
        k = self.get_argument("kind", 'kind')
        m = self.get_argument("mark", 'mark')
        s = b._api.state(uid, k, m)
        if s[0] and s[1]:
            id = s[1]['_id']
            r = b._api.cancel(uid, k, m)
        else:
            r = b._api.ok(uid, k, m, nick=self.current_user)
        self.write(json.dumps(r))

class AjaxToggleInputHandler(BaseHandler):
    @session
    def post(self):
        uid = self.SESSION['uid']
        b = Behavior()
        k = self.get_argument("kind", None)
        m = self.get_argument("mark", None)
        return self.write(json.dumps('ok'))
        
        s = b._api.state(uid, k, m)
        if s[0] and s[1]:
            id = s[1]['_id']
            r = b._api.cancel(uid, k, m)
        else:
            r = b._api.ok(uid, k, m)
        self.write(json.dumps(r))
    
    
    
    
    
    
    
    
    
    
    