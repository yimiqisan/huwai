#!/usr/bin/env python
# encoding: utf-8
"""
uimethods.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from tornado import template
#from huwai.apps.perm import PERM_CLASS

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