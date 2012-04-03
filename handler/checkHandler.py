#!/usr/bin/env python
# encoding: utf-8
"""
checkHandler.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import json
from tornado.web import addslash
from config import TIME_FORMAT

from mongokit import *
import datetime
import types 
import pymongo
import uuid

from huwai.apps.tools import session
from huwai.apps.event import Event

from baseHandler import BaseHandler

class AjaxCheckEventHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        e = Event()
        r = e._api.list(check=True)
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
        pass


class CheckEventHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        e = Event()
        r = e._api.list(check=True)
        if r[0]:
            return self.render("check/event.html", event_list=r[1])
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
    def post(self):
        uid = self.SESSION['uid']
        e = Event()
        for k in self.request.arguments.keys():
            v = self.get_argument(k)
            if (int(v) == 1):
                r = e._api.check(k, True)
        self.redirect('/check/event/')

class CheckTagHandler(BaseHandler):
    def get(self):
        return self.render("check/tag.html")
    
    def post(self):
        self.redirect('/check/tag/')




