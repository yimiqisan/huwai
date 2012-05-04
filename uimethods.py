#!/usr/bin/env python
# encoding: utf-8
"""
uimethods.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from tornado import template
#from huwai.apps.perm import PERM_CLASS
#from huwai.apps.tag import Tag

def ifNone(handler, v=None):
    return v if v else ''

def truncate(handler, v, length=100):
    return v[:length]

def verify(handler, perm, reference):
    if isinstance(reference, int):
        return perm == reference
    elif isinstance(reference, list):
        return (perm in reference)
    elif isinstance(reference, dict):
        s=reference.get('start', 0x00)
        e=reference.get('end', 0x99)
        return (s <= perm <= e)
    return False

def list2txt(handler, v=None):
    if isinstance(v, list):
        if None in v:v.remove(None)
        return ','.join(v)
    elif isinstance(v, unicode) or isinstance(v, str):
        return v
    return ''

def dict2txt(handler, v=None):
    if isinstance(v, dict):
        return ''.join(v.values())

def list2url(handler, v=None):
    if isinstance(v, list):
        if None in v:v.remove(None)
        l = []
        for i, c in v:
            href, txt = '/tag/'+i, c
            l.append(u'<a class="badge badge-info" href="%s">%s</a>' % (href, txt))
        return ' '.join(l)
    elif isinstance(v, tuple):
        href = '/tag/'+v[0]
        txt = v[1]
        return u'<a class="badge badge-info" href="%s">%s</a>' % (href, txt)
    return ''

def cntDict(handler, l, **kwargs):
    cnt = 0
    for i in l:
        plus = True
        for k, v in kwargs.items():
            if i.get(k, None) != v:
                plus = False
        if plus:cnt += 1
    return cnt

def abstract(handler, c, n=100):
    import re
    s = re.sub(r'</?\w+[^>]*>','',c)
    s = s.replace(' ', '')
    if (len(s) > n):
        return s[:n-3] + '...'
    else:
        return s[:n]
