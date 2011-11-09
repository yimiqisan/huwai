#!/usr/bin/env python
# encoding: utf-8
"""
urls.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from handler import *

handlers = [(r"/", RootHandler),
            (r"/feedback", FeedbackHandler),
            (r"/google9f2d915bcc519f6e.html", GoogleWebMasterHandler),
            (r"/account/login", LoginHandler),
            (r"/account/register", RegisterHandler),
            (r"/account/logout", LogoutHandler),
            (r"/account/profile", ProfileHandler),
            (r"/account/setting", SettingHandler),
            (r"/t", TestHandler),
            (r".*", Error404Handler),
            ]