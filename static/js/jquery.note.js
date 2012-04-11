(function(b) {
    var a = window.yhui || {};
    a.log = function(c) {
        if (typeof(console) != "undefined" && typeof(console.log) == "function") {
            console.log(c)
        }
    };
    a.iNote = (function() {
        var c = {
            id: 'tags',
            eclass: 'span3',
            placeholderText: '输入后按 < Enter > 键',
            removeConfirmation: true,
            tagSource:function() {},
            onTagRemoved: function(evt, tag) {},
            onTagClicked: function(evt, tag) {},
            onTagAdded: function(evt, tag) {},
        },
        d = {
            panelControl: false,
        },
        g = b.extend(c, d);
        function h() {
            if (!b("#note_title").val()) {
                alert('请您填写题目');
                b("#note_title").select();
                return false;
            }
            if (!b("#note_text").val()) {
                alert('请在正文中说点什么吧');
                b("#note_text").select();
                return false;
            }
            return true
        };
        function i() {
            b("#form_note").submit(function(){
                if (!h()) {return false};
                j();
                window.location.reload();
                return false;
            });
            b("#preview_note").click(function(t) {
                alert("loading...");
                return ;
            });
            b("#cancel_note").click(function(t) {
                if (!confirm("离开页面 , 确定 ?")) return ! 1
            });
        };
        function j() {
            var u = b('#note_title').val();
            var v = k();
            var message = {'note_title': u, 'note_text': v};
            $.postJSON("/a/note/", 'POST', message, function(response) {
                if (response.error){
                    alert(response.error);
                    return ;
                }
            });
        };
        function k() {
            var u = b('#note_text').val();
            b("#thumbnails li").each(function(index, object){
                var i = index+1;
                var pic = "图:"+i,
                reg = new RegExp(pic,"g"),
                pid = "pic"+i,
                pos = "pos"+i,
                rdo = b('input[name='+pos+']:checked').val(),
                dtl = b(this).find('textarea').val();
                var src = b("#"+pid+" img").attr('src');
                var img = '<img src='+src+'>';
                if (dtl) {img=img+'<div>'+dtl+'</div>';}
                if (rdo == '-1') {
                    img = '<div class="PICL">'+img+'</div>';
                }else if (rdo == '0') {
                    img = '<div class="PIC">'+img+'</div>';
                }else if (rdo == '1') {
                    img = '<div class="PICR">'+img+'</div>';
                }
                u = u.replace(reg, img);
            });
            return '<div class="p">'+u+'</div>';
        };
        function l(u) {
            var v = b(u).attr("rel");
            var li = b('#pic'+v);
            reg = "\/image\/attach\/(.*)";
            var args = {};
            args.pid = li.find('img').attr('src').match(reg)[1];
            $.postJSON("/a/image/delete/", 'POST', args, function(response) {
                if (response.error){
                    alert(response.error);
                }
                var w = b('#note_text')
                w.val(w.val().replace(eval("/图:"+v+"/g"),""))
                b('#pic'+v).fadeOut()
                return false;
            });
            return false;
        };
        return {
            check: function() {
                return h();
            },
            init:function() {
                return i();
            },
            delPic: function(u) {
                return l(u);
            }
        }
    })();
    window.yhui = a
})(jQuery);
