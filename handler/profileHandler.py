#!/usr/bin/env python
# encoding: utf-8
"""
profile.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
from huwai import config

from baseHandler import BaseHandler

from apps.user import User
from apps.tools import session
from apps.oauth2 import APIClient



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

class ThirdPartHandler(BaseHandler):
    @session
    def get(self):
        return self.render('thirdpart.html', nick='朋友仔')
        CALLBACK_URL = self.request.protocol+'://'+self.request.host+'/account/thirdpart'
        client = APIClient(config.SINA_CONSUME_KEY, config.SINA_CONSUME_SECRET, CALLBACK_URL)
        code = self.get_argument('code', None)
        if code:
            r = client.request_access_token(code)
            access_token = r.access_token
            self.SESSION['sina_request_token'] = request_token
            client.set_access_token(access_token, r.expires_in)
            sinfo = client.account__profile__basic()
            self.render('thirdpart.html', nick=sinfo['name'])
        else:
            url = client.get_authorize_url()
            self.redirect(url)
    
    @session
    def post(self):
        a = self.get_argument('act', None)
        n = self.get_argument('nick', None)
        if n is None:return self.render('thirdpart.html', **{'warning': '请先报上名号'})
        p = self.get_argument('password', None)
        if p is None:return self.render('thirdpart.html', **{'warning': '您接头暗号是？'})
        u = User()
        sina_request_token = self.SESSION['sina_request_token']
        if a == 'reg':
            e= self.get_argument('email', None)
            if e is None:return self.render('thirdpart.html', **{'warning': '设置邮箱，可能帮您找回失散多年的密码'})
            r = u.register(n, e, p, sina_tk=sina_request_token)
            if r[0]:
                self.set_secure_cookie("user", n, 1)
                self.SESSION['uid']=u._id
                self.redirect('/account/profile')
            else:
                return self.render('thirdpart.html', **{'warning': r[1]})
        elif a == 'bind':
            r = u.login(n, p)
            if r[0]:
                u._api.edit(u._id, sina_tk=sina_request_token)
                self.set_secure_cookie("user", n, 1)
                self.SESSION['uid']=u._id
                self.redirect('/account/profile')
            else:
                return self.render('thirdpart.html', **{'warning': r[1]})
        else:
            return self.render('thirdpart.html', **{'warning': '系统晕了，不知道您是绑定还是注册！'})

class RegisterHandler(BaseHandler):
    def get(self):
        self.render('register.html')

    @session
    def post(self):
        n = self.get_argument('nick', None)
        if n is None:return self.render('register.html', **{'warning': '请先报上名号'})
        e= self.get_argument('email', None)
        if e is None:return self.render('register.html', **{'warning': '设置邮箱，可能帮您找回失散多年的密码'})
        p = self.get_argument('password', None)
        if p is None:return self.render('register.html', **{'warning': '您接头暗号是？'})
        u = User()
        r = u.register(n, e, p)
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