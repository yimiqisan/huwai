#!/usr/bin/env python
# encoding: utf-8
"""
base.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from tornado.web import RequestHandler
from apps.tools import session

class BaseHandler(RequestHandler):
    @property
    def db(self):
        return DB_CON
        
    @property
    def cache(self):
        return self.settings["cache_engine"]
        
    def get_current_user(self):
        return self.get_secure_cookie("user")
    
    @session
    def render(self, template_name, **kwargs):
        kwargs['uid'] = self.SESSION['uid']
        kwargs['warning'] = kwargs.get('warning', None)
        super(BaseHandler, self).render(template_name, **kwargs)
    
    @session
    def render_alert(self, msg, **kwargs):
        kwargs['alert']=msg
        kwargs['leftnav']=kwargs.get('leftnav', [])
        self.render('alert.html', **kwargs)