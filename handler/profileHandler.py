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
        self.render('login.html')
    
class RegisterHandler(BaseHandler):
    def get(self):
        self.render('register.html')
    
    def post(self):
        u = User()
        cek_ret = u._api.check_reg(**self.request.arguments)
        if cek_ret[0]:
            info = cek_ret[1]
            email = info['email']
        else:
            return self.render('register.html', **{'warning': cek_ret[1]})
        ret = u._api.create(**info)
        if ret[0]:
            u.whois('email', email)
            n = u.nick.encode('utf-8') if u.nick else u.email
            self.set_secure_cookie("user", n, 1)
            self.SESSION['uid']=u._id
            at = u.added.get('access_token', None)
            self.set_access_token(u.sina_id, at)
            self.skip_page()
        else:
            self.render('register.html', **{'warning': ret[1]})
    
class LogoutHandler(BaseHandler):
    def get(self):
        self.redirct('/')
    
class ProfileHandler(BaseHandler):
    def get(self):
        self.redirct('profile.html')
    
class SettingHandler(BaseHandler):
    def get(self):
        self.render('setting.html')