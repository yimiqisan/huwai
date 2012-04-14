#! /usr/bin/env python
#coding=utf-8


from huwai.apps.user import User
from huwai.apps.tag import Tag
from huwai.config import SITE_ID
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
            r = u.register(n.decode('utf-8'), password=unicode(p.strip()), email=unicode(e))
            print r
    elif channel[:3] == 'tag':
        t = Tag()
        while(True):
            line=f.readline()
            if not line:
                break
            h, d, c = line.split(',')
            c = c.replace('\r\n', '').replace('\n', '').replace('\r', '').decode('utf-8')
            r = t._api.add(SITE_ID, c, relation_l=['place'])
            print r
    else:
        pass
    f.close()
    print 'finish!!!'
    return True
