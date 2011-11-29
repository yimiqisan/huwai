$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};
    var extend_id = null;
    $(".reply").click(function() {
        click_id = $(this).parent().parent().attr("id");
        if (extend_id == click_id) {
            Reply.hide($(this));
        }else{
            $('#'+extend_id).find(".extend").hide();
            Reply.show($(this));
            extend_id = click_id;
        }
        return false;
    });
});

var Reply = {
    show: function(e){
        var $p = $(e).parent().parent();
        var id = $p.attr('id');
        var args = {'id': id.replace("m-","")}
        $.postJSON("/a/reply", "GET", args, function(response) {
            if (response.error){
                return alert(response.error);
            }
            var $cur = $('#'+id);
            $cur.find(".extend").remove();
            $cur.append("<div class='extend'><ul class='rep-list'></ul></div>");
            for (var i=0; i<response.length; i++) {
                $cur.find(".rep-list").append(response[i]);
            }
            $cur.find(".extend").append("<form action='/a/reply' method='post' id='replyform'><input name='content' id='reply' style='margin-left:100px;height:20px;width:450px;' /><input type='submit' value='回复'/></form>");
            Reply.submit($("#replyform"));
        });
    },
    
    hide: function(e){
        var $p = $(e).parent().parent();
        $p.find(".extend").toggle();
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
        message["to"] = form.parent().parent().attr("id").replace("m-", "");
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


