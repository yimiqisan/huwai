#!/usr/bin/env python
# encoding: utf-8
"""
eventHandler.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from tornado.web import addslash

from mongokit import *
import datetime
import types 
import pymongo
import uuid

from huwai.apps.tools import session
from huwai.apps.event import Event, EventScrapyAPI
from huwai.apps.timeline import TimeLine
from huwai.apps.behavior import Behavior
from huwai.apps.role import Role
from huwai.apps.tag import Tag

from baseHandler import BaseHandler

ISO_TIME_FORMAT_YMDHM = '%Y%m%d:%H:%M'

class EventHandler(BaseHandler):
    @addslash
    @session
    def get(self, id):
        uid = self.SESSION['uid']
        e = Event()
        b = Behavior()
        r = e._api.get(id, uid)
        rb = b._api.list(channel=u'approval', she=id)
        if r[0]:
            self.render("event/item.html", user_list=rb, eid=id, **r[1])
        else:
            self.render("event/item.html", eid=id, warning=r[1])
    
    @addslash
    def post(self):
        pass

class EventPubaHandler(BaseHandler):
    KEYS = ["logo", "title", "club", "level", "attention_tl", "declare_tl", "members", "spend_tl", "place", "equipTags", "route", "is_merc", "schedule_tl", "eventTags"]
    
    @addslash
    def get(self):
        d = {}
        for n in self.KEYS:d[n] = None
        self.render("event/publish_step_one.html", **d)
    
    @addslash
    @session
    def post(self):
        uid = self.SESSION['uid']
        d = {}
        for n in self.KEYS:d[n] = self.get_argument(n, None)
        timestr = ":".join([self.get_argument("begin_time"), self.get_argument("begin_time_hour"), self.get_argument("begin_time_minute")])
        d['date'] = datetime.datetime.strptime(timestr, ISO_TIME_FORMAT_YMDHM)
        e = Event()
        is_merc = d['is_merc'] is u'no_merc'
        nick = self.current_user if uid else u'匿名驴友'
        r = e._api.save_step_one(uid, d['logo'], d['title'], self._flt_tags(d['eventTags']), is_merc, float(d['level']), d['date'], d['place'], d['schedule_tl'], nick=nick, members={'name':d['members']}, club=d['club'], route=u'route', spend_tl=d['spend_tl'], equip=self._flt_tags(d['equipTags']), declare_tl=d['declare_tl'], attention_tl=d['attention_tl'])
        if r[0]:
            return self.redirect('/event/pubb/?eid='+str(r[1]))
        else:
            d['warning'] = r[1]
            return self.render("event/publish_step_one.html", **d)
    
    def _flt_tags(self, content):
        t = Tag()
        return t._api.content2id(content)
    
class EventPubbHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        eid = self.get_argument('eid', None)
        if not eid:return self.redirect("/event/puba/")
        e = Event(id=eid)
        if e.owner != uid:return self.redirect('/event/puba/')
        self.render("event/publish_step_two.html", eid=eid)
    
    @addslash
    @session
    def post(self):
        uid = self.SESSION['uid']
        eid = self.get_argument('eid', None)
        l = ["fr", "to", "where"]
        d = {}
        for n in l:d[n] = self.get_argument(n, None)
        e = Event(id=eid)
        timestr = ":".join([self.get_argument("close_time"), self.get_argument("close_time_hour"), self.get_argument("close_time_minute")])
        deadline = datetime.datetime.strptime(timestr, ISO_TIME_FORMAT_YMDHM)
        timestr = ":".join([self.get_argument("collect_time"), self.get_argument("collect_time_hour"), self.get_argument("collect_time_minute")])
        when = datetime.datetime.strptime(timestr, ISO_TIME_FORMAT_YMDHM)
        r = e._api.save_step_two(eid, uid, deadline, int(d['fr']), int(d['to']), when, d['where'])
        if r[0]:
            return self.redirect('/event/loading')
        else:
            return self.render("event/event_pubb.html", **{'warning': r[1]})

class EventCheckHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        self.render_alert(u"发布成功，\n请耐心等待，\n我们的审核灰常快。")

class EventListHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        e = Event()
        r = e._api.page(cuid=uid, check=True)
        l = []
        if r[0]:
            es = r[1]
            # crawler start
            sapi = EventScrapyAPI()
            rc = sapi.list()
            if rc[0]:es.extend(rc[1])
            # crawler end
            t = TimeLine()
            for i in es:
                i['tl'] = t._api.abbr(topic=i['tid'], channel=[u'weibo'])
                l.append(i)
            self.render("event/list.html", event_list=l, title="活动列表", pagination=r[2])
        else:
            self.render("event/list.html", event_list=l, warning=r[1])

class EventFallsHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        e = Event()
        r = e._api.list(cuid=uid, check=True)
        l = []
        if r[0]:
            t = TimeLine()
            es = r[1]
            # crawler start
            sapi = EventScrapyAPI()
            rc = sapi.list()
            if rc[0]:es.extend(rc[1])
            # crawler end
            for i in r[1]:
                i['tl'] = t._api.abbr(topic=i['tid'], channel=[u'weibo'])
                l.append(i)
            self.render("event/falls.html", event_list=l, title="活动列表")
        else:
            self.render("event/falls.html", event_list=l, warning=r[1])

class EventMemberHandler(BaseHandler):
    channel = u'approval'
    @addslash
    @session
    def get(self, id):
        uid = self.SESSION['uid']
        b = Behavior()
        r = b._api.list(cuid=uid, she=id, channel=self.channel)
        self.render("event/member.html", userlist=r, eid=id)

class EventApprovalHandler(BaseHandler):
    @addslash
    @session
    def get(self, id):
        uid = self.SESSION['uid']
        b = Behavior()
        r = b._api.list(channel=u'approval', she=id)
        self.render("event/approval.html", userlist=r, eid=id)

class AjaxEventJoinHandler(BaseHandler):
    channel = u'approval'
    @session
    def post(self):
        uid = self.SESSION['uid']
        she = self.get_argument('she', None)
        b = Behavior()
        r = b._api._is_contain(uid, she, self.channel)
        rr = b._api.delete(uid, she, self.channel) if (r[0] and r[1]) else b._api.create(uid, she, self.channel, switch=False, nick=self.current_user)
        if rr[0]:
            return self.write({'data':rr[1]})
        else:
            return self.write({'error':rr[1]})

class AjaxEventApprovalHandler(BaseHandler):
    channel = u'approval'
    @session
    def get(self):
        uid = self.SESSION['uid']
        she = self.get_argument('she', None)
        b = Behavior()
        r = b._api.list(channel=self.channel, she=she)
        if r[0]:
            return self.write(json.dumps({'userlist':r[1]}))
        else:
            return self.write({'error':'save error'})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        owner = self.get_argument('owner', uid)
        she = self.get_argument('she', None)
        check = True if self.get_argument('check', None) else False
        b = Behavior()
        if check:
            r = b._api.on(uid, she, self.channel)
        else:
            r = b._api.off(uid, she, self.channel)
        if r[0]:
            return self.write({'data':r[1]})
        else:
            return self.write({'error':r[1]})
    
    
    