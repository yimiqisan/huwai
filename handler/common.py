#!/usr/bin/env python
# encoding: utf-8
"""
common.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from base import BaseHandler

class Error404Handler(BaseHandler):
    def get(self):
        self.write('404 not found')