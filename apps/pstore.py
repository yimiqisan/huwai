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
import Image
import StringIO

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
        
    def get_version(self, filename=None, version=-1, **kwargs):
        try:
            return (True, self.fs.get_version(filename=filename, **kwargs).read())
        except Exception, e:
            return (False, e)
        
    def get_last_version(self, filename=None, **kwargs):
        try:
            return (True, self.fs.get_last_version(filename=filename, **kwargs).read())
        except Exception, e:
            return (False, e)
    
    def list(self):
        return self.fs.list()
    
    
class ImageProcessor(object):
    def __init__(self, uid=None):
        self.uid = uid
        self.sz_l = [100]
        self.p = Pstore()
        self.max_sz = 600
    
    def _get_attr(self, im):
        if not im:
            log.error("Invalid parameter. [im]: %s" % im)
            return False
        args = {}
        args["size"] = "%dx%d" % (im.columns(), im.rows())
        args["content_type"] = "image/" + im.magick().lower()
        return args
        
    def _get_fn(self, suffix=None):
        uu = uuid.uuid4().hex
        return uu+'_'+str(suffix) if suffix else uu
        
    def _thumbnail(self, im_obj, size):
        o = StringIO.StringIO()
        im_obj.thumbnail((size, size), Image.ANTIALIAS)
        im_obj.save(o, 'JPEG')
        return o.getvalue()
        
    def process(self, data):
        ofn = self._get_fn()
        im = Image.open(StringIO.StringIO(data))
        if (im.size[0]>self.max_sz)or(im.size[1]>self.max_sz):
            data = self._thumbnail(im, self.max_sz)
        self.p.put(data, filename=ofn, size=-1)
        for sz in self.sz_l:
            fn = self._get_fn(sz)
            data = self._thumbnail(im, sz)
            self.p.put(data, filename=fn)
        return ofn
        
    def display(self, fn, version=None, **kwargs):
        if version is None:
            r = self.p.get_last_version(filename=fn, **kwargs)
        else:
            kwargs['version'] = version
            r = self.p.get_version(filename=fn, **kwargs)
        return r[1]


class AvatarProcessor(ImageProcessor):
    def __init__(self, uid=None):
        self.uid = uid
        self.sz_l = [100, 50, 30]
        self.p = Pstore()
        self.max_sz = 600
    
    def _get_fn(self, suffix=None):
        return self.uid+'_'+str(suffix) if suffix else self.uid


class AttachProcessor(ImageProcessor):
    pass

def image_font():
    import ImageFont, ImageDraw
    draw = ImageDraw.Draw(image)
    font = ImageFont.load("arial.pil")
    draw.text((10, 10), "hello", font=font)
    font = ImageFont.truetype("arial.ttf", 15)
    draw.text((10, 25), "world", font=font)
    
    
if __name__ == '__main__':
    import _imaging
    core = _imaging
    print getattr(core, "zip_decoder")