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

from apps.tools import session
from apps.event import Event
from apps.behavior import Behavior

from baseHandler import BaseHandler

ISO_TIME_FORMAT_YMDHM = '%Y%m%d:%H:%M'

class EventHandler(BaseHandler):
    @addslash
    def get(self, id):
        e = Event()
        b = Behavior()
        r = e._api.get(id)
        rb = b._api.list(kind=u'join', mark=id)
        if r[0]:
            self.render("event/event_show.html", user_list=rb, **r[1])
        else:
            self.render("event/event_show.html", warning=r[1])
    
    @addslash
    def post(self):
        pass

class EventPubaHandler(BaseHandler):
    @addslash
    def get(self):
        self.render("event/event_puba.html")
    
    @addslash
    @session
    def post(self):
        uid = self.SESSION['uid']
        l = ["logo", "title", "club", "level", "attention_tl", "declare_tl", "members", "spend_tl", "place", "equip", "route", "is_merc", "schedule_tl", "tags"]
        d = {}
        for n in l:d[n] = self.get_argument(n, None)
        timestr = ":".join([self.get_argument("begin_time"), self.get_argument("begin_time_hour"), self.get_argument("begin_time_minute")])
        date = datetime.datetime.strptime(timestr, ISO_TIME_FORMAT_YMDHM)
        e = Event()
        is_merc = d['is_merc'] is u'no_merc'
        d['place'] = u'place'
        nick = self.current_user if uid else u'匿名驴友'
        r = e._api.save_step_one(uid, d['logo'], d['title'], [d['tags']], is_merc, float(d['level']), date, d['place'], d['schedule_tl'], nick=nick, members={'name':d['members']}, club=d['club'], route=u'route', spend_tl=d['spend_tl'], equip=[d['equip']], declare_tl=d['declare_tl'], attention_tl=d['attention_tl'])
        if r[0]:
            return self.redirect('/event/pubb/?eid='+str(r[1]))
        else:
            return self.render("event/event_puba.html", **{'warning': r[1]})

class EventPubbHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        eid = self.get_argument('eid', None)
        if not eid:return self.render("event/event_puba.html", **{'warning': u'发布失败，请重试！'})
        e = Event(id=eid)
        if e.owner != uid:return self.redirect('/event/puba/')
        self.render("event/event_pubb.html", eid=eid)
    
    @addslash
    @session
    def post(self):
        uid = self.SESSION['uid']
        eid = self.get_argument('eid', '3f88dd869fd343e6bbe4061e22d8dec2')
        l = ["fr", "to"]
        d = {}
        for n in l:d[n] = self.get_argument(n, None)
        e = Event(id=eid)
        timestr = ":".join([self.get_argument("close_time"), self.get_argument("close_time_hour"), self.get_argument("close_time_minute")])
        deadline = datetime.datetime.strptime(timestr, ISO_TIME_FORMAT_YMDHM)
        timestr = ":".join([self.get_argument("collect_time"), self.get_argument("collect_time_hour"), self.get_argument("collect_time_minute")])
        when = datetime.datetime.strptime(timestr, ISO_TIME_FORMAT_YMDHM)
        r = e._api.save_step_two(eid, deadline, int(d['fr']), int(d['to']), when, u'where')
        if r[0]:
            return self.redirect('/event/loading')
        else:
            return self.render("event/event_pubb.html", **{'warning': r[1]})

class EventListHandler(BaseHandler):
    @addslash
    def get(self):
        e = Event()
        r = e._api.list()
        l = []
        if r[0]:
            self.render("event/event_list.html", event_list=r[1])
        else:
            self.render("event/event_list.html", event_list=[], warning=r[1])

class EventCheckHandler(BaseHandler):
    @addslash
    def get(self):
        self.render_alert(u"发布成功，\n请耐心等待，\n我们的审核灰常快")

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
