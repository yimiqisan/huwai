(function(b) {
    var a = window.yhui || {};
    a.log = function(c) {
        if (typeof(console) != "undefined" && typeof(console.log) == "function") {
            console.log(c)
        }
    };
    a.iAlert = (function() {
        var c = {
            id: 'alert'
        },
        d = {
        },
        g = b.extend(c, d);
        function h(x) {
            var args = {};
            var e = $('#alert');
            $.postJSON("/a/alert/", "GET", args, function(response) {
                if (response.error){
                    return alert(response.error);
                }
                ms = response.messages;
                b.each(ms, function(){
                    var u = b('<div class="alert fade in"></div>');
                    if (this.nature == 'error') {
                        u.addClass('alert-error');
                    } else if (this.nature == 'success') {
                        u.addClass('alert-success');
                    } else if (this.nature == 'confirm') {
                        u.addClass('alert-info');
                    } else if (this.nature == 'alert') {
                        
                    } else {
                        u.addClass('alert-default');
                    }
                    u.append(b('<a class="close" data-dismiss="alert">×</a>'));
                    u.append(b('<p>'+this.suffix+'<a id=r-'+ this.id +' href="#" onclick="yhui.iAlert.click(this);return false;" subject='+this.subject+'>&nbsp;&nbsp;点击查看</a></p>'));
                    x.append(u);
                })
            });
        };
        function i(u) {
             var args = {};
             var subject = $(u).attr('subject');
             args['subject'] = subject
             $.postJSON("/a/alert/", 'POST', args, function(response) {
                 if (response.error){
                     disabled.enable();
                     return alert(response.error);
                 }
                 $(u).css('display', 'none');
                 window.location.href = '/alert/'+subject;
             });
        };
        return {
            list: function(x) {
                return h(x);
            },
            click: function(u) {
                return i(u);
            }
        }
    })();
    window.yhui = a
})(jQuery);
