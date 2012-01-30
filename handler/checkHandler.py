#!/usr/bin/env python
# encoding: utf-8
"""
checkHandler.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from tornado.web import addslash
from config import TIME_FORMAT

from mongokit import *
import datetime
import types 
import pymongo
import uuid

from apps.tools import session
from apps.event import Event

from baseHandler import BaseHandler


class CheckEventHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        e = Event()
        r = e._api.list(check=False)
        if r[0]:
            return self.render("check/c_event.html", event_list=self._content_filter(r[1]))
        else:
            return self.render("check/c_event.html", **{'warning': r[1], 'event_list':[]})
    
    def _content_filter(self, l):
        rl = []
        for i in l:
            i['is_merc']=u'商业性质' if i['is_merc'] else u'非商业性质'
            i['created']=i['created'].strftime(TIME_FORMAT)
            i['date']=i['date'].strftime(TIME_FORMAT)
            i['tags']=''.join(i['tags']) if i['tags'][0] else ''
            i['equip']=''.join(i['equip']) if i['equip'][0] else ''
            i['club']= u'网站' if (i['club']==u'site') else u'小组内部'
            i['deadline']=i['deadline'].strftime(TIME_FORMAT)
            i['when']=i['when'].strftime(TIME_FORMAT)
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






