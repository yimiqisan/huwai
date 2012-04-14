(function(b) {
    var a = window.yhui || {};
    a.log = function(c) {
        if (typeof(console) != "undefined" && typeof(console.log) == "function") {
            console.log(c)
        }
    };
    a.iPage = (function() {
        var c = {
            id: 'pagination',
            mode: 'LIST',
            prefix_url: '',
            start_page: 1,
            has_pre: false,
            pre_page: 1,
            page: 1,
            total_page: 1,
            page_list: [],
            has_eps: false,
            has_next: false,
            next_page: 1,
            end_page: 1,
            toPage: null,
        },
        d = {
        },
        g = b.extend(c, d);
        function h(x, u) {
            var v = b.extend(g, u || {});
            b('#'+v.id).empty();
            var y = b('<ul></ul>');
            y.append(b('<li><a href="'+v.start_page+'">&lt;&lt;</a></li>'));
            if (v.has_pre) {y.append(b('<li><a href="'+v.pre_page+'">&lt;</a></li>'));}
            for (var i=0; i<v.page_list.length; i++) {
                if (v.page_list[i] == v.page) {
                    y.append(b('<li class="active"><a href="'+v.page_list[i]+'">'+v.page_list[i]+'</a></li>'));
                } else {
                    y.append(b('<li><a href="'+v.page_list[i]+'">'+v.page_list[i]+'</a></li>'));
                }
            }
            if (v.has_eps) {y.append(b('<li><a>...</a></li>'));}
            if (v.has_next) {y.append(b('<li><a href="'+v.next_page+'">&gt;</a></li>'));}
            y.append(b('<li><a href="'+v.end_page+'">&gt;&gt;</a></li>'));
            x.append(y);
            b('#'+v.id).find('a').click(function(){
                b(this).addClass('active');
                if (b(this).attr('href')) {
                    v.toPage({page:b(this).attr('href')});
                }
                return false;
            })
        };
        return {
            create:function(u, v) {
                return h(u, v);
            }
        }
    })();
    window.yhui = a
})(jQuery);
