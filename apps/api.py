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
        self.datastore = DB_CON[DB_NAME]
        self.collection = self.datastore[IdDoc.__collection__]
    
    def incr(self):
        self.collection.update({"_id":self.idx},{"$inc":{"id":1}}, upsert=True)
    
    def decr(self):
        self.collection.update({"_id":self.idx},{"$inc":{"id":-1}}, upsert=True)
    
    def clear(self):
        self.collection.update({"_id":self.idx},{"$set":{"id":0}}, upsert=True)
    
    def count(self):
        try:
            return int(self.collection.one({"_id":self.idx})["id"])
        except:
            return 0
    
    def get(self):
        self.incr()
        return int(self.collection.one({"_id":self.idx})["id"])

class Mapping(object):
    ''' get mapping '''
    def __init__(self):
        DB_CON.register([MappingDoc])
        self.datastore = DB_CON[DB_NAME]
        self.collection = self.datastore[MappingDoc.__collection__]
        self.doc = self.collection.MappingDoc()
    
    def do(self, channel, image):
        r = self.get(channel=channel, image=image)
        if (not r[0])or r[1]:return r
        mid = get_uuid()
        self.doc['_id'] = mid
        self.doc['channel'] = channel
        self.doc['image'] = image
        try:
            self.doc.save(uuid=True, validate=True)
        except Exception, e:
            logging.info(e)
            return (False, unicode(e))
        return (True, mid)
    
    def get(self, id=None, channel=None, image=None):
        try:
            i = None
            if id and (not image):
                r = self.collection.one({"_id":id})["image"]
                if r:i=r["image"]
            elif (not id) and image:
                r = self.collection.one({"image":image, "channel":channel})
                if r:i=r["_id"]
            return (True, i)
        except Exception, e:
            logging.info(e)
            return (False, e)
        return (True, None)

class API(object):
    def __init__(self, db_name=DB_NAME, col_name=None, collection=None, doc=None):
        self.datastore = DB_CON[db_name]
        self.col_name = col_name
        self.collection = collection
        self.doc = doc
        self.structure = self.doc.structure
        self.structure.pop('added', None)
        
    def _init_doc(self, id):
        try:
            self.doc = self.collection.FileDoc.one({'_id':docid})
        except Exception:
            logging.info(e)
            raise Exception
    
    def _escape_year(self, n, c):
        if n.year == c.year:
            return c.strftime('%m-%d %H:%M')
        else:
            return c.strftime('%Y-%m-%d %H:%M')
    
    def _escape_date(self, n, c):
        e = unicode(c-n)
        if ',' in e:
            a, x = e.split(',', 1)
            d = a.split(' ')[0]
            if int(d) < 0:
                e = unicode(n-c)
                if ',' in e:
                    a, x = e.split(',', 1)
                    d = a.split(' ')[0]
                    if int(d) > 30:
                        r = u'早已结束'
                    elif int(d) > 7:
                        r = u'已结束 '+unicode(int(d)/7)+u'周'
                    elif int(d) > 1:
                        r = u'已结束 '+unicode(int(d))+u'天'
                    else:
                        r = u'刚刚结束'
                else:
                    r = u'刚刚结束'
            else:
                if int(d) > 10:
                    r = c.strftime('%m-%d %H:%M') if (n.year == c.year) else c.strftime('%Y-%m-%d %H:%M')
                else:
                    r = u'还有 '+unicode(int(d))+u'天'
        else:
            h, m, s = e.split(':')
            if int(h) != 0:
                r = u'还有 '+unicode(int(h))+u'小时开始'
            else:
                r = u'即将开始'
        return r
    
    def _escape_created(self, n, c):
        e = unicode(n-c)
        if ',' in e:
            a, x = e.split(',', 1)
            d = a.split(' ')[0]
            if int(d) > 10:
                r = c.strftime('%m-%d %H:%M') if (n.year == c.year) else c.strftime('%Y-%m-%d %H:%M')
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
        self.doc['added'] = {}
        for k, v in kwargs.items():
            try:
                if k in self.structure:
                    if isinstance(self.structure[k], list) and not isinstance(v, list):
                        v = [v]
                    self.doc[k]=v
                else:
                    self.doc['added'][k] = v
            except Exception, e:
                pass
        a = Added_id(self.col_name)
        self.doc['added_id'] = a.get()
        id = get_uuid()
        self.doc['_id'] = id
        self.doc['created'] = datetime.now()
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
        self.datastore.drop_collection(self.col_name)
        
    def _edit_added(self, id, **addeds):
        r = self.one(_id=id)
        if r[0]:
            addeds.update(r[1].get('added', {}))
            self.collection.update({"_id":id}, {'$set':{'added': addeds}})
    
    def _edit_dict(self, id, key, **dicts):
        r = self.one(_id=id)
        if r[0]:
            dicts.update(r[1].get(key, {}))
            self.collection.update({"_id":id}, {'$set':{key: dicts}})
    
    def edit(self, id, *args, **kwargs):
        items=dict(args)
        items.update(kwargs)
        keyl_l = items.keys()
        addeds = {}
        lists = {}
        for k in keyl_l:
            try:
                if k not in self.structure:
                    addeds[k]=items.pop(k)
                elif isinstance([], self.structure[k]):
                    li = items.pop(k, None)
                    if li:lists[k] = {"$each":li} if isinstance(li, list) else li
                elif isinstance({}, self.structure[k]):
                    dicts = items.pop(k)
                    self._edit_dict(id, k, **dicts)
            except Exception, e:
                pass
        try:
            if lists: self.collection.update({"_id":id}, {"$addToSet":lists})
            self.collection.update({"_id":id}, {"$set":items})
            if (len(addeds)>0):self._edit_added(id, **addeds)
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
        order = kwargs.pop('order', -1)
        order_by = kwargs.pop('order_by', 'added_id')
        try:
            r = self.collection.find(kwargs).sort(order_by, order).limit(30)
        except Exception, e:
            logging.info(e)
            return (False, e)
        return (True, r)
    
    def map(self, func, opts, **kwargs):
        if kwargs == {}:
            objs = self.collection.find()
        else:
            ret = self.collection.find(kwargs)
            if not ret[0]:
                return (False, 'error get objects')
            objs = ret[1]
        cnt = objs.count()
        c = True
        for i in xrange(cnt/100+1):
            objr = objs[i*100:(i*100 + 100)]
            for obj in objr:
                r = func(obj, opts)
                if not r:
                    c = False
                    break
            if not c:
                break
        return (True, None)
    
    def exist(self, key, value):
        try:
            return self.collection.one({key:value}) is not None
        except Exception, e:
            logging.info(e)
            raise Exception


