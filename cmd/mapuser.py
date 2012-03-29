#! /usr/bin/env python
#coding=utf-8


from apps.user import User
from md5 import md5

def run(argv):
    opts = {}
    u = User()
    u._api.map(_handle_entity, opts)
    return
    
def _handle_entity(obj, opts):
    pwd = unicode(md5(obj['password']).hexdigest())
    u = User()
    u._api.edit(obj['_id'], password=pwd)
    return True
