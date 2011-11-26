$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#replyform").live("submit", function() {
        newReply($(this));
        return false;
    });
    $("#replyform").live("keypress", function(e) {
        if (e.keyCode == 13) {
            newReply($(this));
            return false;
        }
    });
    $("#reply").select();
    
    $(".reply").click(function() {
        showReply($(this));
        return false;
    });
    
    
});

function showReply(e) {
    var $p = $(e).parent().parent();
    var args = {'id': $p.attr('id').replace("m-","")}
    $.postJSON("/a/reply", "GET", args, function(response) {
        if (response.error){
            return alert(response.error);
        }
        $p.append("<ul class='rep-list'></ul>")
        for (var i=0; i<response.length; i++) {
            $(".rep-list").append(response[i]);
        }
    });

};

function hideReply() {
    
};

function newReply(form) {
    var message = form.formToDict();
    var disabled = form.find("input[type=submit]");
    disabled.disable();
    $.postJSON("/a/reply", "POST", message, function(response) {
        if (response.error){
            disabled.enable();
            return alert(response.error);
        }
        insertReply(response);
        form.find("#reply").val("").select();
        disabled.enable();
    });
};

function insertReply(message) {
    var existing = $("#m" + message.id);
    if (existing.length > 0) return;
    var node = $(message.html);
    node.hide();
    $("#inbox").append(node);
    node.slideDown();
}

jQuery.postJSON = function(url, type, args, callback) {
    $.ajax({url: url, data: $.param(args), dataType: "text", type: type,
            success: function(response) {
        if (callback) callback(eval("(" + response + ")"));
    }, error: function(response) {
        console.log("ERROR:", response)
    }});
};

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

jQuery.fn.disable = function() {
    this.enable(false);
    return this;
};

jQuery.fn.enable = function(opt_enable) {
    if (arguments.length && !opt_enable) {
        this.attr("disabled", "disabled");
    } else {
        this.removeAttr("disabled");
    }
    return this;
};
