(function() {
	var x = window.dui || {},
	e = "dui-dialog",
	u = [],
	r = null,
	f = ($.browser.msie && $.browser.version === "6.0") ? true: false,
	d = {},
	q = {},
	b = "dui-dialog",
	k = "dui-dialog-close",
	a = "dui-dialog-shd",
	p = "dui-dialog-content",
	l = "dui-dialog-iframe",
	o = "确定",
	c = "取消",
	t = "提示",
	m = "下载中，请稍候...",
	i = '<div id="{ID}" class="' + b + ' {CLS}" style="{CSS_ISHIDE}">				<span class="' + a + '"></span>				<div class="' + p + '">					{TITLE}					<div class="bd">{BODY}</div>                    {BN_CLOSE}				</div>			</div>',
	g = '<a href="#" class="' + k + '">X</a>',
	j = '<div class="hd"><h3>{TITLE}</h3></div>',
	v = '<iframe class="' + l + '"></iframe>',
	n = {
		confirm: {
			text: o,
			method: function(z) {
				z.close()
			}
		},
		cancel: {
			text: c,
			method: function(z) {
				z.close()
			}
		}
	},
	y = {
		url: "",
		nodeId: "",
		cls: "",
		content: "",
		title: t,
		width: 0,
		height: 0,
		visible: false,
		iframe: false,
		maxWidth: 960,
		autoupdate: false,
		cache: true,
		buttons: [],
		callback: null,
		dataType: "text",
		isStick: false,
		isHideClose: false,
		isHideTitle: false
	},
	h = function(C, B) {
		var z = {},
		A;
		for (A in B) {
			if (B.hasOwnProperty(A)) {
				z[A] = C[A] || B[A]
			}
		}
		return z
	},
	w = function(E) {
		var B = E.elements,
		A = 0,
		C,
		D = [],
		z = {
			"select-one": function(F) {
				return encodeURIComponent(F.name) + "=" + encodeURIComponent(F.options[F.selectedIndex].value)
			},
			"select-multiple": function(I) {
				var H = 0,
				G,
				F = [];
				for (; G = I.options[H++];) {
					if (G.selected) {
						F.push(encodeURIComponent(I.name) + "=" + encodeURIComponent(G.value))
					}
				}
				return F.join("&")
			},
			radio: function(F) {
				if (F.checked) {
					return encodeURIComponent(F.name) + "=" + encodeURIComponent(F.value)
				}
			},
			checkbox: function(F) {
				if (F.checked) {
					return encodeURIComponent(F.name) + "=" + encodeURIComponent(F.value)
				}
			}
		};
		for (; C = B[A++];) {
			if (z[C.type]) {
				D.push(z[C.type](C))
			} else {
				D.push(encodeURIComponent(C.name) + "=" + encodeURIComponent(C.value))
			}
		}
		return D.join("&").replace(/\&{2,}/g, "&")
	},
	s = function(z) {
		var A = z || {};
		this.config = h(A, y);
		this.init()
	};
	s.prototype = {
		init: function() {
			if (!this.config) {
				return
			}
			this.render();
			this.bind();
			return this
		},
		render: function(B) {
			var z = this.config,
			C = z.nodeId || e + u.length;
			u.push(C);
			var A = typeof z.content === "object" ? $(z.content).html() : z.content;
			$("body").append(i.replace("{ID}", C).replace("{CSS_ISHIDE}", z.visible ? "": "visibility:hidden;top:-999em;left:-999em;").replace("{CLS}", z.cls).replace("{TITLE}", j.replace("{TITLE}", z.title)).replace("{BN_CLOSE}", g).replace("{BODY}", A || B || ""));
			this.nodeId = C;
			this.node = $("#" + C);
			this.title = $(".hd", this.node);
			this.body = $(".bd", this.node);
			this.btnClose = $("." + k, this.node);
			this.shadow = $("." + a, this.node);
			this.iframe = $("." + l, this.node);
			this.set(z);
			return this
		},
		bind: function() {
			var z = this;
			$(window).bind({
				resize: function() {
					if (f) {
						return
					}
					z.updatePosition()
				},
				scroll: function() {
					if (!f) {
						return
					}
					z.updatePosition()
				}
			});
			this.btnClose.click(function(A) {
				z.close();
				A.preventDefault()
			});
			$("body").keypress(function(A) {
				if (A.keyCode === 27) {
					z.close()
				}
			});
			return this
		},
		updateSize: function() {
			var A = this.node.width(),
			B,
			C = $(window).height(),
			z = this.config;
			$(".bd", this.node).css({
				height: "auto",
				"overflow-x": "visible",
				"overflow-y": "visible"
			});
			B = this.node.height();
			if (A > z.maxWidth) {
				A = z.maxWidth;
				this.node.css("width", A + "px")
			}
			if (B > C) {
				$(".bd", this.node).css({
					height: (C - 150) + "px",
					"overflow-x": "hidden",
					"overflow-y": "auto"
				})
			}
			B = this.node.height();
			this.shadow.width(A).height(B);
			this.iframe.width(A + 16).height(B + 16);
			return this
		},
		updatePosition: function() {
			if (this.config.isStick) {
				return
			}
			var z = this.node.width(),
			B = this.node.height(),
			C = $(window),
			A = f ? C.scrollTop() : 0;
			this.node.css({
				left: Math.floor(C.width() / 2 - z / 2 - 8) + "px",
				top: Math.floor(C.height() / 2 - B / 2 - 8) + A + "px"
			});
			return this
		},
		set: function(E) {
			var G,
			J,
			A,
			B,
			z = this.nodeId,
			H = this.nodeId || H,
			C = [],
			D = this,
			I = function(K) {
				C.push(0);
				return z + "-" + K + "-" + C.length
			};
			if (!E) {
				return this
			}
			if (E.width) {
				this.node.css("width", E.width + "px");
				this.config.width = E.width
			}
			if (E.height) {
				this.node.css("height", E.height + "px");
				this.config.height = E.height
			}
			if ($.isArray(E.buttons) && E.buttons[0]) {
				B = $(".ft", this.node);
				A = [];
				$(E.buttons).each(function() {
					var L = arguments[1],
					K = I("bn");
					if (typeof L === "string") {
						L = n[L]
					}
					if (!L.text) {
						return
					}
					if (L.href) {
						A.push('<a class="' + (L.cls || "") + '" id="' + K + '" href="' + L.href + '">' + L.text + "</a> ")
					} else {
						A.push('<span class="bn-flat ' + (L.cls || "") + '"><input type="button" id="' + K + '" class="' + H + '-bn" value="' + L.text + '" /></span> ')
					}
					q[K] = L.method
				});
				if (!B[0]) {
					B = this.body.parent().append('<div class="ft">' + A.join("") + "</div>")
				} else {
					B.html(A.join(""))
				}
				this.footer = $(".ft", this.node);
				$(".ft input, .ft a", this.node).click(function(M) {
					var L = this.id && q[this.id];
					if (L) {
						var K = L.call(this, D)
					}
					if (K) {
						M.preventDefault();
						if (typeof K == "string") {
							alert(K)
						}
					}
				})
			} else {
				this.footer = $(".ft", this.node);
				this.footer.html("")
			}
			if (typeof E.isHideClose !== "undefined") {
				if (E.isHideClose) {
					this.btnClose.hide()
				} else {
					this.btnClose.show()
				}
				this.config.isHideClose = E.isHideClose
			}
			if (typeof E.isHideTitle !== "undefined") {
				if (E.isHideTitle) {
					this.title.hide()
				} else {
					this.title.show()
				}
				this.config.isHideTitle = E.isHideTitle
			}
			if (E.title) {
				this.setTitle(E.title);
				this.config.title = E.title
			}
			if (typeof E.iframe !== "undefined") {
				if (!E.iframe) {
					this.iframe.hide()
				} else {
					if (!this.iframe[0]) {
						this.node.prepend(v);
						this.iframe = $("." + l, this.node)
					} else {
						this.iframe.show()
					}
				}
				this.config.iframe = E.iframe
			}
			if (E.content) {
				this.body.html(typeof E.content === "object" ? $(E.content).html() : E.content);
				this.config.content = E.content
			}
			if (E.url) {
				if (E.cache && d[E.url]) {
					if (E.dataType === "text" || !E.dataType) {
						this.setContent(d[E.url])
					}
					if (E.callback) {
						E.callback(d[E.url], this)
					}
				} else {
					if (E.dataType === "json") {
						this.setContent(m);
						if (this.footer) {
							this.footer.hide()
						}
						$.getJSON(E.url,
						function(K) {
							D.footer.show();
							d[E.url] = K;
							if (E.callback) {
								E.callback(K, D)
							}
						})
					} else {
						this.setContent(m);
						if (this.footer) {
							this.footer.hide()
						}
						$.ajax({
							url: E.url,
							dataType: E.dataType,
							success: function(K) {
								d[E.url] = K;
								if (D.footer) {
									D.footer.show()
								}
								D.setContent(K);
								if (E.callback) {
									E.callback(K, D)
								}
							}
						})
					}
				}
			}
			var F = E.position;
			if (F) {
				this.node.css({
					left: F[0] + "px",
					top: F[1] + "px"
				})
			}
			if (typeof E.autoupdate === "boolean") {
				this.config.autoupdate = E.autoupdate
			}
			if (typeof E.isStick === "boolean") {
				if (E.isStick) {
					this.node[0].style.position = "absolute"
				} else {
					this.node[0].style.position = ""
				}
				this.config.isStick = E.isStick
			}
			return this.update()
		},
		update: function() {
			this.updateSize();
			this.updatePosition();
			return this
		},
		setContent: function(z) {
			this.body.html(z);
			return this.update()
		},
		setTitle: function(z) {
			$("h3", this.title).html(z);
			return this
		},
		submit: function(B) {
			var z = this,
			A = $("form", this.node);
			A.submit(function(F) {
				F.preventDefault();
				var C = this.getAttribute("action", 2),
				D = this.getAttribute("method") || "get",
				E = w(this);
				$[D.toLowerCase()](C, E,
				function(G) {
					if (B) {
						B(G)
					}
				},
				"json")
			});
			A.submit()
		},
		open: function() {
			this.node.appendTo("body").css("visibility", "visible").show();
			var z = this,
			A = z.body[0];
			z.contentHeight = A.offsetHeight;
			this.watcher = !this.config.autoupdate ? 0: setInterval(function() {
				if (A.offsetHeight === z.contentHeight) {
					return
				}
				z.update();
				z.contentHeight = A.offsetHeight
			},
			100);
			return this
		},
		close: function() {
			this.node.hide();
			this.node.trigger("dialog:close", this);
			clearInterval(this.watcher);
			return this
		}
	};
	x.Dialog = function(z, A) {
		if (!A && r) {
			return z ? r.set(z) : r
		}
		if (!r && !A) {
			r = new s(z);
			return r
		}
		return new s(z)
	};
	window.dui = x
})();