(function(b) {
    var a = window.yhui || {};
    a.log = function(c) {
        if (typeof(console) != "undefined" && typeof(console.log) == "function") {
            console.log(c)
        }
    };
    a.iMap = (function() {
        var c = {
            width: 500,
            height: 400,
            lat: 40.92,
            lng: 120.46,
            zoom: 8,
            type: "ROADMAP",
            callback: ""
        },
        d = {
            lat: c.lat,
            lng: c.lng,
            latLng: function() {
                return new google.maps.LatLng(c.lat, c.lng)
            } (),
            draggable: false,
            handleDragStart: function() {},
            handleDragEnd: function() {},
            handleDrag: function() {},
            clickable: false,
            handleClick: function() {},
            visible: true
        },
        e = {
            disableDefaultUI: false,
            panControl: true,
            zoomControl: true,
            zoomControlOptions: {
                style: google.maps.ZoomControlStyle.SMALL
            },
            mapTypeControl: true,
            mapTypeControlOptions: {
                style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR
            },
            scaleControl: true,
            streetViewControl: false,
            overviewMapControl: false,
            searchControl: false,
            searchCallback: ""
        },
        f = {
            lat: c.lat,
            lng: c.lng,
            latLng: function() {
                return new google.maps.LatLng(c.lat, c.lng)
            } ()
        },
        g = b.extend(c, e),
        h = [],
        i = [];
        function j(w, u) {
            var v = b.extend(f, u || {});
            w.setCenter(v.latLng)
        }
        function k(u) {
            return !! u && !u.nodeName && u.constructor != String && u.constructor != RegExp && u.constructor != Array && /function/m.test(u + "")
        }
        function l(x, u) {
            var v = b.extend(g, u || {});
            x.css({
                width: v.width,
                height: v.height
            });
            v.mapTypeId = google.maps.MapTypeId[v.type];
            var w = new google.maps.Map(x.get(0), v),
            y = new google.maps.LatLng(v.lat, v.lng);
            w.setCenter(y);
            if (k(v.callback)) {
                v.callback(w)
            }
            if (v.searchControl) {
                p(w, v.searchCallback)
            }
            if (v.markControl) {
                ab(w, v.markCallback)
            }
            if (v.routeControl) {
                ac(w, v.routeCallback)
            }
            return w
        }
        function m(x, v, idx) {
            var w = b.extend(d, v || {}),
            u = new google.maps.Marker({
                position: w.latLng,
                map: x,
                draggable: w.draggable,
                cilckable: w.clickable
            });
            if (w.draggable && w.handleDrag && k(w.handleDrag)) {
                google.maps.event.addListener(u, "drag", w.handleDrag)
            }
            if (w.draggable && w.handleDragStart && k(w.handleDragStart)) {
                google.maps.event.addListener(u, "dragstart", w.handleDragStart)
            }
            if (w.draggable && w.handleDragEnd && k(w.handleDragEnd)) {
                google.maps.event.addListener(u, "dragend", w.handleDragEnd)
            }
            if (w.clickable && w.handleClick && k(w.handleClick)) {
                google.maps.event.addListener(u, "click", w.handleClick)
            }
            if (w.clickable && w.handleRightClick && k(w.handleRightClick)) {
                google.maps.event.addListener(u, "rightclick", w.handleRightClick)
            }
            if (w.clickable && w.handleDBClick && k(w.handleDBClick)) {
                google.maps.event.addListener(u, "dbclick", w.handleDBClick)
            }
            if (idx == null || idx >= u.length) {
                h.push(u);
            } else {
                h.splice(m, 0, u);
            }
            return u
        }
        function n(u) {
            for (var v = 0; v < u.length; v++) {
                u[v].setMap(null)
            }
        }
        function o(w, u, v) {
            switch (u) {
            case "click":
                google.maps.event.addListener(w, "click", v);
                break;
            case "zoom":
                google.maps.event.addListener(w, "zoom_changed", v);
                break;
            case "drag":
                google.maps.event.addListener(w, "drag", v);
                break;
            case "dragstart":
                google.maps.event.addListener(w, "dragstart", v);
                break;
            case "dragend":
                google.maps.event.addListener(w, "dragend", v);
                break;
            default:
            }
        }
        function p(y, z) {
            var x = b('<div id="search-control"></div>'),
            v = b('<div id="search-control-ui"></div>'),
            u = b('<input type="text" name="search-txt" id="search-txt" />'),
            w = b('<input type="button" id="btn-search" value="search" />');
            v.append(u).append(w);
            x.append(v);
            y.controls[google.maps.ControlPosition.TOP_LEFT].push(x.get(0));
            google.maps.event.addDomListener(w.get(0), "click",
            function() {
                var A = u.val();
                q({
                    map: y,
                    address: A,
                    fail: z
                })
            });
            u.bind("keydown",
            function(B) {
                if (B.keyCode == "13") {
                    var A = u.val();
                    q({
                        map: y,
                        address: A
                    })
                }
            });
            u.autocomplete({
                source: function(B, A) {
                    var C = new google.maps.Geocoder();
                    C.geocode({
                        address: B.term
                    },
                    function(E, D) {
                        A(b.map(E,
                        function(F) {
                            return {
                                label: F.formatted_address,
                                value: F.formatted_address,
                                latitude: F.geometry.location.lat(),
                                longitude: F.geometry.location.lng()
                            }
                        }))
                    })
                },
                select: function(C, D) {
                    if (n.length) {
                        b.each(n,
                        function(F, E) {
                            E.setMap(null)
                        })
                    }
                    var B = new google.maps.LatLng(D.item.latitude, D.item.longitude),
                    A = i(y, {
                        latLng: B
                    });
                    j(y, {
                        latLng: B
                    });
                    y.setZoom(15)
                }
            })
        }
        function q(u) {
            var x = {
                ele: "",
                map: "",
                address: "",
                zoom: 15,
                success: "",
                fail: ""
            },
            v = b.extend(x, u || {});
            if (h && h.length) {
                e(h)
            }
            if (i && i.length) {
                n(i)
            }
            var w = new google.maps.Geocoder();
            w.geocode({
                address: v.address
            },
            function(A, z) {
                if (z == google.maps.GeocoderStatus.OK) {
                    v.map.setZoom(v.zoom);
                    if (k(v.success)) {
                        v.success(v.map, A[0])
                    } else {
                        var C = A[0].geometry.location,
                        y = m(v.map, {
                            draggable: false,
                            latLng: C
                        }),
                        B = '<div class="info-window"><div class="info-win-hd">' + A[0].formatted_address + '</div><div class="info-win-bd"><a target="_blank" href="http://ditu.google.cn/maps?hl=zh-CN&ie=UTF8&dirflg=r&f=d&daddr=' + A[0].formatted_address + '">驾车/公交路线</a></div></div>',
                        D = a.iMap.infowindow(v.map, y, {
                            content: B
                        });
                        t(v.map, {
                            latLng: C
                        });
                        D.open(v.map, y)
                    }
                    b(v.ele).data("latLng", A[0].geometry.location)
                } else {
                    if (k(v.fail)) {
                        v.fail(v.map)
                    }
                }
            })
        }
        function r(z, u, v) {
            var y = {
                content: "",
                maxWidth: 200,
                maxHeight: 100,
                autoScroll: true
            },
            w = b.extend(y, v || {}),
            x = new google.maps.InfoWindow({
                content: w.content,
                maxWidth: w.maxWidth,
                maxHeight: w.maxHeight,
                autoScroll: w.autoScroll
            });
            i.push(x);
            google.maps.event.addListener(u, "click",
            function() {
                x.open(z, u)
            });
            return x
        }
        function s(v) {
            var x = {
                latLng: "",
                callback: function() {}
            },
            w = b.extend(x, v || {}),
            u = new google.maps.Geocoder();
            u.geocode({
                latLng: w.latLng
            },
            function(z, y) {
                if (y === google.maps.GeocoderStatus.OK && k(w.callback)) {
                    w.callback(z[0])
                }
            })
        }
        function t(v) {
            var y = {
                center: "beijing",
                size: "400x300",
                zoom: "16",
                maptype: "roadmap"
            },
            x = b.extend(y, v || {}),
            u = "http://maps.google.cn/maps/api/staticmap?center=" + x.center + "&size=" + x.size + "&zoom=" + x.zoom + "&markers=" + x.center + "&maptype=" + x.maptype + "&sensor=false",
            w = b('<img src="' + u + '" alt="google static map" />');
            return w
        }
        function aa(v, u) {
            for (var i = 0; i < u.length; i++) {
                yhui.iMap.createMarker(v, {latLng: u[i], draggable: true, clickable: true});
            }
            yhui.iMap.reloadPolyline(v);
            var w = google.maps.event.addListener(v, 'click', function(event) {
                yhui.iMap.createMarker(v, {latLng: event.latLng, draggable: true, clickable: true,
                    handleClick: function(event) {
                        yhui.iMap.infowindow(v, event.marker, {content: 'event.marker.getPosition().toUrlValue()'});
                    }, handleDragEnd: function(event) {
                        yhui.iMap.reloadPolyline(v);
                    }, handleRightClick: function(event) {
                        yhui.iMap.reloadPolyline(v);
                    }, handleDBClick:function(event) {
                        yhui.iMap.reloadPolyline(v);
                    }
                })
                yhui.iMap.reloadPolyline(v);
            });
            return w;
        }
        var bb;
        function dd(x) {
            if (bb){
                bb.setMap(null);
            }
            var path = [];
            for (var i = 0; i < h.length; i++) {
                var latlng = h[i].getPosition();
                path.push(latlng);
                h[i].setTitle("#" + i + ": " + latlng.toUrlValue());
            }
            bb = new google.maps.Polyline({
                map: x,
                path: path,
                strokeColor: "red",
                strokeOpacity: 0.5,
                strokeWeight: 3,
            });
        }
        function ab(y, z) {
            var x = b('<div id="mark-control"></div>'),
            v = b('<div id="mark-control-ui"></div>'),
            u = b('<img src="/static/img/route_grey.gif" id="search-img" />');
            v.append(u)
            x.append(v);
            y.controls[google.maps.ControlPosition.TOP_RIGHT].push(x.get(0));
            google.maps.event.addDomListener(v.get(0), "click",
            function() {
                alert('click mark');
            });
        }
        function ac(y, z) {
            var x = b('<div id="route-control"></div>'),
            v = b('<div id="route-control-ui"></div>'),
            u = b('<img src="/static/img/route_red.gif" id="search-img" />');
            v.append(u);
            x.append(v);
            y.controls[google.maps.ControlPosition.TOP_RIGHT].push(x.get(0));
            var isopen = false;
            google.maps.event.addDomListener(v.get(0), "click",
                function() {
                    if (isopen) {
                        aa(y, []);
                        v.html('<img src="/static/img/route_red.gif" id="search-img" />');
                        isopen = false;
                    } else {
                        v.html('<img src="/static/img/route_grey.gif" id="search-img" />');
                        google.maps.event.clearListeners(y, 'click');
                        isopen = true;
                    }
                });
        }
        return {
            createMap: function(u, v) {
                return l(u, v)
            },
            setCenter: function(v, u) {
                j(v, u)
            },
            createMarker: function(u, v) {
                return m(u, v)
            },
            removeOverlay: function(u) {
                n(u)
            },
            bind: function(w, u, v) {
                o(w, u, v)
            },
            search: function(u) {
                return q(u)
            },
            infowindow: function(w, u, v) {
                return r(w, u, v)
            },
            addressLookup: function(u) {
                s(u)
            },
            staticMap: function(u) {
                return t(u)
            },
            initPolyline: function(v, u) {
                return aa(v, u)
            },
            reloadPolyline: function(v) {
                return dd(v)
            }
        }
    })();
    window.yhui = a
})(jQuery);






var map;
var markers = [];
var polyline;
var id = "points";

function showPolyline() {
    if (polyline) {
        polyline.setMap(null);
    }
    var path = [];
    for (var i = 0; i < markers.length; i++) {
        var latlng = markers[i].getPosition();
        path.push(latlng);
        markers[i].setTitle("#" + i + ": " + latlng.toUrlValue());
    }
    polyline = new google.maps.Polyline({
            map: map,
            path: path,
            strokeColor: "#0000FF",
            strokeOpacity: 0.5,
            strokeWeight: 8,
        });
}

function clearMarkers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
    showPolyline();
}

function getMarkerIndex(marker) {
    for (var i = 0; i < markers.length; i++) {
        if (marker == markers[i]) {
            return i;
        }
    }
    return -1;
}

function addMarker(latlng, i) {
    var marker = new google.maps.Marker({
            map: map,
            position: latlng,
            draggable: true,
        });
    /*
    google.maps.event.addListener(marker, 'click', function() {
            var infoWindow = new google.maps.InfoWindow({
                    content: marker.getPosition().toUrlValue(),
                });
            infoWindow.open(map, marker);
        });
    */
    google.maps.event.addListener(marker, 'dragend', function(event) {
            showPolyline();
            displayMarkers();
        });
    google.maps.event.addListener(marker, 'rightclick', function(event) {
            removeMarker(marker);
            showPolyline();
            displayMarkers();
        });
    google.maps.event.addListener(marker, 'dblclick', function(event) {
            var i = getMarkerIndex(marker);
            if (i > 0 && i == markers.length - 1) {
                i--;
            }
            if (i < markers.length - 1) {
                var lat0 = markers[i].getPosition().lat();
                var lng0 = markers[i].getPosition().lng();
                var lat1 = markers[i+1].getPosition().lat();
                var lng1 = markers[i+1].getPosition().lng();
                var latlng = new google.maps.LatLng((lat0+lat1)/2, (lng0+lng1)/2);
                addMarker(latlng, i+1);
            }
        });
    if (i == null || i >= markers.length) {
        markers.push(marker);
    } else {
        markers.splice(i, 0, marker);
    }
    showPolyline();
}

function removeMarker(marker) {
    var i = getMarkerIndex(marker);
    marker.setMap(null);
    markers.splice(i, 1);
    showPolyline();
}

function displayMarkers() {
    var txt = document.getElementById(id);
    txt.value = "";
    for (var i = 0; i < markers.length; i++) {
        var latlng = markers[i].getPosition();
        txt.value += latlng.toUrlValue() + ",\n";
    }
}

function setMarkers() {
    var txt = document.getElementById(id);
    var lines = txt.value.split(/\n/);
    clearMarkers();
    for (var i in lines) {
        var ps = lines[i].split(/,/);
        if (ps.length >= 2) {
            var latlng = new google.maps.LatLng(ps[0], ps[1]);
            addMarker(latlng);
        }
    }
    displayMarkers();
    if (markers.length > 0) {
        map.setCenter(markers[0].getPosition());
    }
}

function initialize(canvasName) {
    map = new google.maps.Map(document.getElementById(canvasName), {
            mapTypeId: google.maps.MapTypeId.ROADMAP,
        });
    google.maps.event.addListener(map, 'click', function(event) {
            addMarker(event.latLng);
            displayMarkers();
        });
}