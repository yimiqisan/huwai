#!/usr/bin/env python
# encoding: utf-8
"""
api.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import logging
import uuid
from datetime import datetime

from huwai.config import DB_CON, DB_NAME
from modules import IdDoc, MappingDoc

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
        return int(self.collection.one({"_id":self.idx})["id"])

class Mapping(object):
    ''' get mapping '''
    def __init__(self):
        DB_CON.register([MappingDoc])
        self.datastroe = DB_CON[DB_NAME]
        self.collection = self.datastroe[MappingDoc.__collection__]
        self.doc = self.collection.MappingDoc()
    
    def do(self, image):
        r = self.get(image=image)
        if (not r[0])or r[1]:return r
        mid = get_uuid()
        self.doc['_id'] = mid
        self.doc['image'] = image
        try:
            self.doc.save(uuid=True, validate=True)
        except Exception, e:
            logging.info(e)
            return (False, unicode(e))
        return (True, mid)
    
    def get(self, id=None, image=None):
        try:
            i = None
            if id and (not image):
                r = self.collection.one({"_id":id})["image"]
                if r:i=r["image"]
            elif (not id) and image:
                r = self.collection.one({"image":image})
                if r:i=r["_id"]
            return (True, i)
        except Exception, e:
            logging.info(e)
            return (False, e)
        return (True, None)

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
    
    def _escape_created(self, n, c):
        e = unicode(n-c)
        if ',' in e:
            a, x = e.split(',', 1)
            d = a.split(' ')[0]
            if int(d) > 5:
                r = c.strftime('%Y-%m-%d %X')
            elif int(d) == 1:
                r = a.replace('day', u'天前')
            else:
                r = a.replace('days', u'天前')
        else:
            h, m, s = e.split(':')
            if int(h) != 0:
                r = unicode(int(h))+u'小时前'
            elif int(m) != 0:
                r = unicode(int(m))+u'分钟前'
            else:
                r = unicode(int(float(s)))+u'秒前'
        return r
    
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
        if not id:return False
        return self.collection.remove(id)
        
    def drops(self, **kwargs):
        try:
            self.collection.remove(kwargs)
        except Exception, e:
            logging.info(e)
            return False
        return True
        
    def drop_table(self):
        self.datastroe.drop_collection(self.col_name)
        
    def edit(self, id, *args, **kwargs):
        items=dict(args)
        items.update(kwargs)
        keyl_l = items.keys()
        for k in keyl_l:
            if k not in self.keys:
                items['added']={k:items.pop(k)}
        try:
            self.collection.update({"_id":id}, {"$set":items})
        except Exception, e:
            logging.info(e)
            return(False, unicode(e))
        return (True, keyl_l)
    
    def extend(self, **kwargs):
        cursor = kwargs.pop('cursor', None)
        limit = kwargs.pop('limit', 20)
        order = kwargs.pop('order', -1)
        order_by = kwargs.pop('order_by', 'added_id')
        if cursor and (order < 0):
            kwargs.update({order_by:{'$lt':cursor}})
        elif cursor and (order > 0):
            kwargs.update({order_by:{'$gt':cursor}})
        try:
            objs= self.collection.find(kwargs).sort(order_by, order).limit(limit)
#            kwargs.update({'created':{'$lt':datetime.now()}})
#            objs= self.collection.find(kwargs).sort('created', 1).limit(limit)
        except:
            return (False, 'search error')
        return (True, objs)
    
    def page(self, **kwargs):
        page = kwargs.pop('page', 1)
        pglen = kwargs.pop('pglen', 10)
        limit = kwargs.pop('limit', 20)
        start = (page-1)*limit
        order_by = kwargs.pop('order_by', 'added_id')
        order = kwargs.pop('order', -1)
        try:
            objs=self.collection.find(kwargs).sort(order_by, order).skip(start).limit(limit)
            cnt=self.collection.find(kwargs).count()
        except Exception, e:
            return (False, e)
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
    
    def count(self, **kwargs):
        try:
            cnt=self.collection.find(kwargs).count()
        except Exception, e:
            return -1
        return cnt
    
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


