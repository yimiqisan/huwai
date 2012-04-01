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
            tagSource:function() {},
            onTagRemoved: function(evt, tag) {},
            onTagClicked: function(evt, tag) {},
            onTagAdded: function(evt, tag) {},
        },
        d = {
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
                tagSource: v.tagSource,
                placeholderText: v.placeholderText,
                onTagRemoved: v.onTagRemoved,
                onTagClicked: v.onTagClicked,
                onTagAdded: v.onTagAdded
            });
            if (v.panelControl) {
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
                    });
                    i();
                })
                x.append(y);
                x.prepend(b('<textarea id="'+v.id+'Panel" class="span10" rows=20 name="'+v.id+'Panel" disabled="true"></textarea>'));
            i();
            }
        };
        function i(u) {
            var v = b.extend(g, u || {});
            var args = {};
            z = $('.tabbable .active a').attr('href').replace('#', '');
            if (z){args.rel=z;}
            $.postJSON("/a/tag/", 'GET', args, function(response) {
                if (response.error){
                    return alert(response.error);
                }
                $("#"+v.id+"Panel").val(response.data);
            });
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
