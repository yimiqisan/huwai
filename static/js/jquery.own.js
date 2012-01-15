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
