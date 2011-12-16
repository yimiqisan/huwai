#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from commonHandler import RootHandler, TestHandler, AjaxReplyHandler, AjaxRemoveHandler, FeedbackHandler, Error404Handler, GoogleWebMasterHandler
from profileHandler import LoginHandler, ThirdPartHandler, RegisterHandler, LogoutHandler, ProfileHandler, SettingHandler
from weiboHandler import WeiboHandler, AjaxWeiboNewHandler
from peopleHandler import PeopleHandler
from eventHandler import EventHandler
from imageHandler import UploadImageHandler, AvatarHandler

