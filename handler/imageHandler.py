#!/usr/bin/env python
# encoding: utf-8
"""
imageHandler.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
from tornado.web import addslash

from baseHandler import BaseHandler
from huwai.apps.pstore import Pstore, AvatarProcessor, AttachProcessor
from huwai.apps.tools import session

class AvatarHandler(BaseHandler):
    def get(self, fn=None):
        if not fn:return
        v = self.get_argument('v', None)
        p=AvatarProcessor()
        kwargs = {}
        kwargs['version']=v
        self.write(p.display(fn, **kwargs))

class AttachHandler(BaseHandler):
    def get(self, fn=None):
        if not fn:return
        v = self.get_argument('v', None)
        p=AttachProcessor()
        kwargs = {}
        kwargs['version']=v
        self.write(p.display(fn, **kwargs))

class UploadImageHandler(BaseHandler):
    def get(self):
        pid = self.get_argument("pid", None)
        self.render('upload_image.html', pid=pid)
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        p=AvatarProcessor(uid)
        f=self.request.files['upload'][0]
        r = p.process(f['body'])
        self.redirect('/image/upload?pid='+r)
    
class AjaxAvatarHandler(BaseHandler):
    @session
    def post(self):
        #uid = self.SESSION['uid']
        uid = self.get_argument('uid', None)
        p=AvatarProcessor(uid)
        f=self.request.files['upload'][0]
        r = p.process(f['body'])
        return self.write(uid)

class AjaxImageHandler(BaseHandler):
    @session
    def post(self):
        #uid = self.SESSION['uid']
        uid = self.get_argument('uid', None)
        p=AttachProcessor()
        f=self.request.files['upload'][0]
        r = p.process(f['body'])
        return self.write(r)

class AjaxImageDeleteHandler(BaseHandler):
    @session
    def post(self):
        uid = self.SESSION['uid']
        pid = self.get_argument('pid', None)
        p=Pstore()
        r = p.delete(pid)
        return self.write({'ret':'ok'})

class AjaxImageCheckHandler(BaseHandler):
    def post(self):
        return True










