$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#messageform").live("submit", function() {
        newMessage($(this));
        return false;
    });
    $("#messageform").live("keypress", function(e) {
        if (e.keyCode == 13) {
            newMessage($(this));
            return false;
        }
    });
    $("#message").select();
    updater.start();
});

function newMessage(form) {
    var message = form.formToDict();
    updater.socket.send(JSON.stringify(message));
    form.find("input[type=text]").val("").select();
}

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

var updater = {
    socket: null,

    start: function() {
        var url = "ws://" + location.host + "/chatsocket";
        if ("WebSocket" in window) {
	    updater.socket = new WebSocket(url);
        } else {
            updater.socket = new MozWebSocket(url);
        }
	updater.socket.onmessage = function(event) {
	    updater.showMessage(JSON.parse(event.data));
	}
    },

    showMessage: function(message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        node.hide();
        $("#inbox").append(node);
        node.slideDown();
    }
};




var Alert = {
    init: function(){
        Alert.list();
    },
    
    list: function() {
        var args = {};
        var e = $('#alert');
        $.postJSON("/a/alert/", "GET", args, function(response) {
            if (response.error){
                return alert(response.error);
            }
            htmls = response.htmls;
            if (htmls.length > 0){for (var i=0; i<htmls.length; i++) {e.append(htmls[i]);}}
            else {$(e).parent().css('display', 'none');}
        });
    },
    
    click: function(e) {
        var args = {};
        var subject = $(e).attr('subject');
        args['subject'] = subject
        $.postJSON("/a/alert/", 'POST', args, function(response) {
            if (response.error){
                disabled.enable();
                return alert(response.error);
            }
            $(e).css('display', 'none');
            window.location.href = '/alert/'+subject;
        });
    }
};
