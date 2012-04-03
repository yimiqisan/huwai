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
            (r"/weibo/(.{32})/", WeiboItemHandler),
            (r"/weibo/she/(.{32})/", WeiboSheHandler),
            (r"/a/weibo", AjaxWeiboHandler),
            
            (r"/account/login/", LoginHandler),
            (r"/account/register/", RegisterHandler),
            (r"/account/invite/", InviteHandler),
            (r"/account/logout/", LogoutHandler),
            (r"/account/profile/", ProfileHandler),
            (r"/account/setting/", SettingHandler),
            (r"/account/setting/alert/", SettingAlertHandler),
            (r"/account/setting/thirdpart/", SettingThirdPartHandler),
            (r"/account/cpassword/", CpasswordHandler),
            (r"/account/thirdpart/", ThirdPartHandler),
            (r"/bind/sina/", BindSinaHandler),
            (r"/a/login/", AjaxLoginHandler),
            (r"/a/register/", AjaxRegisterHandler),
            (r"/a/cpassword/", AjaxCpasswordHandler),
            
            (r"/auth/", AuthHandler),
            (r"/auth/sina/", SinaLoginHandler),
            (r"/auth/qq/", QQLoginHandler),
            (r"/auth/renren/", RenrenLoginHandler),
            
            (r"/event/(.{32})/", EventHandler),
            (r"/event/(.{32})/approval/", EventApprovalHandler),
            (r"/event/puba/", EventPubaHandler),
            (r"/event/pubb/", EventPubbHandler),
            (r"/event/", EventListHandler),
            (r"/event/falls/", EventFallsHandler),
            (r"/event/(.{32})/member/", EventMemberHandler),
            (r"/event/loading/", EventCheckHandler),
            
            (r"/note/", NoteHandler),
            (r"/note/write/", NoteWriteHandler),
            (r"/a/note/", AjaxNoteHandler),
            
            (r"/map/", MapHandler),
            (r"/map/(.{32})/", MapItemHandler),
            (r"/map/event/", MapEventHandler),
            (r"/map/weibo/", MapWeiboHandler),
            (r"/a/map/", AjaxMapHandler),
            
            (r"/alert/", AlertHandler),
            (r"/alert/(.*)/", AlertListHandler),
#            (r"/alert/(.{32})/", AlertHandler),
            (r"/a/alert/", AjaxAlertHandler),
            
            (r"/feedback/", FeedbackHandler),
            
            (r"/a/tag/", AjaxTagHandler),
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
            (r"/check/tag/", CheckTagHandler),
            (r"/a/check/event/", AjaxCheckEventHandler),
            
            (r"/xd.html/?", SinaXDHandler),
            (r"/google9f2d915bcc519f6e.html", GoogleWebMasterHandler),
            (r"/306e81119936619cbfb5e703cca43e84.html", CDNZZHandler),
            (r"/t/", TestHandler),
            (r".*", Error404Handler),
            ]