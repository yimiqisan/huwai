#!/usr/bin/env python
# encoding: utf-8
"""
api.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import logging
import uuid

from huwai.config import DB_CON, DB_NAME
from modules import IdDoc, UserDoc, TimeLineDoc
from tools import trans_64

def get_uuid():
    return unicode(uuid.uuid4().hex)

class Added_id(object):
    ''' get autoincrement　id '''
    def __init__(self, idx):
        self.idx = idx
        DB_CON.register([IdDoc])
        self.datastroe = DB_CON[DB_NAME]
        self.collection = self.datastroe[IdDoc.__collection__]
        
    def incr(self):
        self.collection.update({"_id":self.idx},{"$inc":{"id":1}}, upsert=True)
    
    def get(self):
        self.incr()
        return trans_64(self.collection.one({"_id":self.idx})["id"])

class API(object):
    def __init__(self, col_name=None, collection=None, doc=None):
        self.datastroe = DB_CON[DB_NAME]
        self.col_name = col_name
        self.collection = collection
        self.doc = doc
        self.keys = self.doc.structure.keys()
        self.keys.remove('added')
        
    def _init_doc(self, id):
        try:
            self.doc = self.collection.FileDoc.one({'_id':docid})
        except Exception:
            logging.info(e)
            raise Exception
        
    def create(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.keys:
                self.doc[k]=v
            else:
                self.doc['added'][k] = v
        a = Added_id(self.col_name)
        self.doc['added_id'] = a.get()
        id = get_uuid()
        self.doc['_id'] = id
        try:
            self.doc.save(uuid=True, validate=True)
        except Exception, e:
            logging.info(e)
            return (False, unicode(e))
        return (True, id)
        
    def remove(self, id):
        self.collection.remove(id)
        
    def drop_table(self):
        self.datastroe.drop_collection(self.col_name)
        
    def edit(self, id, *args, **kwargs):
        items=dict(args)
        items.update(kwargs)
        keyl_l = items.keys()
        for k in keyl_l:
            if k not in self.keys():
                items['added'][k]=items.pop(k)
        try:
            self.collection.update({"_id":id}, {"$set":items})
        except Exception, e:
            logging.info(e)
            return(False, unicode(e))
        return (True, keyl_l)

    def page(self, **kwargs):
        page = kwargs.pop('page', 1)
        pglen = kwargs.pop('pglen', 10)
        limit = kwargs.pop('page', 20)
        order_by = kwargs.pop('order_by', 'added_id')
        order = kwargs.pop('order', 1)
        try:
            objs=self.collection.find(kwargs).sort(order_by, order)
            cnt = len(objs)
        except:
            return (False, 'search error')
        start = (page-1)*limit
        end = start+limit
        objs = objs[start:] if end>cnt else objs[start:end]
        #get page additional infomation
        info = {}
        total_page = cnt/limit
        if (cnt%limit) != 0:total_page+=1
        info['total_page'] = total_page
        info['has_pre'] = (page>1)
        info['start_page'] = 1
        info['pre_page'] = max(1, page-1)
        info['page'] = page
        info['page_list'] = range(max(1, min(page-4, total_page-pglen+1)), min(max(page+1+pglen/2, pglen+1), total_page+1))
        info['has_eps'] = (total_page>max(page+1+pglen/2, pglen+1)>pglen)
        info['has_next'] = (page<total_page)
        info['next_page'] = min(page+1, total_page)
        info['end_page'] = total_page		
        return (True, objs, info)
        
    def one(self, **kwargs):
        try:
            r = self.collection.one(kwargs)
        except Exception, e:
            logging.info(e)
            return (False, e)
        return (True, r)
        
    def find(self, **kwargs):
        try:
            r = self.collection.find(kwargs)
        except Exception, e:
            logging.info(e)
            return (False, e)
        return (True, r)
        
    def exist(self, key, value):
        try:
            return self.collection.one({key:value}) is not None
        except Exception, e:
            logging.info(e)
            raise Exception


class UserAPI(API):
    def __init__(self):
        DB_CON.register([UserDoc])
        datastore = DB_CON[DB_NAME]
        col_name = UserDoc.__collection__
        collection = datastore[col_name]
        doc = collection.UserDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
        
    def is_nick_exist(self, nick):
        return self.exist("nick", nick)
    
    def is_email_exist(self, email):
        return self.exist("email", email)
    

class TimeLineAPI(API):
    def __init__(self):
        DB_CON.register([TimeLineDoc])
        datastore = DB_CON[DB_NAME]
        col_name = TimeLineDoc.__collection__
        collection = datastore[col_name]
        doc = collection.TimeLineDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
        
    def save(self, column, subject, content, owner=None, nick=u'匿名'):
        return super(TimeLineAPI, self).create(owner=owner, column=column, subject=subject, content=content, nick=nick)
        
    def list(self, owner=None, column=None, subject=None):
        kwargs = {}
        if owner:kwargs['owner']=owner
        if owner:kwargs['column']=column
        if owner:kwargs['subject']=subject
        r = self.find(**kwargs)
        if r[0]:
            l = [{'nick':i['added']['nick'], 'content':i['content']} for i in r[1]]
            return (True, l)
        else:
            return (False, r[1])

        
        
        