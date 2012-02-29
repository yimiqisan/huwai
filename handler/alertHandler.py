#!/usr/bin/env python
# encoding: utf-8
"""
eventHandler.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import json

from tornado.web import addslash, authenticated

from apps.tools import session
from apps.alert import Alert
from apps.timeline import TimeLine

from baseHandler import BaseHandler

class AlertHandler(BaseHandler):
    @authenticated
    @addslash
    @session
    def get(self, id):
        pass
    
    @authenticated
    @addslash
    @session
    def post(self):
        pass

class AlertListHandler(BaseHandler):
    @authenticated
    @addslash
    @session
    def get(self, subject):
        uid = self.SESSION['uid']
        t = TimeLine()
        if subject == 'reply':
            r = t._api.get_rp_org(owner=uid)
        elif subject == 'rpat':
            r = t._api.get_rpat_org(channel=[u'reply'], at=self.current_user)
        elif subject == 'at':
            r = t._api.extend(channel=[u'weibo'], at=self.current_user, cursor=None)
        else:
            return self.render("alert/list.html", alert_list=[])
        if r[0]:self.render("alert/list.html", alert_list=r[1])
    
    @authenticated
    @addslash
    @session
    def post(self):
        pass

class AjaxAlertHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        a = Alert()
        r = a._api.list(uid)
        if r[0]:
            htmls = []
            for i in r[1]:
                i['suffix'] = {u'at':u'微博中@您', u'rpat':u'回复中@您', u'reply':u'回复'}[i['subject']]
                htmls.append(self.render_string("alert/item.html", message=i))
            return self.write(json.dumps({'htmls':htmls}))
        else:
            return self.write({'error':'save error'})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        subject = unicode(self.get_argument('subject', ''))
        a = Alert()
        r = a._api.click(uid, subject)
        return self.write(json.dumps({'ret':'ok'}))
    









