#!/usr/bin/env python
# encoding: utf-8
"""
common.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from baseHandler import BaseHandler

class RootHandler(BaseHandler):
    def get(self):
        self.render("index.html")

class TestHandler(BaseHandler):
    def get(self):
        self.render("google.html")

class FeedbackHandler(BaseHandler):
    def get(self):
        self.render("feedback.html")

class Error404Handler(BaseHandler):
    def get(self):
        self.render("404.html")