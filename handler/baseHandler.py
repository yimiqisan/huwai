#!/usr/bin/env python
# encoding: utf-8
"""
base.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from tornado.web import RequestHandler
from huwai.apps.tools import session
from huwai.config import DB_CON

class BaseHandler(RequestHandler):
    @property
    def db(self):
        return DB_CON
        
    @property
    def cache(self):
        return self.settings["cache_engine"]
    
    @session
    def get_current_user(self):
        return self.SESSION['nick']
    
    @session
    def render(self, template_name, **kwargs):
        kwargs['uid'] = self.SESSION['uid']
        kwargs['warning'] = kwargs.get('warning', None)
        kwargs['page_title'] = kwargs.get('page_title', None)
        kwargs['meta_kws'] = kwargs.get('meta_kws', None)
        kwargs['meta_desp'] = kwargs.get('meta_desp', None)
        super(BaseHandler, self).render(template_name, **kwargs)
    
    @session
    def render_alert(self, msg, **kwargs):
        kwargs['alert']=msg
        self.render('alert.html', **kwargs)
    