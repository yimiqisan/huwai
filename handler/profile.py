#!/usr/bin/env python
# encoding: utf-8
"""
profile.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from base import BaseHandler

class ProfileHandler(BaseHandler):
    def get(self):
        self.write('ok')