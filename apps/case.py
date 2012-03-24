#!/usr/bin/env python
# encoding: utf-8
"""
case.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import logging

from alert import Alert
import sina


class Case:
    _cases = {
        'a_weibo_at': True,
        'a_weibo_ra': True,
        'a_weibo_fl': True,
        'a_account_ml': True,
        'a_account_pw': True,
        'a_account_iv': True,
        'a_event_ckfb': True,
        'a_event_jnfb': True,
        'a_event_ckps': True,
        'a_event_jnps': True,
        'a_event_jncf': True,
        's_update': True,
    }
    _case_map = {}
    
    def __init__(self):
        a = Alert()
        self.on('a_weibo_at', a._api.on_weibo_at)
        self.on('a_weibo_ra', a._api.on_weibo_ra)
        self.on('a_weibo_fl', a._api.on_weibo_fl)
        self.on('a_account_ml', a._api.on_account_ml)
        self.on('a_account_pw', a._api.on_account_pw)
        self.on('a_account_iv', a._api.on_account_iv)
        self.on('a_event_ckfb', a._api.on_event_ckfb)
        self.on('a_event_jnfb', a._api.on_event_jnfb)
        self.on('a_event_ckps', a._api.on_event_ckps)
        self.on('a_event_jnps', a._api.on_event_jnps)
        self.on('a_event_jncf', a._api.on_event_jncf)
        self.on('s_update', sina.update)
    
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
