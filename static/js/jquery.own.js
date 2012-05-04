jQuery.postJSON = function(url, type, args, callback) {
    $.ajax({url: url, data: $.param(args), dataType: "text", type: type, async: false,
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

function login() {
    $("#login form").submit(function(){
        $(".help-inline").addClass("hide");
        $(".control-group").removeClass("error");
        var args = {};
        $("#login .control-group").each(function(){
            var inp = $(this).find("input");
            args[inp.attr('name')] = inp.val()
            if(!inp.val()) {
                $(this).addClass("error");
                $(this).find(".help-inline").removeClass("hide");
            }
        })
        $.postJSON("/a/login/", "POST", args, function(response) {
            if (response.error){
                return alert(response.error);
            }
            $.cookie("uid", response.uid, {path: '/', expires: 1});
            window.location.reload();
        });
        return false;
    })
};

function reg() {
    $("#register form").submit(function(){
        $(".help-inline").addClass("hide");
        $(".control-group").removeClass("error");
        var args = {};
        $("#register .control-group").each(function(){
            var inp = $(this).find("input");
            args[inp.attr('name')] = inp.val()
            if(!inp.val()) {
                $(this).addClass("error");
                $(this).find(".help-inline").removeClass("hide");
            }
        })
        $.postJSON("/a/register/", "POST", args, function(response) {
            if (response.error){
                return alert(response.error);
            }
            $.cookie("uid", response.uid, {path: '/', expires: 1});
            window.location.reload();
        });
        return false;
    })
};

function logout(e) {
    var args = {};
    $.postJSON("/a/logout/", "POST", args, function(response) {
        if (response.error){
            return alert(response.error);
        }
        $.cookie("uid", null, {path: '/', expires: 1});
        window.location = '/';
    });
    return false;
};

function cpassword() {
    $("#change_pwd form").submit(function(){
        $(".help-inline").addClass("hide");
        $(".control-group").removeClass("error");
        var args = {};
        $("#change_pwd .control-group").each(function(){
            var inp = $(this).find("input");
            args[inp.attr('name')] = inp.val()
            if(!inp.val()) {
                $(this).addClass("error");
                $(this).find(".help-inline").removeClass("hide");
            }
        })
        $.postJSON("/a/cpassword/", "POST", args, function(response) {
            if (response.error){
                return alert(response.error);
            }
            window.location.reload();
        });
        return false;
    })
};

function delconfirm(e) {
    if (!confirm(" 确定删除?")) return false;
};

function like(a, b, e) {
    var f_html = "<from><input type=input style='opacity:1.0;width:90%;'/></from>";
    $.popForm(b, 200, 400, f_html);
};

jQuery.popForm =function(a, width, height, from) {
    $('#popform').remove();
    var a = $(a).position()
    var html = "<div id='popform' style='z-index:105;position:absolute;border:1px solid green;background:green;opacity:0.9;padding:5px;'></div>";
    $(document.body).append(html);
    var l = a.left;
    var p = document.documentElement.clientWidth - l < 400;
    var top = a.top-height/2;
    var left = p ? l - width - 20: l + 40;
    $('#popform').offset({top:top,left:left}).width(width).height(height).append(from);
};

