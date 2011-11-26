$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#weiboform").live("submit", function() {
        newWeibo($(this));
        return false;
    });
    $("#weiboform").live("keypress", function(e) {
        if (e.keyCode == 13) {
            newWeibo($(this));
            return false;
        }
    });
    $("#reply").select();
});

function newWeibo(form) {
    var message = form.formToDict();
    var disabled = form.find("input[type=submit]");
    disabled.disable();
    $.postJSON("/weibo/a/new", message, function(response) {
        if (response.error){
            disabled.enable();
            return alert(response.error);
        }
        insertWeibo(response);
        form.find("#weibo-content").val("").select();
        disabled.enable();
    });
};

function insertWeibo(message) {
    var existing = $("#m" + message.id);
    if (existing.length > 0) return;
    var node = $(message.html);
    node.hide();
    $(node).insertBefore("#inbox .message:first");
    node.slideDown();
}

jQuery.postJSON = function(url, args, callback) {
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
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
