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
from huwai.apps.timeline import TimeLine
from huwai.apps.event import Event
from huwai.apps.note import Note
from huwai.apps.album import Album
from huwai.apps.tag import Tag
from huwai.apps.pstore import Pstore
from huwai.apps.tools import session

class RootHandler(BaseHandler):
    def get(self):
        return self.render("index_vote.html")
        if self.current_user:
            self.redirect('/account/profile/')
        else:
            t = TimeLine()
            rt = t._api.list(channel=[u'normal', u'weibo', u'club', u'event', u'album'])
            g = Tag()
            rg = g._api.list(rels='place')
            self.render("index.html", weibo_l=rt[1], tag_l=rg[1][:10])

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
    
class SinaXDHandler(BaseHandler):
    def get(self):
        self.render("xd.html")
    
class GoogleWebMasterHandler(BaseHandler):
    def get(self):
        self.write('google-site-verification: google9f2d915bcc519f6e.html')
    
class CDNZZHandler(BaseHandler):
    def get(self):
        self.write('0e9f73cc370a47640032ac94b1d9d1a7')

class SiteMapHandler(BaseHandler):
    def get(self):
        item = self.get_argument('item', None)
        page = int(self.get_argument('page', 1))
        wb_args = et_args = nt_args = al_args = {}
        if item == 'weibo':
            wb_args['page'] = page
        elif item == 'event':
            et_args['page'] = page
        elif item == 'note':
            nt_args['page'] = page
        elif item == 'album':
            al_args['page'] = page
        t = TimeLine()
        rt = t._api.page(channel=[u'normal', u'reply', u'weibo', u'club', u'event', u'album'], **wb_args)
        e = Event()
        re = e._api.page(check=True, **et_args)
        n = Note()
        rn = n._api.page(**nt_args)
        a = Album()
        ra = a._api.page(**al_args)
        self.render("sitemap.html", wb_list=rt[1], wb_info=rt[2], et_list=re[1], et_info=re[2], nt_list=rn[1], nt_info=rn[2], al_list=ra[1], al_info=ra[2])

class ContactHandler(BaseHandler):
    def get(self):
        self.render("contact.html")
    

