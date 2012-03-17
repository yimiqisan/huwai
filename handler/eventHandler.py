#!/usr/bin/env python
# encoding: utf-8
"""
eventHandler.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from tornado.web import addslash, authenticated

from mongokit import *
import datetime
import types 
import pymongo
import uuid

from apps.tools import session
from apps.event import Event
from apps.timeline import TimeLine
from apps.behavior import Behavior
from apps.role import Role

from baseHandler import BaseHandler

ISO_TIME_FORMAT_YMDHM = '%Y%m%d:%H:%M'

class EventHandler(BaseHandler):
    @authenticated
    @addslash
    @session
    def get(self, id):
        uid = self.SESSION['uid']
        e = Event()
        b = Behavior()
        r = e._api.get(id, uid)
        rb = b._api.list(kind=u'join', mark=id)
        if r[0]:
            self.render("event/item.html", user_list=rb, eid=id, **r[1])
        else:
            self.render("event/item.html", eid=id, warning=r[1])
    
    @addslash
    def post(self):
        pass

class EventPubaHandler(BaseHandler):
    KEYS = ["logo", "title", "club", "level", "attention_tl", "declare_tl", "members", "spend_tl", "place", "equip", "route", "is_merc", "schedule_tl", "tags"]
    
    @authenticated
    @addslash
    def get(self):
        d = {}
        for n in self.KEYS:d[n] = None
        self.render("event/publish_step_one.html", **d)
    
    @authenticated
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
        r = e._api.save_step_one(uid, d['logo'], d['title'], [d['tags']], is_merc, float(d['level']), d['date'], d['place'], d['schedule_tl'], nick=nick, members={'name':d['members']}, club=d['club'], route=u'route', spend_tl=d['spend_tl'], equip=[d['equip']], declare_tl=d['declare_tl'], attention_tl=d['attention_tl'])
        if r[0]:
            return self.redirect('/event/pubb/?eid='+str(r[1]))
        else:
            d['warning'] = r[1]
            return self.render("event/event_puba.html", **d)
    
class EventPubbHandler(BaseHandler):
    @authenticated
    @addslash
    @session
    def get(self):
        return self.render("event/publish_step_two.html")
        uid = self.SESSION['uid']
        eid = self.get_argument('eid', None)
        if not eid:return self.render("event/publish_step_two.html", **{'warning': u'发布失败，请重试！'})
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

class EventListHandler(BaseHandler):
    @authenticated
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        e = Event()
        r = e._api.list(cuid=uid)
        l = []
        if r[0]:
            t = TimeLine()
            for i in r[1]:
                i['tl'] = t._api.abbr(topic=i['tid'], channel=[u'weibo'])
                l.append(i)
            self.render("event/list.html", event_list=l, title="活动列表")
        else:
            self.render("event/list.html", event_list=l, warning=r[1])

class EventFallsHandler(BaseHandler):
    @authenticated
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        e = Event()
        r = e._api.list(cuid=uid)
        l = []
        if r[0]:
            t = TimeLine()
            for i in r[1]:
                i['tl'] = t._api.abbr(topic=i['tid'], channel=[u'weibo'])
                l.append(i)
            self.render("event/falls.html", event_list=l, title="活动列表")
        else:
            self.render("event/falls.html", event_list=l, warning=r[1])

class EventMemberHandler(BaseHandler):
    @authenticated
    @addslash
    @session
    def get(self, id):
        uid = self.SESSION['uid']
        b = Behavior()
        r = b._api.list(kind=u'join', mark=id)
        self.render("event/member.html", userlist=r, eid=id)

class EventCheckHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        self.render_alert(u"发布成功，\n请耐心等待，\n我们的审核灰常快。")

class EventApprovalHandler(BaseHandler):
    @addslash
    @session
    def get(self, id):
        uid = self.SESSION['uid']
        b = Behavior()
        r = b._api.list(kind=u'join')
        self.render("event/approval.html", userlist=r)

class EventCrawlerHandler(BaseHandler):
    @addslash
    def get(self):
        stra = self.get_spider_events()
        l=len(stra)/2
        entries1=[]
        entries2=[]
        for i in range(l):
            entries1.append(stra[i])
            entries2.append(stra[i+l])
            #handler data for outputing
        self.render("event/event.html", entries1=entries1, entries2=entries2, entries=stra)
    
    def get_spider_events(self, page=1, number=8, data="all"):
        conn = Connection()
        conn.register([ActivityData])
        col = conn.test.example
        return list(col.find().sort('rank', pymongo.DESCENDING))

class DBException(Exception):
    def __init__(self, error):
        Exception.__init__(self)
        self.error = error

class ActivityData(Document):
    structure = {
        'title':unicode,
        'link':unicode,
        'imageurl':{"originurl":unicode,"localurl":unicode},
        'organizername':unicode,
        'activityclass':unicode,
        'place':unicode,
        'time':unicode,
        'hotnumber':unicode,
        'uuid':str,
        'date_creation':datetime.datetime,
        'rank':int
    }
    required_fields = ['title','link','imageurl.originurl','imageurl.localurl','organizername','activityclass','place','time','hotnumber']
    default_values = {'uuid':str(uuid.uuid4()), 'rank':0, 'date_creation':datetime.datetime.utcnow}
