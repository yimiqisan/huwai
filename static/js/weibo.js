var Weibo = {
    init: function(){
        $("#weiboform").live("submit", function() {
            Weibo.new($(this));
            return false;
        })
        Weibo.getLen();
        $("#weibo-content").select();
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
        var mtp = $('#weibo .wb_items').attr('maintype');
        var stp = $('#weibo .wb_items').attr('subtype');
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
