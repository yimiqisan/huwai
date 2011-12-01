#!/usr/bin/env python
# encoding: utf-8
"""
urls.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from handler import *

handlers = [(r"/", RootHandler),
            (r"/people", PeopleHandler),
            
            (r"/weibo", WeiboHandler),
            (r"/weibo/a/new", AjaxWeiboNewHandler),
            
            (r"/account/login", LoginHandler),
            (r"/account/thirdpart", ThirdPartHandler),
            (r"/account/register", RegisterHandler),
            (r"/account/logout", LogoutHandler),
            (r"/account/profile", ProfileHandler),
            (r"/account/setting", SettingHandler),
            
            (r"/event", EventHandler),

            (r"/feedback", FeedbackHandler),
            
            (r"/a/reply", AjaxReplyHandler),
            (r"/a/remove", AjaxRemoveHandler),
            
            (r"/google9f2d915bcc519f6e.html", GoogleWebMasterHandler),
            (r"/t", TestHandler),
            (r".*", Error404Handler),
            ]