(function(b) {
    var a = window.yhui || {};
    a.log = function(c) {
        if (typeof(console) != "undefined" && typeof(console.log) == "function") {
            console.log(c)
        }
    };
    a.iTag = (function() {
        var c = {
            id: 'tags',
            eclass: 'span3',
            placeholderText: '输入后按 < Enter > 键',
            removeConfirmation: true,
            initTags: true, 
            addedAble:true,         //for add
            removeAble:false,       //for remove
            editAble:false,         //edit name or owner
            pageAble:false,         //for page
            numberOpt: 0,           //to be elected 
            relations:[],          //query by this rel
            tagSource:function() {},
            onTagRemoved: function(evt, tag) {},
            onTagClicked: function(evt, tag) {},
            onTagAdded: function(evt, tag) {},
        },
        d = {
            page: 1,
            pglen: 10,
            limit: 50,
            panelControl: false,
        },
        g = b.extend(c, d);
        function h(x, u) {
            var v = b.extend(g, u || {});
            x.append(b('<input id="'+v.id+'Single" name="'+v.id+'" type="hidden"/>'));
            x.append(b('<ul id="'+v.id+'" class="pull-left '+v.eclass+'"></ul>'));
            var w = $('#'+v.id);
            w.tagit({
                singleField: true,
                singleFieldNode: b('#'+v.id+'Single'),
                removeConfirmation: v.removeConfirmation,
                editAble: v.editAble,
                tagSource: v.tagSource,
                placeholderText: v.placeholderText,
                onTagRemoved: v.onTagRemoved,
                onTagClicked: v.onTagClicked,
                onTagAdded: v.onTagAdded
            });
            if (v.addedAble) {
                alert(v.id);
                y = b('<a id="'+v.id+'Submit" class="btn btn-primary pull-right">加上去</a>');
                y.click(function(){
                    var za = $('#'+v.id+'Single').val();
                    if (!za) {return false;}
                    var z = $('.tabbable .active a').attr('href').replace('#', '');
                    args = {'content': za, 'rel': z};
                    $.postJSON("/a/tag/", 'POST', args, function(response) {
                        if (response.error){
                            return alert(response.error);
                        }
                        w.tagit("removeAll");
                        alert("添加成功");
                    });
                    i();
                })
                x.append(y);
            }
            if (v.initTags) {i();}
        };
        function i(u) {
            var v = b.extend(g, u || {});
            var args = {page:v.page, pglen:v.pglen, limit:v.limit};
            if (v.relations){args.rel=v.relations;}
            $.postJSON("/a/tag/", 'GET', args, function(response) {
                if (response.error){
                    return alert(response.error);
                }
                $("#"+v.id).tagit('removeAll');
                for (var i=0; i<response.data.length; i++) {
                    $("#"+v.id).tagit('createTag', response.data[i]['content'], '', response.data[i]['id']);
                }
                if (v.pageAble) {
                    yhui.iPage.create($('#tpage'), {
                        id: 'tpage',
                        start_page: response.pagination.start_page,
                        has_pre: response.pagination.has_pre,
                        pre_page: response.pagination.pre_page,
                        page: response.pagination.page,
                        total_page: response.pagination.total_page,
                        page_list: response.pagination.page_list,
                        has_eps: response.pagination.has_eps,
                        has_next: response.pagination.has_next,
                        next_page: response.pagination.next_page,
                        end_page: response.pagination.end_page,
                        toPage: j,
                    });
                }
            });
        };
        function j(u) {
            i(u);
        };
        return {
            create: function(x, u) {
                return h(x, u);
            },
            tab: function(u) {
                i(u);
            }
        }
    })();
    window.yhui = a
})(jQuery);
