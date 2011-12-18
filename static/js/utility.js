function delItem(e) {
    var mid = $(e).attr('id').replace('d-', 'm-');
    var $p = $("#"+mid);
    var args = {'id': mid.replace('m-', '')};
    $.ajax({
        url: "/a/remove", 
        type: "POST", 
        dataType: "text",
        data: $.param(args), 
        beforeSend: function() {
            $p.css("color", "#D6EED8");
        },
        success: function() {
            $p.slideUp(300, function() {$p.remove();})
        }
    });
};

var Reply = {
    toggle: function(e) {
        mid = $(e).attr('id').replace('r-', 'm-');
        var isHas = $('#'+mid).hasClass('disp-re');
        if (isHas) {
            $('#'+mid+' .rep-list').toggle();
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
            $cur.find(".rep-list").remove();
            $cur.append('<div node-type="feed_list_repeat" class="repeat W_textc W_linecolor W_bgcolor rep-list"><div node-type="commentList" class="input clearfix"><form action="/a/reply" method="post" class="replyform"><input name="content" class="reply-content" style="margin:0 0 3px 0; padding：4px 4px 0 4px; border: 1px solid rgb(198, 198, 198); font-size: 12px; font-family: Tahoma, 宋体; word-wrap: break-word; line-height: 18px; outline-style: none; outline-width: initial; outline-color: initial; overflow-x: hidden; overflow-y: hidden; height: 22px;" /><input style="margin-top:5px;float:right;" type="submit" value="回复"/></form><div class="action clearfix" node-type="widget"></div></div><div class="comment_lists" node-type="feed_list_commentList"></div></div>');
            for (var i=0; i<response.length; i++) {
                $cur.find(".rep-list").append(response[i]);
            }
            Reply.submit(id);
        });
    },

//    extend: function(e) {},
    
    submit: function(id){
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
        //$("#reply").select();
    },
    
    insert: function(form, id) {
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
            $(".rep-list").append(node);
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

