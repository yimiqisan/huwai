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
from huwai.apps.tools import session
from datetime import datetime

class NoteHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        n = Note()
        r = n._api.list(owner=uid)
        return self.render("note/index.html", note_l = r[1])

class NoteWriteHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        uid = self.SESSION['uid']
        return self.render("note/write.html")
    
    @addslash
    @session
    def post(self):
        uid = self.SESSION['uid']
        t = self.get_argument("note_title", None)
        e = self.get_argument("note_text", None)
        n = Note()
        r = n._api.save(uid, t, e)
        return self.render("note/write.html")

class AjaxNoteHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        pass
    
    @addslash
    @session
    def post(self):
        uid = self.SESSION['uid']
        t = self.get_argument("note_title", None)
        e = self.get_argument("note_text", None)
        n = Note()
        r = n._api.save(uid, t, e)
        if r[0]:
            return self.write({'info':r[1]})
        else:
            return self.write({'error':'save error'})

    
    
    
    
        
        
        
        
        
        
        
        