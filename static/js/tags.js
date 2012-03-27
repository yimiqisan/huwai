(function(b) {
    var a = window.yhui || {};
    a.log = function(c) {
        if (typeof(console) != "undefined" && typeof(console.log) == "function") {
            console.log(c)
        }
    };
    a.iTag = (function() {
        var c;
        function d(id) {
            var eventTags = $('#'+id);
            eventTags.tagit({
//                availableTags: ['登山', '徒步', '骑行', '聚会', '滑雪', '体育运动', '摄影', '攀岩', '探险', '滑翔伞', '垂钓', '漂流', '自驾', '环保公益'],
                singleField: true,
                singleFieldNode: $('#'+id+'Single'),
                removeConfirmation: true,
                tagSource: e,
                placeholderText: '输入后按 < Enter > 键',
                onTagRemoved: function(evt, tag) {},
                onTagClicked: function(evt, tag) {},
                onTagAdded: function(evt, tag) {},
            });
            $("#tag-submit").click(function(){
                var u = $('#'+id+'Single').val();
                if (!u) {return false;}
                c = $('.tabbable .active a').attr('href').replace('#', '');
                args = {'content': u, 'rel': c};
                $.postJSON("/a/tag/", 'POST', args, function(response) {
                    if (response.error){
                        return alert(response.error);
                    }
                    eventTags.tagit("removeAll");
                    f();
                });
            })
            f();
        };
        function e(search, showChoices) {
            var that = this;
            var args = {'search': search.term};
            if (c){args.rel=c;}
            $.postJSON("/a/tag/", 'GET', args, function(response) {
                if (response.error){
                    return alert(response.error);
                }
                showChoices(that._subtractArray(response.data, that.assignedTags()));
            });
        };
        function f() {
            var args = {};
            c = $('.tabbable .active a').attr('href').replace('#', '');
            if (c){args.rel=c;}
            $.postJSON("/a/tag/", 'GET', args, function(response) {
                if (response.error){
                    return alert(response.error);
                }
                $("#eventTagsPanel").val(response.data);
            });
        };
        return {
            init: function(u) {
                return d(u);
            },
            source: function(u, v) {
                e(u, v);
            },
            load: function() {
                f();
            }
        }
    })();
    window.yhui = a
})(jQuery);
