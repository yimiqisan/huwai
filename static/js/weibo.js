$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#weiboform").live("submit", function() {
        newWeibo($(this));
        return false;
    });
    getLenWeibo();
    hoverWeibo();
    $("#reply").select();
});

function hoverWeibo(){
    $(".message").hover(function(){
            $(this).find(".reply:first").show();
            $(this).find(".remove:first").show();
        },function(){
            $(this).find(".reply:first").hide();
            $(this).find(".remove:first").hide();
        });
};

function newWeibo(form) {
    var message = form.formToDict();
    var disabled = form.find("input[type=submit]");
    disabled.disable();
    $.postJSON("/weibo/a/new", 'POST', message, function(response) {
        if (response.error){
            disabled.enable();
            return alert(response.error);
        }
        insertWeibo(response);
        form.find("#weibo-content").val("").select();
        $("#num").text(140);
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
    hoverWeibo();
};

function getLenWeibo(){
    var max_len = 140;
    $("#num").text(max_len - $("#weibo-content").val().length);
    $("#weibo-content").bind('change ' + ($.browser.msie ? "propertychange" : "input"), function(event){
        var val = $.trim($(this).val()), len = val.length;
        if(len > max_len){ $(this).val(val.substr(0, max_len)); }
        else{ $("#num").text(max_len - len); }
    });
}

