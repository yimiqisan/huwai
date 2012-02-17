#!/usr/bin/env python
# encoding: utf-8
"""
uimethods.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
from tornado import template

def ifNone(handler, v=None):
    return v if v else ''

def truncate(handler, v, length=100):
    return v[:length]