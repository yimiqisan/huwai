#!/usr/bin/env python
# encoding: utf-8
"""
authHandler.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
from huwai import config

import tornado
from tornado.web import addslash
from baseHandler import BaseHandler

from huwai.apps.user import User
from huwai.apps.tools import session
from huwai.apps.oauth2 import APIClient, QQGraphMixin, RenrenGraphMixin
from huwai.apps.pstore import AvatarProcessor


class AuthHandler(BaseHandler):
    @session
    def bind_user(self, **extra):
        uid = self.SESSION['uid']
        u = User()
        r = u._api.edit(uid, **extra)
        if r[0]:
            self.redirect('/account/profile/')
        else:
            return self.redirect('/account/setting/thirdpart/', **{'warning': r[1]})
    
    @session
    def add_user(self, **extra):
        u = User()
        n = extra.pop('nick')
        if u._api.is_nick_exist(n):return self.render('profile/auth.html', **{'warning': '名称已存在', 'nick': n, 'extra': extra})
        r = u.register(n, **extra)
        if r[0]:
            self.SESSION['uid']=u._id
            self.SESSION['nick']=n
            if extra.has_key('photo'):self.save_avatar(extra['photo'])
            u._api.edit(u._id, **extra)
            return self.render('ajax/runjs.html', uid=u._id)
        else:
            return self.render('profile/auth.html', **{'warning': r[1], 'nick': n, 'extra': extra})
    
    @addslash
    @session
    def post(self):
        u = User()
        n = self.get_argument('nick', None)
        extra = self.get_argument('extra', {})
        if isinstance(extra, unicode):extra=eval(extra)
        if not n:return self.render('profile/auth.html', **{'warning': '名称为空', 'nick': n, 'extra': extra})
        extra['nick'] = n
        self.add_user(**extra)
    
    @session
    def is_authed(self, key, value):
        u = User()
        u.whois(key, value)
        if u.uid is None:
            return False
        else:
            self.SESSION['uid']=u._id
            self.SESSION['nick']=u.nick
            self.render('ajax/runjs.html', uid=u._id)
            return True
    
    def save_avatar(self, photo_url):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch(photo_url, self.async_callback(self._on_save_avatar))
    
    @session
    def _on_save_avatar(self, response):
        uid = self.SESSION['uid']
        p=AvatarProcessor(uid)
        r = p.process(response.body)
        self.finish()

class SinaLoginHandler(AuthHandler):
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        CALLBACK_URL = self.request.protocol+'://'+self.request.host+'/auth/sina/'
        client = APIClient(config.SINA_CONSUME_KEY, config.SINA_CONSUME_SECRET, CALLBACK_URL)
        code = self.get_argument('code', None)
        if code:
            r = client.request_access_token(code)
            access_token = r.access_token
            self.SESSION['sina_request_token'] = access_token
            client.set_access_token(access_token, r.expires_in)
            u = self.is_authed('sina_access_token', access_token)
            if not u:
                sinaid = client.get.account__get_uid().uid
                uinfo = client.get.users__show(uid=sinaid)
                if uid:
                    kwargs = {'sinaid':uinfo['id'], 'sina_access_token':access_token}
                    self.bind_user(**kwargs)
                else:
                    kwargs = {'nick':uinfo['name'], 'photo':uinfo['avatar_large'], 'sinaid':uinfo['id'], 'sina_access_token':access_token}
                    self.add_user(**kwargs)
        else:
            url = client.get_authorize_url()
            self.redirect(url)

class SinaHandler(BaseHandler):
    pass

class QQLoginHandler(AuthHandler, QQGraphMixin):
    @addslash
    @session
    @tornado.web.asynchronous
    def get(self):
        CALLBACK_URL = self.request.protocol+'://'+self.request.host+'/auth/qq/'
        code = self.get_argument('code', False)
        if code:
            self.get_authenticated_user(redirect_uri=CALLBACK_URL,client_id=config.QQ_CONSUME_KEY,client_secret=config.QQ_CONSUME_SECRET,code=code, callback=self.async_callback(self._on_login))
        else:
            self.authorize_redirect(redirect_uri=CALLBACK_URL,client_id=config.QQ_CONSUME_KEY,extra_params={"display":"default", "response_type":"code"})
    
    def _on_login(self, response):
        u = self.is_authed('qqid', response['openid'])
        if u:
            self.SESSION['uid']=u._id
            self.SESSION['uid']=u.nick
            self.render('ajax/runjs.html', uid=u._id)
        else:
            self.qq_request(path="/user/get_user_info", callback=self.async_callback(self._on_get_user_info, self._on_register, response['fields'], response['openid']), access_token=response['session']["access_token"], openid=response['openid'], oauth_consumer_key=response['client_id'], fields=",".join(response['fields']))
    
    @session
    def _on_register(self, response):
        uid = self.SESSION['uid']
        if uid:
            kwargs = {'qqid':unicode(response['qqid'])}
            self.bind_user(**kwargs)
        else:
            kwargs = {'nick':response['nickname'], 'photo':response['figureurl_2'], 'qqid':unicode(response['qqid'])}
            self.add_user(**kwargs)

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

class RenrenLoginHandler(AuthHandler, RenrenGraphMixin):
    @addslash
    @session
    def get(self):
        CALLBACK_URL = self.request.protocol+'://'+self.request.host+'/auth/renren/'
        code = self.get_argument('code', False)
        if code:
            self.get_authenticated_user(redirect_uri=CALLBACK_URL,client_id=config.RENREN_CONSUME_KEY,client_secret=config.RENREN_CONSUME_SECRET,code=code, callback=self.async_callback(self._on_login))
        else:
            self.authorize_redirect(redirect_uri=CALLBACK_URL,client_id=config.RENREN_CONSUME_KEY,extra_params={"display":"default", "response_type":"code"})
    
    def post(self):
        verification_code = self.request.get("code")
        args = dict(client_id=RENREN_APP_API_KEY, redirect_uri=self.request.path_url)
        error = self.request.get("error")
        if error:
            args["error"] = error
            args["error_description"] = self.request.get("error_description")
            args["error_uri"] = self.request.get("error_uri")
            path = os.path.join(os.path.dirname(__file__), "error.html")
            args = dict(error=args)
            self.response.out.write(template.render(path, args))
        elif verification_code:
            scope = self.request.get("scope")
            scope_array = str(scope).split("[\\s,+]")
            response_state = self.request.get("state")
            args["client_secret"] = RENREN_APP_SECRET_KEY
            args["code"] = verification_code
            args["grant_type"] = "authorization_code"
            response = urllib.urlopen(RENREN_ACCESS_TOKEN_URI + "?" + urllib.urlencode(args)).read()
            access_token = _parse_json(response)["access_token"]
            '''Obtain session key from the Resource Service.'''
            session_key_request_args = {"oauth_token": access_token}
            response = urllib.urlopen(RENREN_SESSION_KEY_URI + "?" + urllib.urlencode(session_key_request_args)).read()
            session_key = str(_parse_json(response)["renren_token"]["session_key"])
            '''Requesting the Renren API Server obtain the user's base info.'''
            params = {"method": "users.getInfo", "fields": "name,tinyurl"}
            api_client = RenRenAPIClient(session_key, RENREN_APP_API_KEY, RENREN_APP_SECRET_KEY)
            response = api_client.request(params);
            if type(response) is list:
                response = response[0]
            user_id = response["uid"]#str(access_token).split("-")[1]
            name = response["name"]
            avatar = response["tinyurl"]
            user = User(key_name = unicode(user_id), id = unicode(user_id), name = unicode(name), avatar = unicode(avatar), access_token = access_token)
            user.put()
            set_cookie(self.response, "renren_user", str(user_id), expires=time.time() + 30 * 86400)
            self.redirect("/")
        else:
            args["response_type"] = "code"
            args["scope"] = "publish_feed email status_update"
            args["state"] = "1 23 abc&?|."
            self.redirect(RENREN_AUTHORIZATION_URI + "?" +urllib.urlencode(args))


class ThirdPartHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        self.render('profile/thirdpart.html', **{'nick': '', 'extra': {}})
        
    @addslash
    @session
    def post(self):
        a = self.get_argument('act', None)
        extra = self.get_argument('extra', None)
        n = self.get_argument('nick', None)
        if n is None:return self.render('profile/thirdpart.html', **{'warning': '请先报上名号', 'nick': n, 'extra': extra})
        p = self.get_argument('password', None)
        if p is None:return self.render('profile/thirdpart.html', **{'warning': '您接头暗号是？', 'nick': n, 'extra': extra})
        if extra: extra=eval(extra)
        u = User()
        if a == 'reg':
            e= self.get_argument('email', None)
            if e is None:return self.render('profile/thirdpart.html', **{'warning': '设置邮箱，可能帮您找回失散多年的密码', 'nick': n, 'extra': extra})
            r = u.register(n, e, p)
            if r[0]:
                self.set_secure_cookie("user", n, 1)
                uid = r[1]
                self.SESSION['uid']=uid
                if extra.has_key('photo'):self.save_avatar(extra['photo'])
                if extra.has_key('qqid'):u._api.edit(uid, qqid=extra['qqid'])
                if extra.has_key('sinaid'):u._api.edit(uid, sinaid=extra['sinaid'])
                if extra.has_key('sina_access_token'):u._api.edit(uid, sina_access_token=extra['sina_access_token'])
                self.redirect('/account/profile')
            else:
                return self.render('profile/thirdpart.html', **{'warning': r[1], 'nick': n, 'extra': extra})
        elif a == 'bind':
            pass
        else:
            return self.render('profile/thirdpart.html', **{'warning': '系统晕了，不知道您是绑定还是注册！', 'nick': n, 'extra': extra})
    
    def save_avatar(self, photo_url):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch(photo_url, self.async_callback(self._on_save_avatar))
    
    @session
    def _on_save_avatar(self, response):
        uid = self.SESSION['uid']
        p=AvatarProcessor(uid)
        r = p.process(response.body)
        self.finish()

