#! /usr/bin/env python
#coding=utf-8


from apps.user import User
from md5 import md5

def run(argv):
    id = argv[0]
    n = argv[1]
    u = User()
    pwd = unicode(md5(n).hexdigest())
    u._api.change_pwd(id, 'o', pwd, 'c')
    return
    