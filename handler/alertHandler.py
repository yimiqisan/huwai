#!/usr/bin/env python
# encoding: utf-8
"""
eventHandler.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import json

from huwai.apps.tools import session
from huwai.apps.alert import Alert
from huwai.apps.timeline import TimeLine

from baseHandler import BaseHandler

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid


class AlertHandler(BaseHandler):
    def get(self):
        self.render("alert/list.html", messages=ChatSocketHandler.cache)

class AlertListHandler(BaseHandler):
    @session
    def get(self, subject):
        uid = self.SESSION['uid']
        t = TimeLine()
        if subject == 'reply':
            r = t._api.get_rp_org(owner=uid)
        elif subject == 'weibo_ra':
            r = t._api.get_rpat_org(channel=[u'reply'], at=self.current_user)
        elif subject == 'weibo_at':
            r = t._api.extend(channel=[u'weibo'], at=self.current_user, cursor=None)
        else:
            return self.render("alert/list.html", alert_list=[])
        if r[0]:self.render("alert/list.html", alert_list=r[1])
    
class AjaxAlertHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        a = Alert()
        r = a._api.list(uid)
        if r[0]:
            ms = r[1]
            for m in ms:
                m['suffix'] = {u'weibo_at':u'微博中@您', u'weibo_ra':u'回复中@您'}[m['subject']]
                m['suffix'] = u'有' + unicode(m['count']) + u'条' + m['suffix']
            return self.write(json.dumps({'messages':ms}))
        else:
            return self.write({'error':'save error'})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        subject = unicode(self.get_argument('subject', ''))
        a = Alert()
        r = a._api.click(uid, subject)
        return self.write(json.dumps({'ret':'ok'}))

