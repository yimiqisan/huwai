#!/usr/bin/env python
# encoding: utf-8
"""
profile.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from base import BaseHandler

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')
        
    def post(self):
        self.render('login.html')
    
class RegisterHandler(BaseHandler):
    def get(self):
        self.render('register.html')
        
    def post(self):
        self.render('register.html')
    
class LogoutHandler(BaseHandler):
    def get(self):
        self.redirct('/')
    
class ProfileHandler(BaseHandler):
    def get(self):
        self.redirct('profile.html')
    
class SettingHandler(BaseHandler):
    def get(self):
        self.render('setting.html')