#!/usr/bin/env python
# encoding: utf-8
"""
urls.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from handler import *

handlers = [(r"/", RootHandler),
            (r"/people/", PeopleHandler),
            
            (r"/weibo/", WeiboHandler),
            (r"/a/weibo", AjaxWeiboHandler),
            
            (r"/account/login/", LoginHandler),
            (r"/account/invite/", InviteHandler),
            (r"/account/register/", RegisterHandler),
            (r"/account/logout/", LogoutHandler),
            (r"/account/profile/", ProfileHandler),
            (r"/account/setting/", SettingHandler),
            (r"/account/thirdpart/", ThirdPartHandler),
            
            (r"/auth/sina/", SinaLoginHandler),
            (r"/auth/qq/", QQLoginHandler),
            
            (r"/event/c/", EventCrawlerHandler),
            (r"/event/(.{32})/", EventHandler),
            (r"/event/puba/", EventPubaHandler),
            (r"/event/pubb/", EventPubbHandler),
            (r"/event/", EventListHandler),
            (r"/event/loading/", EventCheckHandler),
            
            (r"/feedback/", FeedbackHandler),
            
            (r"/a/reply", AjaxReplyHandler),
            (r"/a/remove", AjaxRemoveHandler),
            (r"/a/toggle/state", AjaxToggleStateHandler),
            (r"/a/toggle/input", AjaxToggleInputHandler),
            
            (r"/image/upload", UploadImageHandler),
            (r"/image/avatar/?(\w*)", AvatarHandler),
            (r"/image/attach/?(\w*)", AttachHandler),
            (r"/a/avatar", AjaxAvatarHandler),
            (r"/a/image", AjaxImageHandler),
            (r"/a/image/check", AjaxImageCheckHandler),
            
            (r"/check/event/", CheckEventHandler),
            
            (r"/google9f2d915bcc519f6e.html", GoogleWebMasterHandler),
            (r"/t/", TestHandler),
            (r".*", Error404Handler),
            ]