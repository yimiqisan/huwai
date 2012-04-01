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
            var w = b('#note_title').val();
            var x = b("#thumbnails li").length;
            var y = b('#note_text').val();
            for (var i=1; i<x+1; i++) {
                var pnm = "图:"+i,
                reg = new RegExp(pnm,"g"),
                pid = "pic"+i;
                var src = b("#"+pid+" img").attr('src');
                var img = '<img src='+src+'>';
                y = y.replace(reg, img);
            }
            var message = {'note_title': w, 'note_text': y};
            $.postJSON("/a/note/", 'POST', message, function(response) {
                if (response.error){
                    alert(response.error);
                    return ;
                }
            });
        };
        return {
            check: function() {
                return h();
            },
            init:function() {
                return i();
            }
        }
    })();
    window.yhui = a
})(jQuery);
