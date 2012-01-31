#!/usr/bin/env python
# encoding: utf-8
"""
profile.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
from huwai import config

from tornado.web import addslash
from baseHandler import BaseHandler

from apps.user import User
from apps.tools import session
from apps.oauth2 import APIClient



class LoginHandler(BaseHandler):
    @addslash
    def get(self):
        n = self.get_argument('next', '')
        self.render('profile/login.html', n=n)
    
    @addslash
    @session
    def post(self):
        n = self.get_argument('nick', None)
        if n is None:return self.render('login.html', **{'warning': '请先报上名号'})
        p = self.get_argument('password', None)
        if p is None:return self.render('login.html', **{'warning': '您接头暗号是？'})
        nt = self.get_argument('next', None)
        u = User()
        r = u.login(n, p)
        if r[0]:
            self.set_secure_cookie("user", n, 1)
            self.SESSION['uid']=u._id
            self.redirect(nt) if nt else self.redirect('/account/profile')
        else:
            return self.render('profile/login.html', **{'warning': r[1]})

class InviteHandler(BaseHandler):
    @addslash
    def get(self):
        self.write('invite')
    
    @addslash
    def post(self):
        mail = self.get_argument('mail')
        u = User()
        r = u.invite(mail)
        if r[0]:
            return self.render_alert(u"发送成功")
        else:
            return self.render('index.html', **{'warning': '邀请邮件发送失败'})

class ThirdPartHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        CALLBACK_URL = self.request.protocol+'://'+self.request.host+'/account/thirdpart'
        client = APIClient(config.SINA_CONSUME_KEY, config.SINA_CONSUME_SECRET, CALLBACK_URL)
        code = self.get_argument('code', None)
        if code:
            r = client.request_access_token(code)
            access_token = r.access_token
            self.SESSION['sina_request_token'] = access_token
            client.set_access_token(access_token, r.expires_in)
            sinfo = client.get.account__profile__basic()
            self.render('profile/thirdpart.html', nick=sinfo['name'])
        else:
            url = client.get_authorize_url()
            self.redirect(url)
    
    @addslash
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
                return self.render('profile/thirdpart.html', **{'warning': r[1]})
        elif a == 'bind':
            r = u.login(n, p)
            if r[0]:
                u._api.edit(u._id, sina_tk=sina_request_token)
                self.set_secure_cookie("user", n, 1)
                self.SESSION['uid']=u._id
                self.redirect('/account/profile')
            else:
                return self.render('profile/thirdpart.html', **{'warning': r[1]})
        else:
            return self.render('profile/thirdpart.html', **{'warning': '系统晕了，不知道您是绑定还是注册！'})

class RegisterHandler(BaseHandler):
    @addslash
    def get(self):
        icode = self.get_argument('icode', None)
        u = User()
        r = u.is_invited(icode)
        if r:
            return self.render('profile/register.html', email=r)
        else:
            return self.render_alert(u"邀请不可用")
    
    @addslash
    @session
    def post(self):
        e= self.get_argument('email', None)
        if e is None:return self.render('profile/register.html', **{'warning': '设置邮箱，可能帮您找回失散多年的密码', 'email':e})
        n = self.get_argument('nick', None)
        if n is None:return self.render('profile/register.html', **{'warning': '请先报上名号', 'email':e})
        p = self.get_argument('password', None)
        if p is None:return self.render('profile/register.html', **{'warning': '您接头暗号是？', 'email':e})
        u = User()
        r = u.register(n, e, p)
        if r[0]:
            self.set_secure_cookie("user", n, 1)
            self.SESSION['uid']=u._id
            self.redirect('/account/profile')
        else:
            return self.render('profile/register.html', **{'warning': r[1], 'email':e})
    
class LogoutHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        self.clear_cookie("user")
        del self.SESSION['uid']
        nt = self.get_argument('next', None)
        self.redirect(nt) if nt else self.redirect('/')

class ProfileHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        if self.current_user:
            title = self.current_user+'的主页'
            self.render('profile/profile.html', title=title)
        else:
            self.redirect('/')
    
class SettingHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        self.render('profile/setting.html', uid=uid)
    
    @addslash
    @session
    def post(self):
        self.render('profile/setting.html')