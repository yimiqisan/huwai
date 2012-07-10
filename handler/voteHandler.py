#!/usr/bin/env python
# encoding: utf-8
"""
voteHandler.py

Created by 刘 智勇 on 2012-06-26.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import json
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from huwai.apps.vote import Vote
from huwai.apps.tools import session
from huwai.apps.perm import preperm
from datetime import datetime

class VoteHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        self.render('vote/index.html')
    
    @addslash
    @session
    def post(self):
        pass
