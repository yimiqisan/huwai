#!/usr/bin/env python
# encoding: utf-8
"""
PeopleHandler.py

Created by 刘 智勇 on 2011-11-19.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from baseHandler import BaseHandler
from apps.timeline import TimeLine
from apps.tools import session


class PeopleHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        tl = TimeLine()
        r = tl._api.list(cuid=uid, owner=uid)
        if r[0]:
            return self.render("profile/people.html", **{'messages': r[1]})
        else:
            return self.render("profile/people.html", **{'warning': r[1], 'messages':[]})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        c = self.get_argument('content', None)
        n = self.get_secure_cookie("user") if uid else u'匿名驴友'
        tl = TimeLine()
        r = tl._api.save(c, owner=uid, nick=n)
        if r[0]:
            return self.redirect("/people")
        else:
            return self.render("profile/people.html", **{'warning': r[1], 'messages':[]})
