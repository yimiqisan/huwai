$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};
    Weibo.init();
});

var Weibo = {
    init: function(){
        $("#weibo").html('<div class="num" node-type="num" style="display: block;font-size:16px;">还可以输入<span style="font-size:24px;color:#ff9933;" id="num">140</span> 字</div><form action="/weibo" method="post" id="weiboform"><textarea rows="5" cols="60" name="content" id="weibo-content"></textarea><input type="submit" value="回复" style="height:20px;"/><input type="hidden" name="_xsrf" value="ca61c7cf01cf4097bd14c959c519637a"/></form></div><br><hr><div class="feed_lists W_linka W_texta" id="inbox">');
        $("#weiboform").live("submit", function() {
            Weibo.new($(this));
            return false;
        });
        Weibo.getLen();
        Weibo.hover();
        $("#weibo-content").select();
        Weibo.list();
    },

    list: function() {
        var args = {};
        $.postJSON("/a/weibo", "GET", args, function(response) {
            if (response.error){
                return alert(response.error);
            }
            for (var i=0; i<response.length; i++) {
                $('#inbox').append(response[i]);
            }
            $('#inbox').append('<div class="bottom feed_list">更多</div>');
        });
    },

    hover: function(){
        $(".feed_list").hover(function(){
                $(this).find(".remove:first").show();
            },function(){
                $(this).find(".remove:first").hide();
            });
    },

    new: function(form) {
        var message = form.formToDict();
        var disabled = form.find("input[type=submit]");
        disabled.disable();
        $.postJSON("/a/weibo", 'POST', message, function(response) {
            if (response.error){
                disabled.enable();
                return alert(response.error);
            }
            Weibo.insert(response);
            form.find("#weibo-content").val("").select();
            $("#num").text(140);
            disabled.enable();
        });
    },

    insert: function(message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        node.hide();
        $(node).insertBefore("#inbox .feed_list:first");
        node.slideDown();
        Weibo.hover();
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
}


