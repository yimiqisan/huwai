#!/usr/bin/env python
# encoding: utf-8
"""
imageHandler.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from baseHandler import BaseHandler
from apps.pstore import AvatarProcessor, AttachProcessor
from apps.tools import session

class AvatarHandler(BaseHandler):
    def get(self, fn=None):
        if not fn:return
        v = self.get_argument('v', None)
        p=AvatarProcessor()
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

