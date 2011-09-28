#!/usr/bin/env python
# encoding: utf-8
"""
profile.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from base import BaseHandler
from apps.user import User

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')
        
    def post(self):
        u = User()
        n = self.get_argument('nick', None)
        if n is None:return self.render('login.html', **{'warning': '请先报上名号'})
        p = self.get_argument('password', None)
        if p is None:return self.render('login.html', **{'warning': '您接头暗号是？'})
        r = u._api.login(n, p)
        if r[0]:
            self.set_secure_cookie("user", n, 1)
            self.redirect('/account/profile')
        else:
            return self.render('login.html', **{'warning': r[1]})
    
class RegisterHandler(BaseHandler):
    def get(self):
        self.render('register.html')
    
    def post(self):
        u = User()
        n = self.get_argument('nick', None)
        if n is None:return self.render('register.html', **{'warning': '请先报上名号'})
        p = self.get_argument('password', None)
        if p is None:return self.render('register.html', **{'warning': '您接头暗号是？'})
        r = u._api.register(n, p)
        if r[0]:
            self.set_secure_cookie("user", n, 1)
            self.redirect('/account/profile')
        else:
            return self.render('register.html', **{'warning': r[1]})
    
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect('/')
    
class ProfileHandler(BaseHandler):
    def get(self):
        self.render('profile.html')
    
class SettingHandler(BaseHandler):
    def get(self):
        self.render('setting.html')