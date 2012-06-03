#!/usr/bin/env python
# encoding: utf-8
"""
wikiHandler.py

Created by 刘 智勇 on 2012-05-10.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import json
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from huwai.apps.note import Note
from huwai.apps.tag import Tag
from huwai.apps.tools import session, calc
from huwai.apps.perm import preperm
from datetime import datetime

class WikiHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        self.render('wiki/index.html')

class WikiItemHandler(BaseHandler):
    @addslash
    @session
    def get(self, id):
        self.render('wiki/item.html')

class WikiEditHandler(BaseHandler):
    @addslash
    @session
    def get(self, id):
        self.render('wiki/edit.html')
