#!/usr/bin/env python
# encoding: utf-8
"""
eventHandler.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import json

from apps.tools import session
from apps.alert import Alert
from apps.timeline import TimeLine

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

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def open(self):
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        parsed = tornado.escape.json_decode(message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed["body"],
            }
        chat["html"] = self.render_string("alert/item.html", message=chat)

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)



class AlertListHandler(BaseHandler):
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

