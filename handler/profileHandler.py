#!/usr/bin/env python
# encoding: utf-8
"""
profile.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from baseHandler import BaseHandler
from apps.user import User
from apps.tools import session

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')
    
    @session
    def post(self):
        n = self.get_argument('nick', None)
        if n is None:return self.render('login.html', **{'warning': '请先报上名号'})
        p = self.get_argument('password', None)
        if p is None:return self.render('login.html', **{'warning': '您接头暗号是？'})
        u = User()
        r = u.login(n, p)
        if r[0]:
            self.set_secure_cookie("user", n, 1)
            self.SESSION['uid']=u._id
            self.redirect('/account/profile')
        else:
            return self.render('login.html', **{'warning': r[1]})

class RegisterHandler(BaseHandler):
    def get(self):
        self.render('register.html')

    @session
    def post(self):
        n = self.get_argument('nick', None)
        if n is None:return self.render('register.html', **{'warning': '请先报上名号'})
        p = self.get_argument('password', None)
        if p is None:return self.render('register.html', **{'warning': '您接头暗号是？'})
        u = User()
        r = u.register(n, p)
        if r[0]:
            self.set_secure_cookie("user", n, 1)
            self.SESSION['uid']=u._id
            self.redirect('/account/profile')
        else:
            return self.render('register.html', **{'warning': r[1]})
    
class LogoutHandler(BaseHandler):
    @session
    def get(self):
        self.clear_cookie("user")
        del self.SESSION['uid']
        self.redirect('/')
    
class ProfileHandler(BaseHandler):
    @session
    def get(self):
        self.render('profile.html')
    
class SettingHandler(BaseHandler):
    @session
    def get(self):
        self.render('setting.html')
    
    @session
    def post(self):
        self.render('setting.html')