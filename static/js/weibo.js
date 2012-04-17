var Weibo = {
    init: function(){
        $("#weiboform").live("submit", function() {
            if (!$.cookie("uid")) {
                $('#login').modal();
                return false;
            }
            Weibo.new($(this));
            return false;
        });
        Weibo.getLen();
        $("#weibo-content").live('focus', function(){
            if (!$.cookie("uid")) {
                $('#login').modal();
                return false;
            }
            $("#weiboform input[type=submit]").addClass("btn-primary");
            return false;
        });
        $("#weibo-content").live('blur', function(){
            $("#weiboform input[type=submit]").removeClass("btn-primary");
            return false;
        });
        Weibo.extend();
        Weibo.hover();
        Weibo.load();
    },
    
    info: function(e) {
        $("#weibo .wb_items").append('<div id="info"><table><tr></tr></table></div>');
        if (e.has_pre){$("#info table tr").append('<td><a href="">&lt;&lt;</a></td><td><a href="">&lt;</a></td>');}
        else{$("#info table tr").append('<td></td>');}
        for (var i=0; i<e.page_list.length; i++){$("#info table tr").append('<td><a href="" target="_self">'+e.page_list[i]+'</a></td>');}
        if (e.has_eps){$("#info table tr").append('<td><span class="break" >...</span></td>');}
        if (e.has_next){$("#info table tr").append('<td><a href="">&gt;</a></td><td><a href="">&gt;&gt;</a></td>{% else %}<td></td>');}
        else{$("#info table tr").append('<td></td>');}
    },
    
    extend: function() {
        var e = $('#wb_bottom');
        if ($(e).find('input').val()=='-1'){$(e).find('a').text('没有更多的了');return false;}
        var args = {'cursor': $(e).find('input').val()};
        var she = $('#weibo .wb_items').attr('she');
        var mtp = $('#weibo .wb_items').attr('maintype');
        var stp = $('#weibo .wb_items').attr('subtype');
        if (she){args.she=she;}
        if (mtp){args.maintype=mtp;}
        if (stp){args.subtype=stp;}
        $(e).find('a').addClass('loading');
        $.postJSON("/a/weibo", "GET", args, function(response) {
            if (response.error){
                return alert(response.error);
            }
            htmls = response.htmls;
            for (var i=0; i<htmls.length; i++) {
                $(htmls[i]).insertBefore(e);
            }
            $(e).find('input').val(response.cursor);
            $(e).find('a').removeClass('loading');
        });
    },
    
    hover: function(){
        $("#weibo .wb_items").hover(function(){
            $(".wb_item").hover(function(){
                $(this).find(".remove:first").show();
            },function(){
                $(this).find(".remove:first").hide();
            });
        },function(){
            $(".wb_item").hover(function(){
                $(this).find(".remove:first").show();
            },function(){
                $(this).find(".remove:first").hide();
            });
        })
    },
    
    new: function(form) {
        if (!form.find("#weibo-content").val()){
            form.find("#weibo-content").select();
            return;
        }
        var title = $("#weibo .wb_items").attr("title");
        if (title){
            var content = form.find("#weibo-content").val()
            if (content.indexOf(title)<0) {
                alert("发布的内容需要包含:"+title);
                form.find("#weibo-content").val(title).select();
                return;
            }
        }
        var message = form.formToDict();
        var disabled = form.find("input[type=submit]");
        disabled.disable();
        var kind = $('#weibo .wb_items').attr('kind');
        if (kind){args.kind=kind;}
        $.postJSON("/a/weibo", 'POST', message, function(response) {
            if (response.error){
                disabled.enable();
                return alert(response.error);
            }
            Weibo.insert(response);
            if (title){
                form.find("#weibo-content").val(title).select();
            }else{
                form.find("#weibo-content").val("").select();
            }
            $("#weiboform input[type=submit]").removeClass("btn-primary");
            $("#num").text(140);
            disabled.enable();
        });
    },

    insert: function(message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        node.hide();
        $(node).insertBefore("#weibo .wb_item:first");
        node.slideDown();
        Weibo.hover();
    },
    
    load: function() {
        $(window).scroll(function () {
            var sBottom = $(this).height()+$(this).scrollTop();
            if (sBottom >= $("#wb_bottom").offset().top) {
                Weibo.extend();
            }
        });
    },

    getLen: function(){
        var max_len = 140;
        $("#num").text(max_len - $("#weibo-content").val().length);
        $("#weibo-content").bind('change ' + ($.browser.msie ? "propertychange" : "input"), function(event){
            var val = $.trim($(this).val()), len = val.length;
            if(len > max_len){ $(this).val(val.substr(0, max_len)); }
            else{ $("#num").text(max_len - len); }
        });
    }
};





























/*
SWFUpload: http://www.swfupload.org, http://swfupload.googlecode.com

mmSWFUpload 1.0: Flash upload dialog - http://profandesign.se/swfupload/,  http://www.vinterwebb.se/

SWFUpload is (c) 2006-2007 Lars Huring, Olov Nilzén and Mammon Media and is released under the MIT License:
http://www.opensource.org/licenses/mit-license.php
 
SWFUpload 2 is (c) 2007-2008 Jake Roberts and is released under the MIT License:
http://www.opensource.org/licenses/mit-license.php
*/

var SWFUpload;
if (SWFUpload == undefined) {
	SWFUpload = function(a) {
		this.initSWFUpload(a)
	}
}
SWFUpload.prototype.initSWFUpload = function(b) {
	try {
		this.customSettings = {};
		this.settings = b;
		this.eventQueue = [];
		this.movieName = "SWFUpload_" + SWFUpload.movieCount++;
		this.movieElement = null;
		SWFUpload.instances[this.movieName] = this;
		this.initSettings();
		this.loadFlash();
		this.displayDebugInfo()
	} catch(a) {
		delete SWFUpload.instances[this.movieName];
		throw a
	}
};
SWFUpload.instances = {};
SWFUpload.movieCount = 0;
SWFUpload.version = "2.2.0 2009-03-25";
SWFUpload.QUEUE_ERROR = {
	QUEUE_LIMIT_EXCEEDED: -100,
	FILE_EXCEEDS_SIZE_LIMIT: -110,
	ZERO_BYTE_FILE: -120,
	INVALID_FILETYPE: -130
};
SWFUpload.UPLOAD_ERROR = {
	HTTP_ERROR: -200,
	MISSING_UPLOAD_URL: -210,
	IO_ERROR: -220,
	SECURITY_ERROR: -230,
	UPLOAD_LIMIT_EXCEEDED: -240,
	UPLOAD_FAILED: -250,
	SPECIFIED_FILE_ID_NOT_FOUND: -260,
	FILE_VALIDATION_FAILED: -270,
	FILE_CANCELLED: -280,
	UPLOAD_STOPPED: -290
};
SWFUpload.FILE_STATUS = {
	QUEUED: -1,
	IN_PROGRESS: -2,
	ERROR: -3,
	COMPLETE: -4,
	CANCELLED: -5
};
SWFUpload.BUTTON_ACTION = {
	SELECT_FILE: -100,
	SELECT_FILES: -110,
	START_UPLOAD: -120
};
SWFUpload.CURSOR = {
	ARROW: -1,
	HAND: -2
};
SWFUpload.WINDOW_MODE = {
	WINDOW: "window",
	TRANSPARENT: "transparent",
	OPAQUE: "opaque"
};
SWFUpload.completeURL = function(a) {
	if (typeof(a) !== "string" || a.match(/^https?:\/\//i) || a.match(/^\//)) {
		return a
	}
	var c = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ":" + window.location.port: "");
	var b = window.location.pathname.lastIndexOf("/");
	if (b <= 0) {
		path = "/"
	} else {
		path = window.location.pathname.substr(0, b) + "/"
	}
	return path + a
};
SWFUpload.prototype.initSettings = function() {
	this.ensureDefault = function(b, a) {
		this.settings[b] = (this.settings[b] == undefined) ? a: this.settings[b]
	};
	this.ensureDefault("upload_url", "");
	this.ensureDefault("preserve_relative_urls", false);
	this.ensureDefault("file_post_name", "Filedata");
	this.ensureDefault("post_params", {});
	this.ensureDefault("use_query_string", false);
	this.ensureDefault("requeue_on_error", false);
	this.ensureDefault("http_success", []);
	this.ensureDefault("assume_success_timeout", 0);
	this.ensureDefault("file_types", "*.*");
	this.ensureDefault("file_types_description", "All Files");
	this.ensureDefault("file_size_limit", 0);
	this.ensureDefault("file_upload_limit", 0);
	this.ensureDefault("file_queue_limit", 0);
	this.ensureDefault("flash_url", "swfupload.swf");
	this.ensureDefault("prevent_swf_caching", true);
	this.ensureDefault("button_image_url", "");
	this.ensureDefault("button_width", 1);
	this.ensureDefault("button_height", 1);
	this.ensureDefault("button_text", "");
	this.ensureDefault("button_text_style", "color: #000000; font-size: 16pt;");
	this.ensureDefault("button_text_top_padding", 0);
	this.ensureDefault("button_text_left_padding", 0);
	this.ensureDefault("button_action", SWFUpload.BUTTON_ACTION.SELECT_FILES);
	this.ensureDefault("button_disabled", false);
	this.ensureDefault("button_placeholder_id", "");
	this.ensureDefault("button_placeholder", null);
	this.ensureDefault("button_cursor", SWFUpload.CURSOR.ARROW);
	this.ensureDefault("button_window_mode", SWFUpload.WINDOW_MODE.WINDOW);
	this.ensureDefault("debug", false);
	this.settings.debug_enabled = this.settings.debug;
	this.settings.return_upload_start_handler = this.returnUploadStart;
	this.ensureDefault("swfupload_loaded_handler", null);
	this.ensureDefault("file_dialog_start_handler", null);
	this.ensureDefault("file_queued_handler", null);
	this.ensureDefault("file_queue_error_handler", null);
	this.ensureDefault("file_dialog_complete_handler", null);
	this.ensureDefault("upload_start_handler", null);
	this.ensureDefault("upload_progress_handler", null);
	this.ensureDefault("upload_error_handler", null);
	this.ensureDefault("upload_success_handler", null);
	this.ensureDefault("upload_complete_handler", null);
	this.ensureDefault("debug_handler", this.debugMessage);
	this.ensureDefault("custom_settings", {});
	this.customSettings = this.settings.custom_settings;
	if ( !! this.settings.prevent_swf_caching) {
		this.settings.flash_url = this.settings.flash_url + (this.settings.flash_url.indexOf("?") < 0 ? "?": "&") + "preventswfcaching=" + new Date().getTime()
	}
	if (!this.settings.preserve_relative_urls) {
		this.settings.upload_url = SWFUpload.completeURL(this.settings.upload_url);
		this.settings.button_image_url = SWFUpload.completeURL(this.settings.button_image_url)
	}
	delete this.ensureDefault
};
SWFUpload.prototype.loadFlash = function() {
	var a,
	b;
	if (document.getElementById(this.movieName) !== null) {
		throw "ID " + this.movieName + " is already in use. The Flash Object could not be added"
	}
	a = document.getElementById(this.settings.button_placeholder_id) || this.settings.button_placeholder;
	if (a == undefined) {
		throw "Could not find the placeholder element: " + this.settings.button_placeholder_id
	}
	b = document.createElement("div");
	b.innerHTML = this.getFlashHTML();
	a.parentNode.replaceChild(b.firstChild, a);
	if (window[this.movieName] == undefined) {
		window[this.movieName] = this.getMovieElement()
	}
};
SWFUpload.prototype.getFlashHTML = function() {
	return ['<object id="', this.movieName, '" type="application/x-shockwave-flash" data="', this.settings.flash_url, '" width="', this.settings.button_width, '" height="', this.settings.button_height, '" class="swfupload">', '<param name="wmode" value="', this.settings.button_window_mode, '" />', '<param name="movie" value="', this.settings.flash_url, '" />', '<param name="quality" value="high" />', '<param name="menu" value="false" />', '<param name="allowScriptAccess" value="always" />', '<param name="flashvars" value="' + this.getFlashVars() + '" />', "</object>"].join("")
};
SWFUpload.prototype.getFlashVars = function() {
	var b = this.buildParamString();
	var a = this.settings.http_success.join(",");
	return ["movieName=", encodeURIComponent(this.movieName), "&amp;uploadURL=", encodeURIComponent(this.settings.upload_url), "&amp;useQueryString=", encodeURIComponent(this.settings.use_query_string), "&amp;requeueOnError=", encodeURIComponent(this.settings.requeue_on_error), "&amp;httpSuccess=", encodeURIComponent(a), "&amp;assumeSuccessTimeout=", encodeURIComponent(this.settings.assume_success_timeout), "&amp;params=", encodeURIComponent(b), "&amp;filePostName=", encodeURIComponent(this.settings.file_post_name), "&amp;fileTypes=", encodeURIComponent(this.settings.file_types), "&amp;fileTypesDescription=", encodeURIComponent(this.settings.file_types_description), "&amp;fileSizeLimit=", encodeURIComponent(this.settings.file_size_limit), "&amp;fileUploadLimit=", encodeURIComponent(this.settings.file_upload_limit), "&amp;fileQueueLimit=", encodeURIComponent(this.settings.file_queue_limit), "&amp;debugEnabled=", encodeURIComponent(this.settings.debug_enabled), "&amp;buttonImageURL=", encodeURIComponent(this.settings.button_image_url), "&amp;buttonWidth=", encodeURIComponent(this.settings.button_width), "&amp;buttonHeight=", encodeURIComponent(this.settings.button_height), "&amp;buttonText=", encodeURIComponent(this.settings.button_text), "&amp;buttonTextTopPadding=", encodeURIComponent(this.settings.button_text_top_padding), "&amp;buttonTextLeftPadding=", encodeURIComponent(this.settings.button_text_left_padding), "&amp;buttonTextStyle=", encodeURIComponent(this.settings.button_text_style), "&amp;buttonAction=", encodeURIComponent(this.settings.button_action), "&amp;buttonDisabled=", encodeURIComponent(this.settings.button_disabled), "&amp;buttonCursor=", encodeURIComponent(this.settings.button_cursor)].join("")
};
SWFUpload.prototype.getMovieElement = function() {
	if (this.movieElement == undefined) {
		this.movieElement = document.getElementById(this.movieName)
	}
	if (this.movieElement === null) {
		throw "Could not find Flash element"
	}
	return this.movieElement
};
SWFUpload.prototype.buildParamString = function() {
	var c = this.settings.post_params;
	var b = [];
	if (typeof(c) === "object") {
		for (var a in c) {
			if (c.hasOwnProperty(a)) {
				b.push(encodeURIComponent(a.toString()) + "=" + encodeURIComponent(c[a].toString()))
			}
		}
	}
	return b.join("&amp;")
};
SWFUpload.prototype.destroy = function() {
	try {
		this.cancelUpload(null, false);
		var a = null;
		a = this.getMovieElement();
		if (a && typeof(a.CallFunction) === "unknown") {
			for (var c in a) {
				try {
					if (typeof(a[c]) === "function") {
						a[c] = null
					}
				} catch(e) {}
			}
			try {
				a.parentNode.removeChild(a)
			} catch(b) {}
		}
		window[this.movieName] = null;
		SWFUpload.instances[this.movieName] = null;
		delete SWFUpload.instances[this.movieName];
		this.movieElement = null;
		this.settings = null;
		this.customSettings = null;
		this.eventQueue = null;
		this.movieName = null;
		return true
	} catch(d) {
		return false
	}
};
SWFUpload.prototype.displayDebugInfo = function() {
	this.debug(["---SWFUpload Instance Info---\n", "Version: ", SWFUpload.version, "\n", "Movie Name: ", this.movieName, "\n", "Settings:\n", "\t", "upload_url:               ", this.settings.upload_url, "\n", "\t", "flash_url:                ", this.settings.flash_url, "\n", "\t", "use_query_string:         ", this.settings.use_query_string.toString(), "\n", "\t", "requeue_on_error:         ", this.settings.requeue_on_error.toString(), "\n", "\t", "http_success:             ", this.settings.http_success.join(", "), "\n", "\t", "assume_success_timeout:   ", this.settings.assume_success_timeout, "\n", "\t", "file_post_name:           ", this.settings.file_post_name, "\n", "\t", "post_params:              ", this.settings.post_params.toString(), "\n", "\t", "file_types:               ", this.settings.file_types, "\n", "\t", "file_types_description:   ", this.settings.file_types_description, "\n", "\t", "file_size_limit:          ", this.settings.file_size_limit, "\n", "\t", "file_upload_limit:        ", this.settings.file_upload_limit, "\n", "\t", "file_queue_limit:         ", this.settings.file_queue_limit, "\n", "\t", "debug:                    ", this.settings.debug.toString(), "\n", "\t", "prevent_swf_caching:      ", this.settings.prevent_swf_caching.toString(), "\n", "\t", "button_placeholder_id:    ", this.settings.button_placeholder_id.toString(), "\n", "\t", "button_placeholder:       ", (this.settings.button_placeholder ? "Set": "Not Set"), "\n", "\t", "button_image_url:         ", this.settings.button_image_url.toString(), "\n", "\t", "button_width:             ", this.settings.button_width.toString(), "\n", "\t", "button_height:            ", this.settings.button_height.toString(), "\n", "\t", "button_text:              ", this.settings.button_text.toString(), "\n", "\t", "button_text_style:        ", this.settings.button_text_style.toString(), "\n", "\t", "button_text_top_padding:  ", this.settings.button_text_top_padding.toString(), "\n", "\t", "button_text_left_padding: ", this.settings.button_text_left_padding.toString(), "\n", "\t", "button_action:            ", this.settings.button_action.toString(), "\n", "\t", "button_disabled:          ", this.settings.button_disabled.toString(), "\n", "\t", "custom_settings:          ", this.settings.custom_settings.toString(), "\n", "Event Handlers:\n", "\t", "swfupload_loaded_handler assigned:  ", (typeof this.settings.swfupload_loaded_handler === "function").toString(), "\n", "\t", "file_dialog_start_handler assigned: ", (typeof this.settings.file_dialog_start_handler === "function").toString(), "\n", "\t", "file_queued_handler assigned:       ", (typeof this.settings.file_queued_handler === "function").toString(), "\n", "\t", "file_queue_error_handler assigned:  ", (typeof this.settings.file_queue_error_handler === "function").toString(), "\n", "\t", "upload_start_handler assigned:      ", (typeof this.settings.upload_start_handler === "function").toString(), "\n", "\t", "upload_progress_handler assigned:   ", (typeof this.settings.upload_progress_handler === "function").toString(), "\n", "\t", "upload_error_handler assigned:      ", (typeof this.settings.upload_error_handler === "function").toString(), "\n", "\t", "upload_success_handler assigned:    ", (typeof this.settings.upload_success_handler === "function").toString(), "\n", "\t", "upload_complete_handler assigned:   ", (typeof this.settings.upload_complete_handler === "function").toString(), "\n", "\t", "debug_handler assigned:             ", (typeof this.settings.debug_handler === "function").toString(), "\n"].join(""))
};
SWFUpload.prototype.addSetting = function(b, c, a) {
	if (c == undefined) {
		return (this.settings[b] = a)
	} else {
		return (this.settings[b] = c)
	}
};
SWFUpload.prototype.getSetting = function(a) {
	if (this.settings[a] != undefined) {
		return this.settings[a]
	}
	return ""
};
SWFUpload.prototype.callFlash = function(functionName, argumentArray) {
	argumentArray = argumentArray || [];
	var movieElement = this.getMovieElement();
	var returnValue,
	returnString;
	try {
		returnString = movieElement.CallFunction('<invoke name="' + functionName + '" returntype="javascript">' + __flash__argumentsToXML(argumentArray, 0) + "</invoke>");
		returnValue = eval(returnString)
	} catch(ex) {
		throw "Call to " + functionName + " failed"
	}
	if (returnValue != undefined && typeof returnValue.post === "object") {
		returnValue = this.unescapeFilePostParams(returnValue)
	}
	return returnValue
};
SWFUpload.prototype.selectFile = function() {
	this.callFlash("SelectFile")
};
SWFUpload.prototype.selectFiles = function() {
	this.callFlash("SelectFiles")
};
SWFUpload.prototype.startUpload = function(a) {
	this.callFlash("StartUpload", [a])
};
SWFUpload.prototype.cancelUpload = function(a, b) {
	if (b !== false) {
		b = true
	}
	this.callFlash("CancelUpload", [a, b])
};
SWFUpload.prototype.stopUpload = function() {
	this.callFlash("StopUpload")
};
SWFUpload.prototype.getStats = function() {
	return this.callFlash("GetStats")
};
SWFUpload.prototype.setStats = function(a) {
	this.callFlash("SetStats", [a])
};
SWFUpload.prototype.getFile = function(a) {
	if (typeof(a) === "number") {
		return this.callFlash("GetFileByIndex", [a])
	} else {
		return this.callFlash("GetFile", [a])
	}
};
SWFUpload.prototype.addFileParam = function(a, b, c) {
	return this.callFlash("AddFileParam", [a, b, c])
};
SWFUpload.prototype.removeFileParam = function(a, b) {
	this.callFlash("RemoveFileParam", [a, b])
};
SWFUpload.prototype.setUploadURL = function(a) {
	this.settings.upload_url = a.toString();
	this.callFlash("SetUploadURL", [a])
};
SWFUpload.prototype.setPostParams = function(a) {
	this.settings.post_params = a;
	this.callFlash("SetPostParams", [a])
};
SWFUpload.prototype.addPostParam = function(a, b) {
	this.settings.post_params[a] = b;
	this.callFlash("SetPostParams", [this.settings.post_params])
};
SWFUpload.prototype.removePostParam = function(a) {
	delete this.settings.post_params[a];
	this.callFlash("SetPostParams", [this.settings.post_params])
};
SWFUpload.prototype.setFileTypes = function(a, b) {
	this.settings.file_types = a;
	this.settings.file_types_description = b;
	this.callFlash("SetFileTypes", [a, b])
};
SWFUpload.prototype.setFileSizeLimit = function(a) {
	this.settings.file_size_limit = a;
	this.callFlash("SetFileSizeLimit", [a])
};
SWFUpload.prototype.setFileUploadLimit = function(a) {
	this.settings.file_upload_limit = a;
	this.callFlash("SetFileUploadLimit", [a])
};
SWFUpload.prototype.setFileQueueLimit = function(a) {
	this.settings.file_queue_limit = a;
	this.callFlash("SetFileQueueLimit", [a])
};
SWFUpload.prototype.setFilePostName = function(a) {
	this.settings.file_post_name = a;
	this.callFlash("SetFilePostName", [a])
};
SWFUpload.prototype.setUseQueryString = function(a) {
	this.settings.use_query_string = a;
	this.callFlash("SetUseQueryString", [a])
};
SWFUpload.prototype.setRequeueOnError = function(a) {
	this.settings.requeue_on_error = a;
	this.callFlash("SetRequeueOnError", [a])
};
SWFUpload.prototype.setHTTPSuccess = function(a) {
	if (typeof a === "string") {
		a = a.replace(" ", "").split(",")
	}
	this.settings.http_success = a;
	this.callFlash("SetHTTPSuccess", [a])
};
SWFUpload.prototype.setAssumeSuccessTimeout = function(a) {
	this.settings.assume_success_timeout = a;
	this.callFlash("SetAssumeSuccessTimeout", [a])
};
SWFUpload.prototype.setDebugEnabled = function(a) {
	this.settings.debug_enabled = a;
	this.callFlash("SetDebugEnabled", [a])
};
SWFUpload.prototype.setButtonImageURL = function(a) {
	if (a == undefined) {
		a = ""
	}
	this.settings.button_image_url = a;
	this.callFlash("SetButtonImageURL", [a])
};
SWFUpload.prototype.setButtonDimensions = function(c, a) {
	this.settings.button_width = c;
	this.settings.button_height = a;
	var b = this.getMovieElement();
	if (b != undefined) {
		b.style.width = c + "px";
		b.style.height = a + "px"
	}
	this.callFlash("SetButtonDimensions", [c, a])
};
SWFUpload.prototype.setButtonText = function(a) {
	this.settings.button_text = a;
	this.callFlash("SetButtonText", [a])
};
SWFUpload.prototype.setButtonTextPadding = function(b, a) {
	this.settings.button_text_top_padding = a;
	this.settings.button_text_left_padding = b;
	this.callFlash("SetButtonTextPadding", [b, a])
};
SWFUpload.prototype.setButtonTextStyle = function(a) {
	this.settings.button_text_style = a;
	this.callFlash("SetButtonTextStyle", [a])
};
SWFUpload.prototype.setButtonDisabled = function(a) {
	this.settings.button_disabled = a;
	this.callFlash("SetButtonDisabled", [a])
};
SWFUpload.prototype.setButtonAction = function(a) {
	this.settings.button_action = a;
	this.callFlash("SetButtonAction", [a])
};
SWFUpload.prototype.setButtonCursor = function(a) {
	this.settings.button_cursor = a;
	this.callFlash("SetButtonCursor", [a])
};
SWFUpload.prototype.queueEvent = function(b, c) {
	if (c == undefined) {
		c = []
	} else {
		if (! (c instanceof Array)) {
			c = [c]
		}
	}
	var a = this;
	if (typeof this.settings[b] === "function") {
		this.eventQueue.push(function() {
			this.settings[b].apply(this, c)
		});
		setTimeout(function() {
			a.executeNextEvent()
		},
		0)
	} else {
		if (this.settings[b] !== null) {
			throw "Event handler " + b + " is unknown or is not a function"
		}
	}
};
SWFUpload.prototype.executeNextEvent = function() {
	var a = this.eventQueue ? this.eventQueue.shift() : null;
	if (typeof(a) === "function") {
		a.apply(this)
	}
};
SWFUpload.prototype.unescapeFilePostParams = function(c) {
	var e = /[$]([0-9a-f]{4})/i;
	var f = {};
	var d;
	if (c != undefined) {
		for (var a in c.post) {
			if (c.post.hasOwnProperty(a)) {
				d = a;
				var b;
				while ((b = e.exec(d)) !== null) {
					d = d.replace(b[0], String.fromCharCode(parseInt("0x" + b[1], 16)))
				}
				f[d] = c.post[a]
			}
		}
		c.post = f
	}
	return c
};
SWFUpload.prototype.testExternalInterface = function() {
	try {
		return this.callFlash("TestExternalInterface")
	} catch(a) {
		return false
	}
};
SWFUpload.prototype.flashReady = function() {
	var a = this.getMovieElement();
	if (!a) {
		this.debug("Flash called back ready but the flash movie can't be found.");
		return
	}
	this.cleanUp(a);
	this.queueEvent("swfupload_loaded_handler")
};
SWFUpload.prototype.cleanUp = function(a) {
	try {
		if (this.movieElement && typeof(a.CallFunction) === "unknown") {
			this.debug("Removing Flash functions hooks (this should only run in IE and should prevent memory leaks)");
			for (var c in a) {
				try {
					if (typeof(a[c]) === "function") {
						a[c] = null
					}
				} catch(b) {}
			}
		}
	} catch(d) {}
	window.__flash__removeCallback = function(e, f) {
		try {
			if (e) {
				e[f] = null
			}
		} catch(g) {}
	}
};
SWFUpload.prototype.fileDialogStart = function() {
	this.queueEvent("file_dialog_start_handler")
};
SWFUpload.prototype.fileQueued = function(a) {
	a = this.unescapeFilePostParams(a);
	this.queueEvent("file_queued_handler", a)
};
SWFUpload.prototype.fileQueueError = function(a, c, b) {
	a = this.unescapeFilePostParams(a);
	this.queueEvent("file_queue_error_handler", [a, c, b])
};
SWFUpload.prototype.fileDialogComplete = function(b, c, a) {
	this.queueEvent("file_dialog_complete_handler", [b, c, a])
};
SWFUpload.prototype.uploadStart = function(a) {
	a = this.unescapeFilePostParams(a);
	this.queueEvent("return_upload_start_handler", a)
};
SWFUpload.prototype.returnUploadStart = function(a) {
	var b;
	if (typeof this.settings.upload_start_handler === "function") {
		a = this.unescapeFilePostParams(a);
		b = this.settings.upload_start_handler.call(this, a)
	} else {
		if (this.settings.upload_start_handler != undefined) {
			throw "upload_start_handler must be a function"
		}
	}
	if (b === undefined) {
		b = true
	}
	b = !!b;
	this.callFlash("ReturnUploadStart", [b])
};
SWFUpload.prototype.uploadProgress = function(a, c, b) {
	a = this.unescapeFilePostParams(a);
	this.queueEvent("upload_progress_handler", [a, c, b])
};
SWFUpload.prototype.uploadError = function(a, c, b) {
	a = this.unescapeFilePostParams(a);
	this.queueEvent("upload_error_handler", [a, c, b])
};
SWFUpload.prototype.uploadSuccess = function(b, a, c) {
	b = this.unescapeFilePostParams(b);
	this.queueEvent("upload_success_handler", [b, a, c])
};
SWFUpload.prototype.uploadComplete = function(a) {
	a = this.unescapeFilePostParams(a);
	this.queueEvent("upload_complete_handler", a)
};
SWFUpload.prototype.debug = function(a) {
	this.queueEvent("debug_handler", a)
};
SWFUpload.prototype.debugMessage = function(c) {
	if (this.settings.debug) {
		var a,
		d = [];
		if (typeof c === "object" && typeof c.name === "string" && typeof c.message === "string") {
			for (var b in c) {
				if (c.hasOwnProperty(b)) {
					d.push(b + ": " + c[b])
				}
			}
			a = d.join("\n") || "";
			d = a.split("\n");
			a = "EXCEPTION: " + d.join("\nEXCEPTION: ");
			SWFUpload.Console.writeLine(a)
		} else {
			SWFUpload.Console.writeLine(c)
		}
	}
};
SWFUpload.Console = {};
SWFUpload.Console.writeLine = function(d) {
	var b,
	a;
	try {
		b = document.getElementById("SWFUpload_Console");
		if (!b) {
			a = document.createElement("form");
			document.getElementsByTagName("body")[0].appendChild(a);
			b = document.createElement("textarea");
			b.id = "SWFUpload_Console";
			b.style.fontFamily = "monospace";
			b.setAttribute("wrap", "off");
			b.wrap = "off";
			b.style.overflow = "auto";
			b.style.width = "700px";
			b.style.height = "350px";
			b.style.margin = "5px";
			a.appendChild(b)
		}
		b.value += d + "\n";
		b.scrollTop = b.scrollHeight - b.clientHeight
	} catch(c) {
		alert("Exception: " + c.name + " Message: " + c.message)
	}
};

/*
Uploadify v3.0.0
Copyright (c) 2010 Ronnie Garcia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

if (jQuery) { (function(a) {
		a.extend(a.fn, {
			uploadify: function(b, c) {
				a(this).each(function() {
					var r = a(this).clone();
					var k = a.extend({
						id: a(this).attr("id"),
						swf: "uploadify.swf",
						uploader: "uploadify.php",
						auto: false,
						buttonClass: "",
						buttonCursor: "hand",
						buttonImage: false,
						buttonText: "SELECT FILES",
						cancelImage: "uploadify-cancel.png",
						checkExisting: "uploadify-check-existing.php",
						debug: false,
						fileObjName: "Filedata",
						fileSizeLimit: 0,
						fileTypeDesc: "All Files (*.*)",
						fileTypeExts: "*.*",
						height: 30,
						method: "post",
						multi: false,
						queueID: false,
						queueSizeLimit: 999,
						removeCompleted: true,
						removeTimeout: 3,
						requeueErrors: true,
						postData: {},
						preventCaching: true,
						progressData: "percentage",
						successTimeout: 30,
						transparent: true,
						uploadLimit: 999,
						uploaderType: "html5",
						width: 120,
						skipDefault: [],
						onClearQueue: function() {},
						onDialogOpen: function() {},
						onDialogClose: function() {},
						onInit: function() {},
						onQueueComplete: function() {},
						onSelectError: function() {},
						onSelect: function() {},
						onSWFReady: function() {},
						onUploadCancel: function() {},
						onUploadComplete: function() {},
						onUploadError: function() {},
						onUploadProgress: function() {},
						onUploadStart: function() {}
					},
					b);
					var d = {
						assume_success_timeout: k.successTimeout,
						button_placeholder_id: k.id,
						button_image_url: k.buttonImage,
						button_width: k.width,
						button_height: k.height,
						button_text: null,
						button_text_style: null,
						button_text_top_padding: 0,
						button_text_left_padding: 0,
						button_action: (k.multi ? SWFUpload.BUTTON_ACTION.SELECT_FILES: SWFUpload.BUTTON_ACTION.SELECT_FILE),
						button_disabled: false,
						button_cursor: (k.buttonCursor == "arrow" ? SWFUpload.CURSOR.ARROW: SWFUpload.CURSOR.HAND),
						button_window_mode: (k.transparent && !k.buttonImage ? SWFUpload.WINDOW_MODE.TRANSPARENT: SWFUpload.WINDOW_MODE.OPAQUE),
						debug: k.debug,
						requeue_on_error: k.requeueErrors,
						file_post_name: k.fileObjName,
						file_size_limit: k.fileSizeLimit,
						file_types: k.fileTypeExts,
						file_types_description: k.fileTypeDesc,
						file_queue_limit: k.queueSizeLimit,
						file_upload_limit: k.uploadLimit,
						flash_url: k.swf,
						prevent_swf_caching: k.preventCaching,
						post_params: k.postData,
						upload_url: k.uploader,
						use_query_string: (k.method == "get"),
						file_dialog_complete_handler: e,
						file_dialog_start_handler: t,
						file_queued_handler: p,
						file_queue_error_handler: q,
						flash_ready_handler: k.onSWFReady,
						upload_complete_handler: i,
						upload_error_handler: s,
						upload_progress_handler: g,
						upload_start_handler: h,
						upload_success_handler: n
					};
					if (c) {
						d = a.extend(d, c)
					}
					d = a.extend(d, k);
					window["uploadify_" + k.id] = new SWFUpload(d);
					var j = window["uploadify_" + k.id];
					j.original = r;
					var f = a("<div />", {
						id: k.id,
						"class": "uploadify",
						css: {
							height: k.height + "px",
							position: "relative",
							width: k.width + "px"
						}
					});
					a("#" + j.movieName).wrap(f);
					if (!k.queueID) {
						var m = a("<div />", {
							id: k.id + "_queue",
							"class": "uploadifyQueue"
						});
						a("#" + k.id).after(m);
						j.settings.queueID = k.queueID = k.id + "_queue"
					}
					j.queue = {
						files: {},
						filesSelected: 0,
						filesQueued: 0,
						filesReplaced: 0,
						filesCancelled: 0,
						filesErrored: 0,
						averageSpeed: 0,
						queueLength: 0,
						queueSize: 0,
						uploadSize: 0,
						queueBytesUploaded: 0,
						uploadQueue: [],
						errorMsg: "Some files were not added to the queue:"
					};
					if (!k.buttonImage) {
						var l = a("<div />", {
							id: k.id + "_button",
							"class": "uploadifyButton " + k.buttonClass,
							html: '<span class="uploadifyButtonText">' + k.buttonText + "</span>"
						});
						a("#" + k.id).append(l);
						a("#" + j.movieName).css({
							position: "absolute",
							"z-index": 1
						})
					} else {
						a("#" + j.movieName).addClass(k.buttonClass)
					}
					function e(u, w, x) {
						var v = j.getStats();
						j.queue.filesErrored = u - w;
						j.queue.filesSelected = u;
						j.queue.filesQueued = w - j.queue.filesCancelled;
						j.queue.queueLength = x;
						if (a.inArray("onDialogClose", j.settings.skipDefault) < 0) {
							if (j.queue.filesErrored > 0) {
								alert(j.queue.errorMsg)
							}
						}
						if (j.settings.onDialogClose) {
							j.settings.onDialogClose(j.queue)
						}
						if (j.settings.auto) {
							a("#" + j.settings.id).uploadifyUpload("*")
						}
					}
					function t() {
						j.queue.errorMsg = "Some files were not added to the queue:";
						j.queue.filesReplaced = 0;
						j.queue.filesCancelled = 0;
						if (j.settings.onDialogOpen) {
							j.settings.onDialogOpen()
						}
					}
					function p(w) {
						if (a.inArray("onSelect", j.settings.skipDefault) < 0) {
							var v = {};
							for (var B in j.queue.files) {
								v = j.queue.files[B];
								if (v.name == w.name) {
									var x = confirm('The file named "' + w.name + '" is already in the queue.\nDo you want to replace the existing item in the queue?');
									if (!x) {
										j.cancelUpload(w.id);
										j.queue.filesCancelled++;
										return false
									} else {
										a("#" + v.id).remove();
										j.cancelUpload(v.id);
										j.queue.filesReplaced++
									}
								}
							}
							var u = Math.round(w.size / 1024);
							var z = "KB";
							if (u > 1000) {
								u = Math.round(u / 1000);
								z = "MB"
							}
							var y = u.toString().split(".");
							u = y[0];
							if (y.length > 1) {
								u += "." + y[1].substr(0, 2)
							}
							u += z;
							var A = w.name;
							if (A.length > 25) {
								A = A.substr(0, 25) + "..."
							}
							a("#" + j.settings.queueID).append('<div id="' + w.id + '" class="uploadifyQueueItem"><div class="cancel"><a href="javascript:jQuery(\'#' + j.settings.id + "').uploadifyCancel('" + w.id + '\')"><img src="' + j.settings.cancelImage + '" border="0" /></a></div><span class="fileName">' + A + " (" + u + ')</span><span class="data"></span><div class="uploadifyProgress"><div class="uploadifyProgressBar"><!--Progress Bar--></div></div></div>');
							j.queue.queueSize += w.size
						}
						j.queue.files[w.id] = w;
						if (j.settings.onSelect) {
							j.settings.onSelect(w)
						}
					}
					function q(u, w, v) {
						if (a.inArray("onSelectError", j.settings.skipDefault) < 0) {
							switch (w) {
							case SWFUpload.QUEUE_ERROR.QUEUE_LIMIT_EXCEEDED:
								if (j.settings.queueSizeLimit > v) {
									j.queue.errorMsg += "\nThe number of files selected exceeds the remaining upload limit (" + v + ")."
								} else {
									j.queue.errorMsg += "\nThe number of files selected exceeds the queue size limit (" + j.settings.queueSizeLimit + ")."
								}
								break;
							case SWFUpload.QUEUE_ERROR.FILE_EXCEEDS_SIZE_LIMIT:
								j.queue.errorMsg += '\nThe file "' + u.name + '" exceeds the size limit (' + j.settings.fileSizeLimit + ").";
								break;
							case SWFUpload.QUEUE_ERROR.ZERO_BYTE_FILE:
								j.queue.errorMsg += '\nThe file "' + u.name + '" is empty.';
								break;
							case SWFUpload.QUEUE_ERROR.FILE_EXCEEDS_SIZE_LIMIT:
								j.queue.errorMsg += '\nThe file "' + u.name + '" is not an accepted file type (' + j.settings.fileTypeDesc + ").";
								break
							}
						}
						if (w != SWFUpload.QUEUE_ERROR.QUEUE_LIMIT_EXCEEDED) {
							delete j.queue.files[u.id]
						}
						if (j.settings.onSelectError) {
							j.settings.onSelectError(u, w, v)
						}
					}
					function o() {
						var u = j.getStats();
						if (j.settings.onQueueComplete) {
							j.settings.onQueueComplete(u)
						}
					}
					function i(v) {
						var u = j.getStats();
						j.queue.queueLength = u.files_queued;
						if (j.queue.uploadQueue[0] == "*") {
							if (j.queue.queueLength > 0) {
								j.startUpload()
							} else {
								j.queue.uploadQueue = [];
								if (j.settings.onQueueComplete) {
									j.settings.onQueueComplete(u)
								}
							}
						} else {
							if (j.queue.uploadQueue.length > 0) {
								j.startUpload(j.queue.uploadQueue.shift())
							} else {
								j.queue.uploadQueue = [];
								if (j.settings.onQueueComplete) {
									setting.onQueueComplete(u)
								}
							}
						}
						if (a.inArray("onUploadComplete", j.settings.skipDefault) < 0) {
							if (j.settings.removeCompleted) {
								switch (v.filestatus) {
								case SWFUpload.FILE_STATUS.COMPLETE:
									setTimeout(function() {
										if (a("#" + v.id)) {
											j.queue.queueSize -= v.size;
											delete j.queue.files[v.id];
											a("#" + v.id).fadeOut(500,
											function() {
												a(this).remove()
											})
										}
									},
									j.settings.removeTimeout * 1000);
									break;
								case SWFUpload.FILE_STATUS.ERROR:
									if (!j.settings.requeueErrors) {
										setTimeout(function() {
											if (a("#" + v.id)) {
												j.queue.queueSize -= v.size;
												delete j.queue.files[v.id];
												a("#" + v.id).fadeOut(500,
												function() {
													a(this).remove()
												})
											}
										},
										j.settings.removeTimeout * 1000)
									}
									break
								}
							}
						}
						if (j.settings.onUploadComplete) {
							j.settings.onUploadComplete(v, j.queue)
						}
					}
					function s(u, x, w) {
						var v = "Error";
						if (x != SWFUpload.UPLOAD_ERROR.FILE_CANCELLED && x != SWFUpload.UPLOAD_ERROR.UPLOAD_STOPPED) {
							a("#" + u.id).addClass("uploadifyError")
						}
						a("#" + u.id).find(".uploadifyProgressBar").css("width", "1px");
						switch (x) {
						case SWFUpload.UPLOAD_ERROR.HTTP_ERROR:
							v = "HTTP Error (" + w + ")";
							break;
						case SWFUpload.UPLOAD_ERROR.MISSING_UPLOAD_URL:
							v = "Missing Upload URL";
							break;
						case SWFUpload.UPLOAD_ERROR.IO_ERROR:
							v = "IO Error";
							break;
						case SWFUpload.UPLOAD_ERROR.SECURITY_ERROR:
							v = "Security Error";
							break;
						case SWFUpload.UPLOAD_ERROR.UPLOAD_LIMIT_EXCEEDED:
							alert("The upload limit has been reached (" + w + ").");
							v = "Exceeds Upload Limit";
							break;
						case SWFUpload.UPLOAD_ERROR.UPLOAD_FAILED:
							v = "Failed";
							break;
						case SWFUpload.UPLOAD_ERROR.SPECIFIED_FILE_ID_NOT_FOUND:
							break;
						case SWFUpload.UPLOAD_ERROR.FILE_VALIDATION_FAILED:
							v = "Validation Error";
							break;
						case SWFUpload.UPLOAD_ERROR.FILE_CANCELLED:
							v = "Cancelled";
							j.queue.queueSize -= u.size;
							if (u.status == SWFUpload.FILE_STATUS.IN_PROGRESS || a.inArray(u.id, j.queue.uploadQueue) >= 0) {
								j.queue.uploadSize -= u.size
							}
							delete j.queue.files[u.id];
							break;
						case SWFUpload.UPLOAD_ERROR.UPLOAD_STOPPED:
							v = "Stopped";
							break
						}
						if (x != SWFUpload.UPLOAD_ERROR.SPECIFIED_FILE_ID_NOT_FOUND && u.status != SWFUpload.FILE_STATUS.COMPLETE) {
							a("#" + u.id).find(".data").html(" - " + v)
						}
						if (j.settings.onUploadError) {
							j.settings.onUploadError(u, x, w, v, j.queue)
						}
					}
					function g(x, C, z) {
						var v = new Date();
						var D = v.getTime();
						var A = D - j.timer;
						j.timer = D;
						var y = C - j.bytesLoaded;
						j.bytesLoaded = C;
						var u = j.queue.queueBytesUploaded + C;
						var F = Math.round(C / z * 100);
						var B = 0;
						var w = (y / 1024) / (A / 1000);
						w = Math.floor(w * 10) / 10;
						if (j.queue.averageSpeed > 0) {
							j.queue.averageSpeed = (j.queue.averageSpeed + w) / 2
						} else {
							j.queue.averageSpeed = w
						}
						if (w > 1000) {
							B = (w * 0.001);
							j.queue.averageSpeed = B
						}
						var E = "KB/s";
						if (B > 0) {
							E = "MB/s"
						}
						if (a.inArray("onUploadProgress", j.settings.skipDefault) < 0) {
							if (j.settings.progressData == "percentage") {
								a("#" + x.id).find(".data").html(" - " + F + "%")
							} else {
								if (j.settings.progressData == "speed") {
									a("#" + x.id).find(".data").html(" - " + F + E)
								}
							}
							a("#" + x.id).find(".uploadifyProgressBar").css("width", F + "%")
						}
						if (j.settings.onUploadProgress) {
							j.settings.onUploadProgress(x, C, z, u, j.queue.uploadSize)
						}
					}
					function h(u) {
						var v = new Date();
						j.timer = v.getTime();
						j.bytesLoaded = 0;
						if (j.queue.uploadQueue.length == 0) {
							j.queue.uploadSize = u.size
						}
						if (j.settings.checkExisting !== false) {
							a.ajax({
								type: "POST",
								async: false,
								url: j.settings.checkExisting,
								data: {
									filename: u.name
								},
								success: function(x) {
									if (x == 1) {
										var w = confirm('A file with the name "' + u.name + '" already exists on the server.\nWould you like to replace the existing file?');
										if (!w) {
											j.cancelUpload(u.id);
											a("#" + u.id).remove();
											if (j.queue.uploadQueue.length > 0 && j.queue.queueLength > 0) {
												if (j.queue.uploadQueue[0] == "*") {
													j.startUpload()
												} else {
													j.startUpload(j.queue.uploadQueue.shift())
												}
											}
										}
									}
								}
							})
						}
						if (j.settings.onUploadStart) {
							j.settings.onUploadStart(u)
						}
					}
					function n(v, w, u) {
						j.queue.queueBytesUploaded += v.size;
						a("#" + v.id).find(".data").html(" - Complete");
						if (j.settings.onUploadSuccess) {
							j.settings.onUploadSuccess(v, w, u)
						}
					}
				})
			},
			uploadifyCancel: function(b) {
				var f = a(this).selector.replace("#", "");
				var d = window["uploadify_" + f];
				var c = -1;
				if (arguments[0]) {
					if (arguments[0] == "*") {
						a("#" + d.settings.queueID).find(".uploadifyQueueItem").each(function() {
							c++;
							d.cancelUpload(a(this).attr("id"));
							a(this).delay(100 * c).fadeOut(500,
							function() {
								a(this).remove()
							})
						});
						d.queue.queueSize = 0
					} else {
						for (var e = 0; e < arguments.length; e++) {
							d.cancelUpload(arguments[e]);
							a("#" + arguments[e]).delay(100 * e).fadeOut(500,
							function() {
								a(this).remove()
							})
						}
					}
				} else {
					a("#" + d.settings.queueID).find(".uploadifyQueueItem").get(0).fadeOut(500,
					function() {
						a(this).remove();
						d.cancelUpload(a(this).attr("id"))
					})
				}
			},
			uploadifyDestroy: function() {
				var c = a(this).selector.replace("#", "");
				var b = window["uploadify_" + c];
				b.destroy();
				a("#" + c + "_queue").remove();
				a("#" + c).replaceWith(b.original);
				delete window["uploadify_" + c]
			},
			uploadifyDisable: function(b) {
				var d = a(this).selector.replace("#", "");
				var c = window["uploadify_" + d];
				c.setButtonDisabled(b)
			},
			uploadifySettings: function(d, e, f) {
				var h = a(this).selector.replace("#", "");
				var c = window["uploadify_" + h];
				if (typeof(arguments[0]) == "object") {
					for (var g in e) {
						b(g, e[g])
					}
				}
				if (arguments.length == 1) {
					return c.settings[d]
				} else {
					b(d, e, f)
				}
				function b(i, j, k) {
					switch (i) {
					case "uploader":
						c.setUploadURL(j);
						break;
					case "postData":
						if (!k) {
							e = a.extend(c.settings.postData, j)
						}
						c.setPostParams(j);
						break;
					case "method":
						if (j == "get") {
							c.setUseQueryString(true)
						} else {
							c.setUseQueryString(false)
						}
						break;
					case "fileObjName":
						c.setFilePostName(j);
						break;
					case "fileTypeExts":
						c.setFileTypes(j, c.settings.fileTypeDesc);
						break;
					case "fileTypeDesc":
						c.setFileTypes(c.settings.fileTypeExts, j);
						break;
					case "fileSizeLimit":
						c.setFileSizeLimit(j);
						break;
					case "uploadLimit":
						c.setFileUploadLimit(j);
						break;
					case "queueSizeLimit":
						c.setFileQueueLimit(j);
						break;
					case "buttonImage":
						a("#" + c.settings.id + "_button").remove();
						c.setButtonImageURL(j);
						break;
					case "buttonCursor":
						if (j == "arrow") {
							c.setButtonCursor(SWFUpload.CURSOR.ARROW)
						} else {
							c.setButtonCursor(SWFUpload.CURSOR.HAND)
						}
						break;
					case "buttonText":
						a("#" + c.settings.id + "_button").find(".uploadifyButtonText").html(j);
						break;
					case "width":
						c.setButtonDimensions(j, c.settings.height);
						break;
					case "height":
						c.setButtonDimensions(c.settings.width, j);
						break;
					case "multi":
						if (j) {
							c.setButtonAction(SWFUpload.BUTTON_ACTION.SELECT_FILES)
						} else {
							c.setButtonAction(SWFUpload.BUTTON_ACTION.SELECT_FILE)
						}
						break
					}
					c.settings[i] = e
				}
			},
			uploadifyStop: function() {
				var c = a(this).selector.replace("#", "");
				var b = window["uploadify_" + c];
				b.stopUpload()
			},
			uploadifyUpload: function() {
				var d = a(this).selector.replace("#", "");
				var b = window["uploadify_" + d];
				b.queue.averageSpeed = 0;
				b.queue.uploadSize = 0;
				b.queue.bytesUploaded = 0;
				b.queue.uploadQueue = [];
				if (arguments[0]) {
					if (arguments[0] == "*") {
						b.queue.uploadSize = b.queue.queueSize;
						b.queue.uploadQueue.push("*");
						b.startUpload()
					} else {
						for (var c = 0; c < arguments.length; c++) {
							b.queue.uploadSize += b.queue.files[arguments[c]].size;
							b.queue.uploadQueue.push(arguments[c])
						}
						b.startUpload(b.queue.uploadQueue.shift())
					}
				} else {
					b.startUpload()
				}
			}
		})
	})(jQuery)
};
