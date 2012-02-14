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
        if n is None:return self.render('login.html', **{'warning': '请先报上名号', 'n':n})
        p = self.get_argument('password', None)
        if p is None:return self.render('login.html', **{'warning': '您接头暗号是？', 'n':n})
        nt = self.get_argument('next', None)
        u = User()
        r = u.login(n, p)
        if r[0]:
            self.set_secure_cookie("user", n, 1)
            self.SESSION['uid']=u._id
            self.redirect(nt) if nt else self.redirect('/account/profile')
        else:
            return self.render('profile/login.html', **{'warning': r[1], 'n':n})

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

class RegisterHandler(BaseHandler):
    @addslash
    def get(self):
        return self.render('profile/register.html')
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
            self.SESSION['uid']=r[1]
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
        self.redirect('/')

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
    KEYS = ["nick", "domain", "avanta", "live", "mail", "password", "phone"]
    
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        d = {'ifNone':self.ifNone}
        for n in self.KEYS:d[n] = None
        u = User()
        u.whois('_id', uid)
        if u.nick:d['nick'] = u.nick
        if u.domain:d['domain'] = u.domain
        if u.avanta:d['avanta'] = u.avanta
        if u.live:d['live'] = u.live
        if u.email:d['mail'] = u.email
        if u.phone:d['phone'] = u.phone
        self.render('profile/setting.html', **d)
    
    @addslash
    @session
    def post(self):
        uid = self.SESSION['uid']
        u = User()
        d = {}
        s = {}
        for n in self.KEYS:
            d[n] = self.get_argument(n, None)
            if d[n]:s[n]=d[n]
        print d
        print s
#        u._api.edit(uid, **d)
        d['ifNone'] = self.ifNone
        self.render('profile/setting.html', **d)
