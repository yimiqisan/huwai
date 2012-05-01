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
        function i(u) {
            if (u) {m(u);}
            b("#form_note").submit(function(){
                if (!h()) {return false};
                j(u);
                window.location.href = '/note/'+u;
                return false;
            });
            b("#preview_note").click(function(t) {
                if (!h()) {return false};
                var u = b('#note_title').val(),
                v = k(),
                w = b('input[name=noteTags]').val();
                var message = {'note_title': u, 'note_text': v, 'note_tag': w};
                return ;
            });
            b("#cancel_note").click(function(t) {
                if (!confirm("离开页面 , 确定 ?")) return ! 1
            });
        };
        function j(x) {
            var u = b('#note_title').val(),
            v = k(),
            w = b('input[name=noteTags]').val();
            var message = {'note_title': u, 'note_text': v, 'note_tag': w};
            if (x) {message.nid=x;}
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
            return u;
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
        function m(u) {
            var args ={'nid': u};
            $.postJSON("/a/note/?r="+Math.random(), 'GET', args, function(response) {
                if (response.error){
                    alert(response.error);
                    return ;
                }
                b('#note_title').val(response.info.title);
                var reg = new RegExp('<div class="([A-Z]{3,4})"><img src=/image/attach/(.{32})><div>(.*)</div></div>',"g");
                var vc = response.info.content;
                for (var i=0; i<response.info.tags.length; i++) {
                    $("#noteTags").tagit('createTag', response.info.tags[i][1], '', response.info.tags[i][0]);
                }
                do {
                    var result = reg.exec(response.info.content);
                    if (!result) {break;}
                    r = n(result[1], result[2], result[3]);
                    var regc = new RegExp(result[0],"g");
                    vc = vc.replace(regc, r)
                } while (result)
                b('#note_text').val(vc);
                return false;
            });
        };
        function n(u, v, w) {
            var pic_num = $("#thumbnails li").length+1;
            var pic_name = " 图:"+pic_num+" ";
            z = b('<li id="pic'+pic_num+'" class="span3 bg-white"><div class="thumbnail" style="min-height:100px;"><div style="float:left; clear:right;margin-right:10px;"><img src="/image/attach/'+v+'" style="width:80px;height:80px;margin-bottom:5px;" width=100 height=100 /></div><div class="span1" style="margin:10px 10px;display:block;width:100px;"><a rel="'+pic_num+'" href="" onclick="yhui.iNote.delPic(this);return false;">删除</a><p class="pull-right">'+pic_name+'</p></div><br/><br/><br/><label class="radio inline" style="margin-left:5px;"><input type="radio" name="pos'+pic_num+'" value="-1">左</label><label class="radio inline" style="margin-left:5px;"><input type="radio" name="pos'+pic_num+'" value="0" checked>中</label><label class="radio inline" style="margin-left:5px;"><input type="radio" name="pos'+pic_num+'" value="1">右</label><textarea style="width:200px;">'+w+'</textarea></div></li>');
            b('#thumbnails').append(z);
            if (u == 'PICL') {
                z.find('.radio input[value=-1]').attr('checked', true);
            }else if (u == 'PICR') {
                z.find('.radio input[value=1]').attr('checked', true);
            }
            return pic_name;
        };
        return {
            check: function() {
                return h();
            },
            init:function(u) {
                return i(u);
            },
            insertPic: function(u, v, w) {
                return n(u, v, w);
            },
            delPic: function(u) {
                return l(u);
            }
        }
    })();
    window.yhui = a
})(jQuery);
