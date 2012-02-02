#!/usr/bin/env python
# encoding: utf-8
"""
profile.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
from huwai import config

import tornado
from tornado.web import addslash
from baseHandler import BaseHandler

from apps.user import User
from apps.tools import session
from apps.oauth2 import APIClient, QQGraphMixin


class LoginHandler(BaseHandler):
    @session
    def is_authed(self, key, value):
        u = User()
        u.whois(key, value)
        if u.uid is None:
            return False
        else:
            return u

class SinaLoginHandler(LoginHandler):
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
            sinfo = client.get.account__profile__basic()
            ## TO DO SAVE
        else:
            url = client.get_authorize_url()
            self.redirect(url)

class QQLoginHandler(LoginHandler, QQGraphMixin):
    @addslash
    @session
    @tornado.web.asynchronous
    def get(self):
        CALLBACK_URL = self.request.protocol+'://'+self.request.host+'/auth/qq/'
        code = self.get_argument('code', False)
        if code:
            self.get_authenticated_user(redirect_uri=CALLBACK_URL,client_id=config.QQ_CONSUME_KEY,client_secret=config.QQ_CONSUME_SECRET,code=code,\
                callback=self.async_callback(self._on_login))
        else:
            self.authorize_redirect(redirect_uri=CALLBACK_URL,client_id=config.QQ_CONSUME_KEY,extra_params={"display":"default", "response_type":"code"})
    
    def _on_login(self, response):
        u = self.is_authed('qqid', response['openid'])
        if u:
            self.set_secure_cookie("user", n, 1)
            self.SESSION['uid']=u._id
            self.redirect(nt) if nt else self.redirect('/account/profile')
        else:
            self.qq_request(path="/user/get_user_info", callback=self.async_callback(self._on_get_user_info, self._on_register, response['fields']), access_token=response['session']["access_token"], openid=response['openid'], oauth_consumer_key=response['client_id'], fields=",".join(response['fields']))
        self.finish()
        
    def _on_register(self, response):
        self.render('profile/thirdpart.html', nick=response['nickname'], photo=response['figureurl_2'])

class QQHandler(BaseHandler, QQGraphMixin):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        self.qq_request(
            "/me/feed",
            post_args={"message": "I am posting from my Tornado application!"},
            access_token=self.current_user["access_token"],
            callback=self.async_callback(self._on_post))
    
    def _on_post(self, new_entry):
        if not new_entry:
            # Call failed; perhaps missing permission?
            self.authorize_redirect()
            return
        self.finish("Posted a message!")

class ThirdPartHandler(BaseHandler):
    @addslash
    @session
    def post(self):
        a = self.get_argument('act', None)
        n = self.get_argument('nick', None)
        if n is None:return self.render('profile/thirdpart.html', **{'warning': '请先报上名号'})
        p = self.get_argument('password', None)
        if p is None:return self.render('profile/thirdpart.html', **{'warning': '您接头暗号是？'})
        o = self.get_argument('photo', None)
        u = User()
#        sina_request_token = self.SESSION['sina_request_token']
        if a == 'reg':
            e= self.get_argument('email', None)
            if e is None:return self.render('profile/thirdpart.html', **{'warning': '设置邮箱，可能帮您找回失散多年的密码'})
            r = u.register(n, e, p)
            if r[0]:
                if o:print o
                self.set_secure_cookie("user", n, 1)
                self.SESSION['uid']=u._id
                self.redirect('/account/profile')
            else:
                return self.render('profile/thirdpart.html', **{'warning': r[1]})
        elif a == 'bind':
            r = u.login(n, p)
            if r[0]:
                u._api.edit(u._id)
                self.set_secure_cookie("user", n, 1)
                self.SESSION['uid']=u._id
                self.redirect('/account/profile')
            else:
                return self.render('profile/thirdpart.html', **{'warning': r[1]})
        else:
            return self.render('profile/thirdpart.html', **{'warning': '系统晕了，不知道您是绑定还是注册！'})
