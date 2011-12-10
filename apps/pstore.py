#!/usr/bin/env python
# encoding: utf-8
"""
pstore.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime
import gridfs
from mongokit import Connection, ObjectId


PIC_DB_NAME = 'hwpicture'
PIC_DB_CON = Connection(host='localhost', port=27017)


class Pstore(object):
    ''' ['delete', 'exists', 'get', 'get_last_version', 'get_version', 'list', 'new_file', 'open', 'put', 'remove'] '''
    def __init__(self):
        db = PIC_DB_CON[PIC_DB_NAME]
        self.fs = gridfs.GridFS(db)
        
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None
    
    def put(self, data, **kwargs):
        return self.fs.put(data, **kwargs)
    
    def get_by_id(self, id):
        if not isinstance(id, ObjectId):id=ObjectId(id)
        return self.fs.get(id)
        
    def get_last_version(self, filename=None, **kwargs):
        try:
            return (True, self.fs.get_last_version(filename=filename, **kwargs).read())
        except Exception, e:
            return (False, e)
    
    def list(self):
        return self.fs.list()
    
class ImageProcessor(object):
    def __init__(self):
        pass


if __name__ == '__main__':
    p = Pstore()
#    pn = '/Users/yimiqisan/Desktop/upload.txt'
#    f = open(pn)
#    print p.put(f.read(), filename='tutu.gif', thumbnail=40)
#    f.close()
#    print p.get_last_version(filename='tutu.gif', thumbnail=50)
    print p.list()
















