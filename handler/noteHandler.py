#!/usr/bin/env python
# encoding: utf-8
"""
weiboHandler.py

Created by 刘 智勇 on 2011-11-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import json
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from huwai.apps.note import Note
from huwai.apps.tag import Tag
from huwai.apps.tools import session
from huwai.apps.perm import preperm
from datetime import datetime

class NoteHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        n = Note()
        r = n._api.list()
        return self.render("note/index.html", note_l = r[1])

class NoteItemHandler(BaseHandler):
    @addslash
    @session
    def get(self, id):
        uid = self.SESSION['uid']
        n = Note()
        r = n._api.get(id, cuid=uid)
        if r[0]:
            return self.render("note/item.html", **r[1])
        else:
            return self.render("note/item.html", warning=r[1])

class NoteEditHandler(BaseHandler):
    @addslash
    @session
    @preperm(keys=['FOUNDER', 'VERIFIER', 'NORMAL'])
    def get(self, id):
        uid = self.SESSION['uid']
        return self.render("note/write.html", id=id)

class NoteDeleteHandler(BaseHandler):
    @addslash
    @session
    @preperm()
    def get(self, id):
        uid = self.SESSION['uid']
        n = Note()
        n._api.remove(id, cuid=uid)
        return self.redirect("/note")

class NoteWriteHandler(BaseHandler):
    @addslash
    @session
    @preperm(keys=['FOUNDER', 'VERIFIER', 'NORMAL'])
    def get(self):
        uid = self.SESSION['uid']
        return self.render("note/write.html", id="")
    
    @addslash
    @session
    def post(self):
        uid = self.SESSION['uid']
        t = self.get_argument("note_title", None)
        e = self.get_argument("note_text", None)
        n = Note()
        r = n._api.save(uid, t, e)
        return self.redirect("/note")

class AjaxNoteHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        nid = self.get_argument("nid", None)
        n = Note()
        r = n._api.get(nid, cuid=uid)
        if r[0]:
            d = r[1]
            d['content'] = d['content'].replace('</br>', '\r\n')
            return self.write({'info':d})
        else:
            return self.write({'error':r[1]})
    
    @addslash
    @session
    def post(self):
        uid = self.SESSION['uid']
        nid = self.get_argument("nid", None)
        nt = self.get_argument("note_title", None)
        nc = self.get_argument("note_text", None)
        ng = self.get_argument("note_tag", None)
        n = Note()
        nc = unicode(nc.replace('\r\n', '</br>').replace('\n', '</br>').replace('\r', '</br>'))
        ng = self._flt_tags(ng)
        if nid is None:
            r = n._api.save(uid, nt, nc, tags=ng)
        else:
            r = n._api.edit(nid, title=nt, content=nc, tags=ng)
        if r[0]:
            return self.write({'info':r[1]})
        else:
            return self.write({'error':'save error'})
    
    def _flt_tags(self, content):
        t = Tag()
        return t._api.content2id(content)
    
    
    
    
    