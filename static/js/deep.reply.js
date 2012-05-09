var Reply = {
    toggle: function(e) {
        mid = $(e).attr('id').replace('r-', 'm-');
        var isHas = $('#'+mid).hasClass('disp-re');
        if (isHas) {
            $('#'+mid+' .wb_rep_list').toggle();
        }else{
            Reply.list(mid);
            $('#'+mid).addClass('disp-re');
        }
    },
    
    list: function(id) {
        var args = {'id': id.replace("m-","")};
        $.postJSON("/a/reply", "GET", args, function(response) {
            if (response.error){
                return alert(response.error);
            }
            var $cur = $('#'+id+' .content');
            $cur.find(".wb_rep_list").remove();
            $cur.append('<div class="wb_rep_list"><div class="input clearfix"><form action="/a/reply" method="post" class="replyform"><input name="content" class="reply-content" style="width:85%;margin:0 0 3px 0; padding：4px 4px 0 4px; border: 1px solid rgb(198, 198, 198); font-size: 12px; font-family: Tahoma, 宋体; word-wrap: break-word; line-height: 18px; outline-style: none; outline-width: initial; outline-color: initial; overflow-x: hidden; overflow-y: hidden; height: 22px;"><input class="btn pull-right" type="submit" value="回复"></form><div class="action clearfix"></div></div></div>');
            $cur.find(".wb_rep_list").append("<div class='bottom'><a style='margin-top:10px;display:block;text-align:center;' onclick=Reply.extend('"+id+"');return false;>下拉</a><input type='hidden' value='0'></div>");
            var e = $("#"+id+" .wb_rep_list .bottom");
            $(e).find('a').text('').addClass('loading');
            htmls = response.htmls;
            for (var i=0; i<htmls.length; i++) {
                $(htmls[i]).insertBefore(e);
            }
            if (htmls.length < 10){
                $(e).find('a').text('没有更多的了').removeClass('loading');
                $(e).find('input').val(-1);
            }else{
                $(e).find('a').text('下拉').removeClass('loading');
                $(e).find('input').val(response.cursor);
            }
            Reply.submit(id);
        });
    },
    
    extend: function(id) {
        var e = $(".wb_rep_list .bottom");
        if ($(e).find('input').val()=='-1'){$(e).find('a').text('没有更多的了');return false;}
        var args = {'id': id.replace("m-",""), 'cursor': $(e).find('input').val()};
        $(e).find('a').text('').addClass('loading');
        $.postJSON("/a/reply", "GET", args, function(response) {
            if (response.error){
                return alert(response.error);
            }
            htmls = response.htmls;
            for (var i=0; i<htmls.length; i++) {
                $(htmls[i]).insertBefore(e);
            }
            if (htmls.length < 10){
                $(e).find('a').text('没有更多的了').removeClass('loading');
                $(e).find('input').val(-1);
            }else{
                if (response.cursor==-1){
                    $(e).find('a').text('没有更多的了').removeClass('loading');
                }else{
                    $(e).find('a').text('下拉').removeClass('loading');
                }
                $(e).find('input').val(response.cursor);
            }
        });
    },
    
    submit: function(id){
        if (!$.cookie("uid")) {
            $('#login').modal();
            return false;
        }
        var e = $('#'+id+' .replyform');
        e.live("submit", function() {
            Reply.insert(e, id.replace('m-', ''));
            return false;
        });
        e.live("keypress", function() {
            if (e.keyCode == 13) {
                Reply.insert(e, id.replace('m-', ''));
                return false;
            }
        });
        $('#'+id+' .reply-content').select();
    },
    
    insert: function(form, id) {
        if ($('#m-'+id+' .reply-content').val() == ""){return false;}
        var message = form.formToDict();
        message["to"] = id
        var disabled = form.find("input[type=submit]");
        disabled.disable();
        $.postJSON("/a/reply", "POST", message, function(response) {
            if (response.error){
                disabled.enable();
                return alert(response.error);
            }
            var existing = $("#r-" + response.id);
            if (existing.length > 0) return;
            var node = $(response.html);
            node.hide();
            $(node).insertAfter($("#m-"+id+" .wb_rep_list .input"));
            node.slideDown();
            form.find(".reply-content").val("").select();
            disabled.enable();
        });
    },
    
    reply: function(e) {
        var mid = 'm-'+$(e).attr('to');
        var nick = $(e).attr('nick');
        $('#'+mid+' .reply-content').val('@'+nick+' ');
    }
}





!function( $ ){

    "use strict"

    /* REPLY CLASS DEFINITION */
    var Reply = function ( content, options ) {
        this.options = options
        this.$element = $(content).delegate('[data-dismiss="reply"]', 'click.dismiss.reply', $.proxy(this.hide, this))
    }

    Reply.prototype = {
        constructor: Reply,
        
        toggle: function () {
            return this[!this.isShown ? 'show' : 'hide']()
        },
        show: function () {
            
        },
        hide: function ( e ) {
            
        },
        list: function ( e ) {
            return
            var args = {'id': id.replace("m-","")};
            $.postJSON("/a/reply", "GET", args, function(response) {
                if (response.error){
                    return alert(response.error);
                }
                var $cur = $('#'+id+' .content');
                $cur.find(".wb_rep_list").remove();
                $cur.append('<div class="wb_rep_list"><div class="input clearfix"><form action="/a/reply" method="post" class="replyform"><input name="content" class="reply-content" style="width:85%;margin:0 0 3px 0; padding：4px 4px 0 4px; border: 1px solid rgb(198, 198, 198); font-size: 12px; font-family: Tahoma, 宋体; word-wrap: break-word; line-height: 18px; outline-style: none; outline-width: initial; outline-color: initial; overflow-x: hidden; overflow-y: hidden; height: 22px;"><input class="btn pull-right" type="submit" value="回复"></form><div class="action clearfix"></div></div></div>');
                $cur.find(".wb_rep_list").append("<div class='bottom'><a style='margin-top:10px;display:block;text-align:center;' onclick=Reply.extend('"+id+"');return false;>下拉</a><input type='hidden' value='0'></div>");
                var e = $("#"+id+" .wb_rep_list .bottom");
                $(e).find('a').text('').addClass('loading');
                htmls = response.htmls;
                for (var i=0; i<htmls.length; i++) {
                    $(htmls[i]).insertBefore(e);
                }
                if (htmls.length < 10){
                    $(e).find('a').text('没有更多的了').removeClass('loading');
                    $(e).find('input').val(-1);
                }else{
                    $(e).find('a').text('下拉').removeClass('loading');
                    $(e).find('input').val(response.cursor);
                }
                Reply.submit(id);
            });
        },
        extend: function ( e ) {
            
        },
        submit: function ( e ) {
            
        },
        insert: function ( e ) {
            
        },
        at: function ( e ) {
            
        }
    }
    /* REPLY PRIVATE METHODS */

    /* REPLY PLUGIN DEFINITION */

    $.fn.reply = function ( option ) {
        return this.each(function () {
            alert($(this).attr('id'));
            var $this = $(this), data = $this.data('reply'), options = $.extend({}, $.fn.reply.defaults, $this.data(), typeof option == 'object' && option)
            if (!data) $this.data('reply', (data = new Reply(this, options)))
            if (typeof option == 'string') data[option]()
            else if (options.show) data.list($this)
        })
    }

    $.fn.reply.defaults = {
        url: '/a/reply/',
        template: '<dl class="replies"><dd id=""><a class="avatar minfriendpic" title="刘智勇"href=""><img width="50" height="50" alt="" src="/image/avatar/c18db1940a5e4c00a4b29f7206bc953f_50"></a><div class="info"><span class="pull-right" style="width:15px"><a class="x-to-hide" onclick="return false;" href="#nogo" alt="删除"></a></span><span class="author me"><a title="连续登录7天, 即可获得橙名特权" href="" class=" lively-user">刘智勇</a></span><span class="time">2008-07-02 22:41</span></div><div class="reply"><p class="content">回复李月：因为脸上有青春痘。</p></div></dd></dl>',
        backdrop: true,
        keyboard: true,
        show: true
    }

    $.fn.reply.Constructor = Reply

    /* REPLY DATA-API */

    $(function () {
        $('body').on('click.reply.data-api', '[data-toggle="reply"]', function ( e ) {
            var $this = $(this), href
            , target = $this.attr('data-target') || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '') //strip for ie7
            , option = $(target).data('reply') ? 'toggle' : $.extend({}, $(target).data(), $this.data())
            e.preventDefault()
            $(target).reply(option)
        })
    })
}( window.jQuery );














