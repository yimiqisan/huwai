#!/usr/bin/env python
# encoding: utf-8
"""
case.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import logging

from alert import Alert


class Case:
    _cases = {
        'a_at': True,
        'a_rpat': True,
        'a_reply': True,
        'a_join': True,
    }
    _case_map = {}
    
    def __init__(self):
        a = Alert()
        self.on('a_at', a._api.on_at)
        self.on('a_rpat', a._api.on_rpat)
        self.on('a_reply', a._api.on_reply)
        self.on('a_join', a._api.on_join)
    
    def on(self, case, func):
        if not self._case_map.has_key(case):
            self._case_map[case] = []
        if self._case_map[case].count(func) == 0:
            self._case_map[case].append(func)
        return True
    
    def fire(self, case, **kwargs):
        if not self._case_map.has_key(case):
            return False
        for func in self._case_map[case]:
            ret = func(**kwargs)
        return True

case_object = None

def get_case_object():
    global case_object
    if case_object == None:
        case_object = Case()
    return case_object
