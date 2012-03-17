#!/usr/bin/env python
# encoding: utf-8
"""
role.py

Created by 刘 智勇 on 2012-03-11.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

from api import API
from modules import RoleDoc
from config import SITE_ID
from event import Event

SITE_ADMIN = 0x01
SITE_CHECKER = 0x02

CLUB_FOUNDER = 0x10
CLUB_MANAGER = 0x11
CLUB_MEMBER = 0x12

EVENT_SPONSOR = 0x21
EVENT_ASSISTANT = 0x22
EVENT_PARTICIPANT = 0x23

ALBUM_FOUNDER = 0x31
ALBUM_EDITOR = 0x32

WEIBO_OWNER = 0x41

class Role(API):
    def __init__(self):
        DB_CON.register([RoleDoc])
        datastore = DB_CON[DB_NAME]
        col_name = RoleDoc.__collection__
        collection = datastore[col_name]
        doc = collection.RoleDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def perm(self, user, subject, xid=None):
        return super(TimeLineAPI, self).create(user=user, subject=subject, xid=xid)
    
    def ban(self, user, subject, xid=None):
        r = super(TimeLineAPI, self).one(user=user, subject=subject, xid=xid)
        return self.remove(r[1])
    
    def inquire(self, user, subject, xid=None):
        if user in [u'53ea291bfa3e4d7dbb97fe367dab385e', u'2d40119715674d82a38216009efe528e']:
            return SITE_ADMIN
        r = self.one(user=user, subject=u'site', xid=SITE_ID)
        if r[0]:#subject == u'site'
            return SITE_CHECKER
        r = self.one(user=user, subject=u'club', xid=xid)
        if r[0]:#subject == u'club':
            return CLUB_FOUNDER
        r = self.one(user=user, subject=u'event', xid=xid)
        if r[0]:#subject == u'event':
            return EVENT_SPONSOR
        r = self.one(user=user, subject=u'album', xid=xid)
        if r[0]:#subject == u'album':
            return ALBUM_FOUNDER
    
    
    