#!/usr/bin/env python
# encoding: utf-8
"""
checkHandler.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import json
from tornado.web import addslash
from huwai.config import TIME_FORMAT, PERM_CLASS

from mongokit import *
import datetime
import types 
import pymongo
import uuid

from huwai.apps.tools import session
from huwai.apps.user import User
from huwai.apps.event import Event
from huwai.apps.perm import Permission, preperm

from baseHandler import BaseHandler


class CheckHandler(BaseHandler):
    @addslash
    @session
    @preperm('FOUNDER')
    def get(self):
        uid = self.SESSION['uid']
        p = Permission()
        r = p._api.list(channel=u'site', key='VERIFIER')
        return self.render("check/index.html", plist=r)
    
    @addslash
    @session
    @preperm('FOUNDER')
    def post(self):
        uid = self.SESSION['uid']
        she = self.get_argument('she', None)
        if she:
            u = User()
            u.whois('_id', she)
            nick = u.nick
        p = Permission()
        r = p._api.award(she, u'site', 'VERIFIER', nick=nick)
        return self.redirect("/check/")

class CheckEventHandler(BaseHandler):
    @addslash
    @session
    @preperm()
    def get(self):
        e = Event()
        r = e._api.list()
        if r[0]:
            ents = r[1]
            for i in xrange(0, len(ents)):
                ents[i]['number']=i+1
            return self.render("check/event.html", event_list=ents, pm=self.pm)
        else:
            return self.render("check/event.html", **{'warning': r[1], 'event_list':[]})
    
    def _content_filter(self, l):
        rl = []
        for i in l:
            i['equip']=''.join(i['equip']) if i['equip'][0] else ''
            i['members'] = ';'.join(i['members'].values())
            d={'id':i['id'], 'from':i['nick'], 'detail':self.render_string('util/event_item.html', **i)}
            rl.append(d)
        return rl
    
    @addslash
    @session
    @preperm()
    def post(self):
        uid = self.SESSION['uid']
        e = Event()
        for k in self.request.arguments.keys():
            v = self.get_argument(k)
            if (int(v) == 1):
                r = e._api.check(k, True)
        self.redirect('/check/event/')

class CheckTagHandler(BaseHandler):
    @session
    @preperm()
    def get(self):
        return self.render("check/tag.html", pm=self.pm)
    
    @session
    @preperm()
    def post(self):
        self.redirect('/check/tag/')

class AjaxCheckEventHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        e = Event()
        r = e._api.list()
        if r[0]:
            htmls = []
            for i in xrange(1, len(r[1])):
                htmls.append(self.render_string("check/event_item.html", e=r[1][i], number=i))
            return self.write(json.dumps({'htmls':htmls}))
        else:
            return self.write({'error':'save error'})
    
    @addslash
    @session
    def post(self):
        eid = self.get_argument('eid', None)
        check = True if self.get_argument('check', None) else False
        e = Event()
        r = e._api.check(eid, check, message=None)
        if r[0]:
            return self.write({'data':r[1]})
        else:
            return self.write({'error':r[1]})



