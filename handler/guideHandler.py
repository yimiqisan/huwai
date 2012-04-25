#!/usr/bin/env python
# encoding: utf-8
"""
guideHandler.py

Created by 刘 智勇 on 2011-11-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import json
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from huwai.apps.guide import Guide
from huwai.apps.tag import Tag
from huwai.apps.tools import session
from huwai.apps.perm import preperm
from datetime import datetime

class GuideHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        n = Guide()
        return self.render("guide/index.html")
