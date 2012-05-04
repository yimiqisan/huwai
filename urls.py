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
            (r"/a/logout/", AjaxLogoutHandler),
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
            (r"/a/event/join/", AjaxEventJoinHandler),
            (r"/a/event/approval/", AjaxEventApprovalHandler),
            
            (r"/note/", NoteHandler),
            (r"/note/list/", NoteListHandler),
            (r"/note/abstract/", NoteAbsHandler),
            (r"/note/(.{32})/", NoteItemHandler),
            (r"/note/(.{32})/edit/", NoteEditHandler),
            (r"/note/(.{32})/append/", NoteAppendHandler),
            (r"/note/(.{32})/delete/", NoteDeleteHandler),
            (r"/note/write/", NoteWriteHandler),
            (r"/a/note/", AjaxNoteHandler),
            
            (r"/album/", AlbumHandler),
            (r"/album/create/", AlbumCreateHandler),
            (r"/album/(.{32})/", AlbumItemHandler),
            (r"/a/album/upload/", AjaxAlbumUploadHandler),
            (r"/a/album/delete/", AjaxAlbumDeleteHandler),
            
            (r"/tag/", TagHandler),
            (r"/tag/(.{32})/", TagItemHandler),
            
            (r"/search/", SearchHandler),
            
            (r"/guide/", GuideHandler),
            
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
            (r"/a/tag/list/", AjaxTagListHandler),
            (r"/a/reply", AjaxReplyHandler),
            (r"/a/remove", AjaxRemoveHandler),
            (r"/a/toggle/state", AjaxToggleStateHandler),
            (r"/a/toggle/input", AjaxToggleInputHandler),
            
            (r"/image/upload", UploadImageHandler),
            (r"/image/avatar/?(\w*)", AvatarHandler),
            (r"/image/attach/?(\w*)", AttachHandler),
            (r"/image/display/?(\w*)", DisplayHandler),
            (r"/a/avatar", AjaxAvatarHandler),
            (r"/a/avatar/delete/", AjaxAvatarDeleteHandler),
            (r"/a/image", AjaxImageHandler),
            (r"/a/image/delete/", AjaxImageDeleteHandler),
            (r"/a/image/check", AjaxImageCheckHandler),
            
            (r"/check/", CheckHandler),
            (r"/check/event/", CheckEventHandler),
            (r"/check/tag/", CheckTagHandler),
            (r"/check/note/", CheckNoteHandler),
            (r"/check/guide/", CheckGuideHandler),
            (r"/a/check/event/", AjaxCheckEventHandler),
            
            (r"/sitemap/", SiteMapHandler),
            (r"/contact/", ContactHandler),
            (r"/xd.html/?", SinaXDHandler),
            (r"/google9f2d915bcc519f6e.html", GoogleWebMasterHandler),
            (r"/306e81119936619cbfb5e703cca43e84.html", CDNZZHandler),
            (r"/t/", TestHandler),
            (r".*", Error404Handler),
            ]