#!/usr/bin/env python
# encoding: utf-8
"""
tagHandler.py

Created by 刘 智勇 on 2012-03-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import json
from tornado.web import addslash, authenticated

from baseHandler import BaseHandler
from huwai.apps.tag import Tag
from huwai.apps.tools import session

class TagHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        t = Tag()
        r = t._api.list()
        if r[0]:
            return self.render("tag/index.html", tags=r[1])
        else:
            return self.render("tag/index.html", tags=[], warning=r[1])

class TagItemHandler(BaseHandler):
    @session
    def get(self, id):
        uid = self.SESSION['uid']
        t = Tag()
        r = t._api.get(id)
        if r[0]:
            return self.render("tag/item.html", **r[1])
        else:
            return self.render("tag/item.html", warning=r[1])

class AjaxTagHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        rel = self.get_argument("rel", None)
        search = self.get_argument("search", None)
        t = Tag()
        r = t._api.list(rels=rel, content=search)
        if r[0]:
            return self.write(json.dumps({"data":r[1]}))
        else:
            return self.write({'error':'save error'})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        c = self.get_argument("content", None)
        e = self.get_argument("rel", None)
        t = Tag()
        r = t._api.madd(uid, c, relation_l=e)
        if r[0]:
            return self.write(json.dumps({'id':r[1]}))
        else:
            return self.write({'error':'save error'})
    
class AjaxTagListHandler(BaseHandler):
    @session
    def get(self):
        uid = self.SESSION['uid']
        rel = self.get_argument("rel", None)
        search = self.get_argument("search", None)
        t = Tag()
        r = t._api.list(rels=rel, content=search)
        if r[0]:
            return self.write(json.dumps({"data":self._flt_content(r[1])}))
        else:
            return self.write({'error':'save error'})
    
    def _flt_content(self, tags):
        l = []
        for t in tags:
            c = t['content']
            if c:l.append(c)
        return l#u','.join(l)
