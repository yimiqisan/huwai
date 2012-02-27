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
        r = u.register(n, p, email=e)
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
    KEYS = ["nick", "domain", "avanta", "live", "mail", "phone"]
    
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        d = {}
        for n in self.KEYS:d[n] = None
        u = User()
        u.whois('_id', uid)
        if u.nick:d['nick'] = u.nick
        if u.domain:d['domain'] = u.domain
        if u.added.get('avanta', None):d['avanta'] = u.added['avanta']
        if u.live:d['live'] = u.live
        if u.email:d['mail'] = u.email
        if u.added.get('phone', None):d['phone'] = u.added['phone']
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
        u._api.edit(uid, **s)
        return self.redirect('/account/setting/')
#        self.render('profile/setting.html', **d)

class SettingAlertHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        d = {}
        self.render('profile/setting_alert.html', **d)
    
    @addslash
    @session
    def post(self):
        return self.redirect('/account/setting/alert/')

class SettingThirdPartHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        d = {}
        u = User()
        u.whois('_id', uid)
        if u.nick:d['sina_access_token'] = u.sina_access_token
        self.render('profile/setting_thirdpart.html', **d)
    
    @addslash
    @session
    def post(self):
        return self.redirect('/account/setting/thirdpart/')

class CpasswordHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        self.render("profile/cpassword.html")
    
    @addslash
    @session
    def post(self):
        uid = self.SESSION['uid']
        o= self.get_argument('oldpassword', None)
        if o is None:return self.render('profile/cpassword.html', **{'warning': '请输入旧密码'})
        n = self.get_argument('newpassword', None)
        if n is None:return self.render('profile/cpassword.html', **{'warning': '请输入新密码'})
        c = self.get_argument('confpassword', None)
        if c is None:return self.render('profile/cpassword.html', **{'warning': '请输入确认密码？'})
        u = User()
        u.whois("_id", uid)
        if (u.password != o):return self.render('profile/cpassword.html', **{'warning': '密码不正确'})
        if (n != c):return self.render('profile/cpassword.html', **{'warning': '新密码不匹配'})
        u._api.edit(uid, password=n)
        return self.redirect('/account/setting/')

class BindSinaHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        CALLBACK_URL = self.request.protocol+'://'+self.request.host+'/auth/sina/'
        client = APIClient(config.SINA_CONSUME_KEY, config.SINA_CONSUME_SECRET, CALLBACK_URL)
        code = self.get_argument('code', None)
        if code:
            r = client.request_access_token(code)
            access_token = r.access_token
            self.SESSION['sina_request_token'] = access_token
            client.set_access_token(access_token, r.expires_in)
            u = self.is_authed('sina_access_token', access_token)
            if u:
                self.set_secure_cookie("user", u.nick, 1)
                self.SESSION['uid']=u._id
                self.redirect('/account/profile')
            else:
                uid = client.get.account__get_uid().uid
                uinfo = client.get.users__show(uid=uid)
                #{'domain': u'yimiqisan', 'avatar_large': u'http://tp2.sinaimg.cn/1683546773/180/5603268482/1', 'id': 1683546773, 'location': u'\u5317\u4eac \u671d\u9633\u533a', 'name': u'\u4e00\u7c73\u4e03\u4e092010', 'gender': u'm'}
                extra_args = {'photo':uinfo['avatar_large'], 'sinaid':uinfo['id'], 'sina_access_token':access_token}
                self.render('profile/thirdpart.html', extra=extra_args, nick=uinfo['name'])
        else:
            url = client.get_authorize_url()
            self.redirect(url)


