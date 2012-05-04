#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from commonHandler import RootHandler, TestHandler, FeedbackHandler, Error404Handler, SinaXDHandler, GoogleWebMasterHandler, CDNZZHandler, SiteMapHandler, ContactHandler
from profileHandler import LoginHandler, InviteHandler, RegisterHandler, LogoutHandler, ProfileHandler, SettingHandler, SettingAlertHandler, SettingThirdPartHandler, CpasswordHandler, BindSinaHandler, AjaxLoginHandler, AjaxRegisterHandler, AjaxLogoutHandler, AjaxCpasswordHandler
from authHandler import AuthHandler, SinaLoginHandler, QQLoginHandler, RenrenLoginHandler, ThirdPartHandler
from weiboHandler import WeiboHandler, WeiboItemHandler, WeiboSheHandler, AjaxWeiboHandler
from peopleHandler import PeopleHandler
from eventHandler import EventHandler, EventPubaHandler, EventPubbHandler, EventCheckHandler, EventListHandler, EventFallsHandler, EventMemberHandler, EventApprovalHandler, AjaxEventJoinHandler, AjaxEventApprovalHandler
from noteHandler import NoteHandler, NoteListHandler, NoteAbsHandler, NoteItemHandler, NoteEditHandler, NoteAppendHandler, NoteDeleteHandler, NoteWriteHandler, AjaxNoteHandler
from imageHandler import UploadImageHandler, AvatarHandler, AttachHandler, AjaxAvatarHandler, AjaxAvatarDeleteHandler, AjaxImageHandler, AjaxImageDeleteHandler, AjaxImageCheckHandler, DisplayHandler
from ajaxHandler import AjaxReplyHandler, AjaxRemoveHandler, AjaxToggleStateHandler, AjaxToggleInputHandler
from checkHandler import CheckHandler, CheckEventHandler, CheckTagHandler, CheckNoteHandler, CheckGuideHandler, AjaxCheckEventHandler
from alertHandler import AlertHandler, AlertListHandler, AjaxAlertHandler
from mapHandler import MapHandler, MapItemHandler, MapEventHandler, MapWeiboHandler, AjaxMapHandler
from tagHandler import TagHandler, TagItemHandler, AjaxTagHandler, AjaxTagListHandler
from albumHandler import AlbumHandler, AlbumCreateHandler, AlbumItemHandler, AjaxAlbumUploadHandler, AjaxAlbumDeleteHandler
from guideHandler import GuideHandler
from searchHandler import SearchHandler