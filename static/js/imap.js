(function(b) {
	var a = window.dui || {};
	a.log = function(c) {
		if (typeof(console) != "undefined" && typeof(console.log) == "function") {
			console.log(c)
		}
	};
	a.iMap = (function() {
		var k = {
			width: 500,
			height: 400,
			lat: 40.92,
			lng: 120.46,
			zoom: 8,
			type: "ROADMAP",
			callback: ""
		},
		c = {
			lat: k.lat,
			lng: k.lng,
			latLng: function() {
				return new google.maps.LatLng(k.lat, k.lng)
			} (),
			draggable: false,
			handleDragStart: function() {},
			handleDragEnd: function() {},
			handleDrag: function() {},
			clickable: false,
			handleClick: function() {},
			visible: true
		},
		f = {
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
		p = {
			lat: k.lat,
			lng: k.lng,
			latLng: function() {
				return new google.maps.LatLng(k.lat, k.lng)
			} ()
		},
		j = b.extend(k, f),
		n = [],
		l = [];
		function t(w, u) {
			var v = b.extend(p, u || {});
			w.setCenter(v.latLng)
		}
		function r(u) {
			return !! u && !u.nodeName && u.constructor != String && u.constructor != RegExp && u.constructor != Array && /function/i.test(u + "")
		}
		function d(x, u) {
			var v = b.extend(j, u || {});
			x.css({
				width: v.width,
				height: v.height
			});
			v.mapTypeId = google.maps.MapTypeId[v.type];
			var w = new google.maps.Map(x.get(0), v),
			y = new google.maps.LatLng(v.lat, v.lng);
			w.setCenter(y);
			if (r(v.callback)) {
				v.callback(w)
			}
			if (v.searchControl) {
				s(w, v.searchCallback)
			}
			return w
		}
		function i(x, v, idx) {
			var w = b.extend(c, v || {}),
			u = new google.maps.Marker({
				position: w.latLng,
				map: x,
				draggable: w.draggable,
				cilckable: w.clickable
			});
			if (w.draggable && w.handleDrag && r(w.handleDrag)) {
				google.maps.event.addListener(u, "drag", w.handleDrag)
			}
			if (w.draggable && w.handleDragStart && r(w.handleDragStart)) {
				google.maps.event.addListener(u, "dragstart", w.handleDragStart)
			}
			if (w.draggable && w.handleDragEnd && r(w.handleDragEnd)) {
				google.maps.event.addListener(u, "dragend", w.handleDragEnd)
			}
			if (w.clickable && w.handleClick && r(w.handleClick)) {
				google.maps.event.addListener(u, "click", w.handleClick)
			}
			if (w.clickable && w.handleClick && r(w.handleRightClick)) {
				google.maps.event.addListener(u, "rightclick", w.handleRightClick)
			}
			if (w.clickable && w.handleClick && r(w.handleDBClick)) {
				google.maps.event.addListener(u, "dbclick", w.handleDBClick)
			}
            if (idx == null || idx >= u.length) {
                n.push(u);
            } else {
                n.splice(i, 0, u);
            }
            dd(x);
            return u
        }
		function e(u) {
			for (var v = 0; v < u.length; v++) {
				u[v].setMap(null)
			}
		}
		function m(w, u, v) {
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
		function s(y, z) {
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
				o({
					map: y,
					address: A,
					fail: z
				})
			});
			u.bind("keydown",
			function(B) {
				if (B.keyCode == "13") {
					var A = u.val();
					o({
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
					t(y, {
						latLng: B
					});
					y.setZoom(15)
				}
			})
		}
		function o(u) {
			var x = {
				ele: "",
				map: "",
				address: "",
				zoom: 15,
				success: "",
				fail: ""
			},
			v = b.extend(x, u || {});
			if (n && n.length) {
				e(n)
			}
			if (l && l.length) {
				e(l)
			}
			var w = new google.maps.Geocoder();
			w.geocode({
				address: v.address
			},
			function(A, z) {
				if (z == google.maps.GeocoderStatus.OK) {
					v.map.setZoom(v.zoom);
					if (r(v.success)) {
						v.success(v.map, A[0])
					} else {
						var C = A[0].geometry.location,
						y = i(v.map, {
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
					if (r(v.fail)) {
						v.fail(v.map)
					}
				}
			})
		}
		function h(z, u, v) {
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
			l.push(x);
			google.maps.event.addListener(u, "click",
			function() {
				x.open(z, u)
			});
			return x
		}
		function q(v) {
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
				if (y === google.maps.GeocoderStatus.OK && r(w.callback)) {
					w.callback(z[0])
				}
			})
		}
		function g(v) {
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
            var y = {
                clickable: false,
                geodesic: true,
                map: v,
                path: u
            },
            x = b.extend(y, v || {});
            var w = new google.maps.Polyline(x);
            return w.setMap(v);
        }
        var bb;
        function dd(x) {
            if (bb){
                bb.setMap(null);
            }
            var path = [];
            for (var i = 0; i < n.length; i++) {
                var latlng = n[i].getPosition();
                path.push(latlng);
                n[i].setTitle("#" + i + ": " + latlng.toUrlValue());
            }
            bb = new google.maps.Polyline({
                map: x,
                path: path,
                strokeColor: "red",
                strokeOpacity: 0.5,
                strokeWeight: 3,
            });
        }
        return {
			createMap: function(u, v) {
				return d(u, v)
			},
			setCenter: function(v, u) {
				t(v, u)
			},
			createMarker: function(u, v) {
				return i(u, v)
			},
			removeOverlay: function(u) {
				e(u)
			},
			bind: function(w, u, v) {
				m(w, u, v)
			},
			search: function(u) {
				return o(u)
			},
			infowindow: function(w, u, v) {
				return h(w, u, v)
			},
			addressLookup: function(u) {
				q(u)
			},
			staticMap: function(u) {
				return g(u)
			},
			polyline: function(v, u) {
			    return aa(v, u)
			},
			showPolyline: function(v) {
			    return dd(v)
			}
		}
	})();
	window.dui = a
})(jQuery);
