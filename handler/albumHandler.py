#!/usr/bin/env python
# encoding: utf-8
"""
albumHandler.py

Created by 刘 智勇 on 2012-03-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import json
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from huwai.apps.pstore import AttachProcessor
from huwai.apps.album import Album
from huwai.apps.tools import session

class AlbumHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        a = Album()
        r = a._api.list(owner=uid)
        if r[0]:
            return self.render("album/index.html", album_list=r[1])
        else:
            return self.render("album/index.html", warning=r[1])

class AlbumCreateHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        return self.render("album/create.html")
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        t = self.get_argument('title', None)
        c = self.get_argument('content', None)
        rel = self.get_argument('relation', None)
        tags = self.get_argument('tags', None)
        allowed = int(self.get_argument('allowed', 0x01))
        a = Album()
        r = a._api.build(uid, t, c, relation=rel, tags=tags, allowed=allowed)
        if r[0]:
            return self.redirect("/album/%s/"%r[1])
        else:
            return self.render("album/create.html", warning=r[1])
    
class AlbumItemHandler(BaseHandler):
    @session
    def get(self, id):
        uid = self.SESSION['uid']
        a = Album()
        r = a._api.get(id)
        return self.render("album/item.html", **r[1])

class AjaxAlbumUploadHandler(BaseHandler):
    @session
    def post(self):
        uid = self.get_argument('uid', None)
        aid = self.get_argument('aid', None)
        p=AttachProcessor()
        f = self.request.files['upload'][0]
        r = p.process(f['body'])
        a = Album()
        ra = a._api.push(aid, r)
        return self.write(r)

class AjaxAlbumDeleteHandler(BaseHandler):
    @session
    def post(self):
        uid = self.SESSION['uid']
        pid = self.get_argument('pid', None)
        p=AvatarProcessor(uid)
        r = p.remove(pid)
        return self.write({'ret':'ok'})

class AjaxAlbumHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        a = Album()
        r = a._api.page()
        if r[0]:
            return self.write(json.dumps({"data":r[1], 'pagination':r[2]}))
        else:
            return self.write({'error':'save error'})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        a = Album()
        r = a._api.madd(uid, c, relation_l=e)
        if r[0]:
            return self.write(json.dumps({'id':r[1]}))
        else:
            return self.write({'error':'save error'})
    