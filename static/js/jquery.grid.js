(function(b) {
    var a = window.yhui || {};
    a.log = function(c) {
        if (typeof(console) != "undefined" && typeof(console.log) == "function") {
            console.log(c)
        }
    };
    a.iGrid = (function() {
        var c = {
            id: "grid",
            row: 1,
            col: 2,
            max_row: 10,
            delimiter: ",",
            btn: "minus",
            ul: null,
            SingleInput: null,
            values: []
        },
        d = {
            type: "text",
            disabled: false,
            value: "",
            eclass: "span2",
            handleCheck: null
        },
        g = b.extend(c, d);
        function h(x, u) {
            var v = b.extend(g, u || {});
            id = x.attr("id");
            y = b('<ul id="'+id+'ul" class="unstyled"></ul>'),
            g.ul = y;
            z = b('<input id="'+id+'input" name="'+id+'" type="hidden" />');
            g.SingleInput = z;
            if (v.values) {z.val(v.values.join(":"))};
            y.append(i({btn: "plus", disabled: true, value: "", values: v.values}));
            x.append(y).append(z);
        };
        function i(u) {
            var v = b.extend(g, u || {});
            var w = b('<li></li>')
            for (var ii=0; ii<v.col; ii++) {
                if (ii != 0) {w.append(b('<span> : </span>'))};
                v.value = v.values[ii];
                w.append(j(v));
            }
            return w.append(k({btn:v.btn}))
        };
        function j(u) {
            var v = b.extend(g, u || {});
            var w = b('<input class="'+v.eclass+'" type="'+v.type+'">');
            if (v.value) {w.attr("value", v.value)};
            if (v.disabled) {w.attr("disabled", "2")};
            if (v.handleCheck) {w.on("change", v.handleCheck)};
            w.on("blur", function(){
                _o(s());
            })
            return w;
        };
        function k(u) {
            var v = b.extend(g, u || {});
            if (v.btn == 'plus') {
                var y = b('<a class="btn btn-plus"><i class="icon-plus"></i></a>');
                y.click(m);
            } else {
                var y = b('<a class="btn btn-minus"><i class="icon-minus"></i></a>')
                y.click(n)
            }
            return y
        };
        function l() {};
        function m(u) {
            var v = b.extend(g, u || {});
            var li = v.ul.find('li');
            var cnt = li.length;
            var inps = li.find("input");
            for (var ii=0; ii<inps.length; ii++) {
                if (!inps[ii].value) {
                    return false;
                }
            }
            if (cnt >= v.max_row) {alert('最多'+v.max_row+'个，谢谢');return false;}
            g.ul.append(i({btn:"minus", disabled: false, value: "", values: []}));
        };
        function n() {
            b(this).parent().remove();
            _o(s());
        };
        function _o(u) {
            g.SingleInput.val(u);
        };
        function _p(u) {
            var isNew = true;
            g.ul.children('li').each(function(i) {
                if (_q(u) == _q(r(this))) {
                    isNew = false;
                    return false;
                }
            });
            return isNew;
        };
        function _q(u) {
            return $.trim(u.toLowerCase());
        };
        function r(u) {
            return $(u).children('input').value;
        };
        function s() {
            var lis = g.ul.find('input').map(function() {
                if (this.value != "") {return this.value;}
            }).get();
            var cnt = lis.length;
            if (cnt%g.col != 0) {return g.SingleInput.val();}
            var uli = []
            for (var ii=0; ii<cnt/g.col; ii++) {
                uli.push(lis.slice(ii*g.col, (ii+1)*g.col).join(":"))
            }
            inps = uli;
            if (inps[0] === '') {inps = [];}
            return inps.join(g.delimiter);
        };
        return {
            createGrid: function(u, v) {
                return h(u, v);
            }
        }
    })();
    window.yhui = a
})(jQuery);
