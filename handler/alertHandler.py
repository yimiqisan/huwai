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
        a = Alert()
        self.render("alert/list.html", alert_list=[])
    
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
    









