$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};
    var extend_id = null;
    $(".reply").click(function() {
        click_id = $(this).attr("id").replace("r-","m-");
        if (extend_id == click_id) {
            Reply.hide(click_id);
        }else{
            $('#'+extend_id).find(".rep-list").hide();
            Reply.show(click_id);
            extend_id = click_id;
        }
        return false;
    });
});

var Reply = {
    show: function(id){
        var args = {'id': id.replace("m-","")}
        $.postJSON("/a/reply", "GET", args, function(response) {
            if (response.error){
                return alert(response.error);
            }
            var $cur = $('#'+id+' .content');
            $cur.find(".rep-list").remove();
            $cur.append('<div node-type="feed_list_repeat" class="repeat W_textc W_linecolor W_bgcolor rep-list"><div node-type="commentList" class="input clearfix"><form action="/a/reply" method="post" id="replyform"><input name="content" id="reply" style="margin:0 0 3px 0; padding：4px 4px 0 4px; border: 1px solid rgb(198, 198, 198); font-size: 12px; font-family: Tahoma, 宋体; word-wrap: break-word; line-height: 18px; outline-style: none; outline-width: initial; outline-color: initial; overflow-x: hidden; overflow-y: hidden; height: 22px;" /><input style="margin-top:5px;float:right;" type="submit" value="回复"/></form><div class="action clearfix" node-type="widget"></div></div><div class="comment_lists" node-type="feed_list_commentList"></div></div>');
            for (var i=0; i<response.length; i++) {
                $cur.find(".rep-list").append(response[i]);
            }
            Reply.submit($('#replyform'));
        });
    },
/*    
<div node-type="feed_list_repeat" class="repeat W_textc W_linecolor W_bgcolor rep-list">
    <div node-type="commentList" class="input clearfix">
        <form action="/a/reply" method="post" id="replyform">
            <input name="content" id="reply" style="margin:0 0 3px 0; padding：4px 4px 0 4px; border: 1px solid rgb(198, 198, 198); font-size: 12px; font-family: Tahoma, 宋体; word-wrap: break-word; line-height: 18px; outline-style: none; outline-width: initial; outline-color: initial; overflow-x: hidden; overflow-y: hidden; height: 22px;" />
            <input style="margin-top:5px;float:right;" type="submit" value="回复"/>
        </form>
        <div class="action clearfix" node-type="widget"></div>
    </div>
    <div class="comment_lists" node-type="feed_list_commentList"></div>
</div>
*/
    
    hide: function(id){
        $('#'+id+' .rep-list').toggle();
    },
    
    submit: function(e){
        $("#replyform").live("submit", function() {
            Reply.insert(e);
            return false;
        });
        $("#replyform").live("keypress", function() {
            if (e.keyCode == 13) {
                Reply.insert(e);
                return false;
            }
        });
        $("#reply").select();
    },
    
    insert: function(form){
        var message = form.formToDict();
        alert(form.parent().parent().parent().parent().attr("id"));
        message["to"] = form.parent().parent().parent().parent().attr("id").replace("m-", "");
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
            form.find("#reply").val("").select();
            disabled.enable();
        });
    },
    
    remove: function(did) {
        var mid = did.replace("d-", "mr-");
        var $p = $("#"+mid);
        var args = {'id': did.replace("d-","")};
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
    }

}


