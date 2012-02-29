#!/usr/bin/env python
# encoding: utf-8
"""
sina.py

Created by 刘 智勇 on 2012-02-27.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import config

from apps.oauth2 import APIClient
from apps.user import User


def update(uid, content):
    u = User()
    u.whois('_id', uid)
    token = u.sina_access_token
    if not token:return False
    client = APIClient(config.SINA_CONSUME_KEY, config.SINA_CONSUME_SECRET)
    client.set_access_token(token)
    client.post.statuses__update(status=content)
    return True
