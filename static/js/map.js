// Placeholder
Do(function() {
    Do.delay(1000, function(){
        var script = document.createElement("script");
        script.type = "text/javascript";
        script.src = "http://maps.google.cn/maps/api/js?sensor=false&callback=loadMap";
        document.body.appendChild(script);
    });
});

// 异步加载 google map
function loadMap(){
    Do.add('imap', {path: 'http://img3.douban.com/js/ui/packed_imap2031263059.js', type: 'js', requires: ['jQueryUI', 'dialog-css', 'dialog']});
    Do('imap', function(){
        var infowindows = [];
        $.fn.iMap = function(){
            var map;
            // 自动搜索
            this.autoSearch = function(){
                var start = new Date(),
                    end = '';
                $(this).bind('keyup', function(){
                    var $this = $(this),
                        $map = $('#event-map'),
                        $city = $('#loc'),
                        city = $city.is('input')? $city.val(): $city.text(),
                        $street = $('#street_address'),
                        street = $.trim($street.val()),
                        address = city + '市' + street;
                    end = new Date();
                    function _successHandle(map, result){
                        var latLng = result.geometry.location,
                            marker = dui.iMap.createMarker(map, {clickable: false, draggable: false, latLng: latLng});
                        dui.iMap.setCenter(map, {latLng: latLng});
                        zoom2center({map: map, marker: marker, infowindow: '', latLng: latLng});
                        $('#location-latLng').val(latLng.lat() + ',' + latLng.lng());
                    }
                    if(end - start > 2000 && address.length > 1){
                        var geocoder = new google.maps.Geocoder();
                         geocoder.geocode({
                            address: address
                        },function(results, status){
                            if (status == google.maps.GeocoderStatus.OK) {
                                var map = dui.iMap.createMap($map, {width: 700, height: 500, panControl: false, mapTypeControl: false, zoomControlOptions: {style: google.maps.ZoomControlStyle.SMALL}});
                                dui.iMap.search({ele: '#event-map', map: map, address: address, success: _successHandle, fail: function(){}});
                            }
                        });
                        start = end;
                    }
                });
            };
            // 显示、隐藏
            this.toggle = function(){
                var $this = $(this),
                    $mapWrap = $('#event-map-wrap'),
                    $city = $('#loc'),
                    city = $city.is('input')? $city.val(): $city.text(),
                    $street = $('#street_address'),
                    street = $.trim($street.val()),
                    address = city + '市' + street;
                function _success(map, result){
                    var latLng = result.geometry.location,
                        marker = dui.iMap.createMarker(map, {draggable: false, latLng: latLng});
                    dui.iMap.setCenter(map, {latLng: latLng});
                    zoom2center({map: map, marker: marker, infowindow: '', latLng: latLng});
                    $('#location-latLng').val(latLng.lat() + ',' + latLng.lng());
                }
                // 搜索无结果时的回调函数
                function _fail(map){
                    var marker = dui.iMap.createMarker(map),
                        $content = $('<div><h3 style="font-size:12px;font-weight:normal;">你输入的地址在地图上找不到</h3><p style="font-size:12px;">请重新输入或<a id="btn-manual-mark" href="#">手动标记</a></p></div>'),
                        infowindow = dui.iMap.infowindow(map, marker, {content: $content.get(0)});
                    infowindow.open(map, marker);
                    marker.setAnimation(google.maps.Animation.BOUNCE);
                    $content.find('#btn-manual-mark').one('click', _manual);
                };
                function _init($checkbox, location){
                    if($checkbox.is(':checked')){
                        var $map = $('<div id="event-map"></div>');
                        // 在地图初始化之前，所需的dom一定要初始化比如show完毕。
                        $mapWrap.empty().append($map).show();
                        map = dui.iMap.createMap($map, {width: 700, height: 500, panControl: false, mapTypeControl: false});
                        if($.trim(location) !== ''){
                            dui.iMap.search({ele: '#event-map', map: map, address: location, success: _success, fail: _fail});
                        }
                    }else{
                        $mapWrap.empty().hide();
                        $('#street_address').unbind();
                    }
                }
                $this.bind('click', function(e){
                    var _city = $city.text(),
                        _street = $.trim($street.val()),
                        _address = _city + _street;
                    _init($this, _address);
                });
                // 页面初始化时
                _init($this, address);
            };
            // 地址提示
            this.suggest = function(ele, map){
                $(this).autocomplete({
                    appendTo: ele,
                    source: function(request, response) {
                        var geocoder = new google.maps.Geocoder(),
                            $city = $('#loc'),
                            city = $city.is('input')? $city.val(): $city.text(),
                            $district = $('#district_id'),
                            district = $district.find(':selected').val() == 0? '': $district.find(':selected').text(),
                            address = $('#manual-mark-map').parents('.dui-dialog').is(':visible')? request.term: city + district + request.term;
                        geocoder.geocode( {'address': address}, function(results, status) {
                            response($.map(results, function(item) {
                                return {
                                    label:  item.formatted_address,
                                    value: item.formatted_address,
                                    latitude: item.geometry.location.lat(),
                                    longitude: item.geometry.location.lng()
                                }
                            }));
                        });
                    },
                    select: function(event, ui) {
                        var location = new google.maps.LatLng(ui.item.latitude, ui.item.longitude),
                            marker = dui.iMap.createMarker(map, {latLng: location});
                        dui.iMap.setCenter(map, {latLng: location});
                        map.setZoom(15);
                    }
                });
            }
            return this;
        };
        // 手动标注地址
        function _manual(e){
            // 搜索
            function _search(map, address){
                function _success(map, result){
                    var latLng = result.geometry.location,
                        marker = dui.iMap.createMarker(map, {draggable: true, latLng: latLng}),
                        content = '<div class="info-window"><div class-"info-win-bd">拖动此图标在地图上标注位置</div></div>',
                        infowindow = dui.iMap.infowindow(map, marker, {content: content}),
                        dragStart,
                        dragEnd;
                    dui.iMap.setCenter(map, {latLng: latLng});
                    setTimeout(function(){
                        infowindow.open(map, marker);
                    }, 0);
                    infowindows.push(infowindow);
                    dui.iMap.bind(map, 'zoom', function() {
                        marker.setMap(null);
                        marker = dui.iMap.createMarker(map, {draggable: true, latLng: latLng}),
                        dui.iMap.setCenter(map, {latLng: latLng});
                        setTimeout(function(){
                            infowindow.open(map, marker);
                        }, 0);
                        dui.iMap.bind(marker, 'dragstart', _dragstart);
                        dui.iMap.bind(marker, 'dragend', _dragend);
                    });
                    function _dragstart(e){
                        dui.iMap.removeOverlay(infowindows);
                        infowindow.setMap(null);
                        google.maps.event.clearListeners(map, 'zoom_changed');
                    }
                    function _dragend(e){
                        var info = '<div class="info-window" style="height:100px;"><div class="info-win-bd"><p>是否将新位置设置为你的默认位置？(可以继续拖动图标标注)</p><a class="btn-save" href="#">保存</a><a class="btn-cancel" href="#">取消</a></div>',
                            infowindow = dui.iMap.infowindow(map, marker, {content: info, maxHeight: 1000}),
                            latLng = e.latLng;
                        dui.iMap.setCenter(map, {latLng: latLng});
                        setTimeout(function(){
                            infowindow.open(map, marker);
                        }, 0);
                        dui.iMap.bind(map, 'zoom', function() {
                            marker.setMap(null);
                            marker = dui.iMap.createMarker(map, {draggable: true, latLng: latLng}),
                            dui.iMap.setCenter(map, {latLng: latLng});
                            setTimeout(function(){
                                infowindow.open(map, marker);
                            }, 0);
                        });
                        // 保存手动标注地址
                        $('.info-window .btn-save').live('click', function(e){
                            e.preventDefault();
                            $('.dui-dialog-close').trigger('click');
                            var $map = $('#event-map'),
                                map = dui.iMap.createMap($map, {zoom:16, width: 700, height: 500, panControl: false, mapTypeControl: false, zoomControlOptions: {style: google.maps.ZoomControlStyle.SMALL}}),
                                marker = dui.iMap.createMarker(map, {latLng: latLng}),
                                $content = $('<div class="info-window"><div class="info-win-hd">' + $('#street_address').val() + '</div><div class="info-win-bd"><a href="#">手动标记</a></div></div>'),
                                infowindow = dui.iMap.infowindow(map, marker, {content: $content.get(0)});
                            dui.iMap.setCenter(map, {latLng: latLng});
                            setTimeout(function(){
                                infowindow.open(map, marker);
                            }, 0);
                            dui.iMap.bind(map, 'zoom', function() {
                                marker.setMap(null);
                                marker = dui.iMap.createMarker(map, {draggable: false, latLng: latLng}),
                                dui.iMap.setCenter(map, {latLng: latLng});
                                setTimeout(function(){
                                    infowindow.open(map, marker);
                                }, 0);
                            });
                            $('#location-latLng').val(latLng.lat() + ',' + latLng.lng());
                            $content.find('a').one('click', function(e){
                                _manual(e);
                                return false;
                            });
                            return false;
                        });
                        // 取消手动标注地址
                        $('.info-window .btn-cancel').live('click', function(e){
                            e.preventDefault();
                            $('.dui-dialog-close').trigger('click');
                            $('#street_address').trigger('blur');
                            return false;
                        });
                    }
                    // 拖拽事件
                    dragStart = dui.iMap.bind(marker, 'dragstart', _dragstart);
                    dragEnd = dui.iMap.bind(marker, 'dragend', _dragend);
                }
                dui.iMap.search({map: map, address: address, success: _success});
            }
            e.preventDefault();
            var $doc = $(document),
                docHeight = $doc.height(),
                $win = $(window),
                winHeight = $win.height(),
                $html = $('html'),
                $city = $('#loc'),
                _city = $city.is('input')? $city.val(): $city.text(),
                $district = $('#district_id'),
                _district = $district.find(':selected').val() == 0? '': $district.find(':selected').text(),
                _address = _city + '市' + _district;;
            // 遮罩
            var top = getPageScroll().top;
            $html.height(winHeight).css({'overflow': 'hidden'}).scrollTop(top);
            $('body').append($('<div class="overlay"></div>'));
            $('div.overlay').css({'width': $doc.width(), 'height': docHeight, 'display': 'block'});
            var content = '<div id="manual-mark-map"><div class="map"></div></div>',
                dlg = dui.Dialog({
                    title: '手动标注地点',
                    width: 600,
                    iframe: true,
                    content: content
                });
            dlg.node.find('.bd').css({padding:0});
            dlg.open();
            // 这里有一个坑
            // 如果地图初始化放在 dlg.open() 之前
            // 地图资源会加载不完全
            var map = dui.iMap.createMap($('#manual-mark-map .map'), {zoom: 16, searchControl: false, width: 600, height: 400, panControl: true, mapTypeControl: true, zoomControl: true, zoomControlOptions: {style: google.maps.ZoomControlStyle.LARGE}});
            dlg.update();
            _search(map, _address);
            // 关闭dialog时，同时关闭遮罩，页面回到之前位置
            dlg.node.find('.dui-dialog-close').bind('click', function(e){
                e.preventDefault();
                $html.height(docHeight).css({'overflow': 'auto'}).scrollTop(top);
                $('.overlay').remove();
                // 这里触发地址栏的失焦事件会导致 autosearch 事件
                // 使得无法保存手动标记地点的座标
                //$('#street_address').trigger('blur');
            });
        };
        // 改变地图缩放级别时，保证地标在地图中心
        function zoom2center(options){
            var defaults = {
                    map: '',
                    marker: '',
                    infowindow: '',
                    latLng: '',
                    callback: function(){}
                },
                opts = $.extend(defaults, options || {});
            dui.iMap.bind(opts.map, 'zoom', function() {
                dui.iMap.setCenter(opts.map, {latLng: opts.latLng});
                if(opts.infowindow){
                    setTimeout(function(){
                        opts.infowindow.open(opts.map, opts.marker);
                    }, 0);
                }
                opts.callback();
            });
        }
        // 地图的自动搜索
        function autosearch(){
            // 选中了显示地图时
            if($('#bits_2').is(':checked')){
                var $this = $(this),
                    $city = $('#loc'),
                    city = $city.is('input')? $city.val(): $city.text(),
                    $street = $('#street_address'),
                    street = $.trim($street.val()),
                    address = city + '市'  + street,
                    $map = $('#event-map'),
                    map = dui.iMap.createMap($map, {width: 700, height: 500, panControl: false, mapTypeControl: false, zoomControlOptions: {style: google.maps.ZoomControlStyle.SMALL}});
                // 搜索成功
                function successHandle(map, result){
                    var latLng = result.geometry.location,
                        marker = dui.iMap.createMarker(map, {clickable: false, draggable: false, latLng: latLng}),
                        $content = $('<div class="info-window"><div class="info-win-hd">' + result.formatted_address + '</div><div class="info-win-bd"><a id="btn-manual-mark" href="#">手动标记</a></div></div>'),
                        infowindow = dui.iMap.infowindow(map, marker, {content: $content.get(0)});
                    dui.iMap.setCenter(map, {latLng: latLng});
                    setTimeout(function(){
                        infowindow.open(map, marker);
                    }, 0);
                    $('#location-latLng').val(latLng.lat() + ',' + latLng.lng());
                    $content.find('#btn-manual-mark').one('click', _manual);
                    zoom2center({map: map, marker: marker, infowindow: infowindow, latLng: latLng, callback: function(){
                        $content.find('#btn-manual-mark').one('click', _manual);
                    }});
                }
                // 搜索无结果时的回调函数
                function _fail(map){
                    var marker = dui.iMap.createMarker(map),
                        $content = $('<div><h3 style="font-size:12px;font-weight:normal;">你输入的地址在地图上找不到</h3><p style="font-size:12px;">请重新输入或<a id="btn-manual-mark" href="#">手动标记</a></p></div>'),
                        infowindow = dui.iMap.infowindow(map, marker, {content: $content.get(0)});
                    infowindow.open(map, marker);
                    marker.setAnimation(google.maps.Animation.BOUNCE);
                    $content.find('#btn-manual-mark').one('click', _manual);
                };
                dui.iMap.search({ele: '#event-map', map: map, address: address, success: successHandle, fail: _fail});
            }
        }
        var _t_map;
        // 事件绑定
        $('#bits_2').iMap().toggle();
        $('.page-address').delegate('#loc', 'change', function() {
            try {
                clearTimeout(_t_map);
            } catch(e) {}
            _t_map = setTimeout(autosearch, 400);
        });
        $('.page-address').delegate('#street_address', 'blur', autosearch);
        $('#street_address').iMap().autoSearch();
    });
}