#! /usr/bin/env python
#coding=utf-8


from huwai.apps.user import User
from md5 import md5

def run(argv):
    channel = argv[0]
    try:
        fn = 'cmd/push_'+channel+'.txt'
        f = open(fn, 'r')
    except Exception:
        print 'open file %s error'%fn
        return False
    print 'start'
    if channel == 'user':
        u = User()
        while(True):
            line=f.readline()
            if not line:
                break
            n, e, p= line.split('\t')
            r = u.register(n.decode('utf-8'), password=p, email=unicode(e))
            print r
    elif channel == 'tag':
        pass
    else:
        pass
    print 'finish!!!'
    return True
