!function( $ ){

    "use strict"

    /* REPLY CLASS DEFINITION */
    
    var Reply = function ( element, options ) {
        this.$element = $(element)
        this.options = $.extend({}, $.fn.collapse.defaults, options)
        if (this.options["parent"]) {
            this.$parent = $(this.options["parent"])
        }
//        this.options.toggle && this.toggle()
        
//        this.$element = $(content).delegate('[data-dismiss="reply"]', 'click.dismiss.reply', $.proxy(this.hide, this))
    }

    Reply.prototype = {
        constructor: Reply,
        
        toggle: function () {
            return this[!this.isShown ? 'show' : 'hide']()
        },
        
        transition: function ( method, startEvent, completeEvent ) {
            var that = this,
            complete = function () {
                //if (startEvent == 'show') that.reset()
                that.$element.trigger(completeEvent)
            }
            this.$element.trigger(startEvent)[method]('in')
            complete()
//            $.support.transition && this.$element.hasClass('reply') ? this.$element.one($.support.transition.end, complete) : complete()
        },
        
        show: function () {
            this.transition('addClass', 'show', 'shown')
        },
        hide: function ( e ) {
            this.transition('addClass', 'hide', 'hidden')
        },
        list: function ( e ) {
            
        },
        extend: function () {
            this.transition('addClass', 'extend', 'extendn');
        },
        submit: function () {
            var id = $(this).attr('id');
            Reply.prototype.insert(id.replace('sub-', ''));
        },
        insert: function (id) {
            var tarea = $('#tarea-'+id).val()
            if (tarea == ""){return false;}
            var args = {'to': id, 'content': tarea};
            $.postJSON("/a/nreply", "POST", args, function(response) {
                if (response.error){
                    disabled.enable();
                    return alert(response.error);
                }
                var node = $(response.html);
                node.hide();
                $(node).insertAfter($("#ins-"+id));
                node.slideDown(300);
                $('#tarea-'+id).val("").select();
//                disabled.enable();
            });
        },
        at: function ( e ) {
            
        },
        remove: function () {
            this.transition('addClass', 'remove', 'removen');
        }
    }
    /* REPLY PRIVATE METHODS */
    /* REPLY PLUGIN DEFINITION */
    $.fn.reply = function ( option ) {
        return this.each(function () {
            var $this = $(this), data = $this.data('reply'), options = $.extend({}, $.fn.reply.defaults, $this.data(), typeof option == 'object' && option)
            if (!data) $this.data('reply', (data = new Reply(this, options)))
            if (typeof option == 'string') data[option]()
            else if (options.show) data.extend()
        })
    }

    $.fn.reply.defaults = {
        url: '/a/reply/',
        template: '<div class="reply-item"><a class="photo30" href="#"><img width="30" height="30" alt="" src="/image/avatar/c18db1940a5e4c00a4b29f7206bc953f_50"></a><div class="content"><span class="pull-right" style="width:15px"><a class="close" onclick="return false;" href="#" alt="删除">&times;</a></span><span class="author me"><a title="" href="" class="lively-user">刘智勇</a>：@李月 因为脸上有青春痘。</span></div><span class="time">2008-07-02 22:41</span></div>',
        backdrop: true,
        keyboard: true,
        show: true
    }

    $.fn.reply.Constructor = Reply
    
    /* REPLY BINDER DEFINITION */
    function toggleSubmit() {
        var that = this;
        $(that).find('textarea').one('focus', function(){
            if (!$.cookie("uid")) {
                $('#login').modal();
                return false;
            }
            if (!$(that).hasClass('activing')) {
                $(that).addClass('activing');
            }
        });
/*        $(that).find('textarea').one('blur', function(){
            if ($(that).hasClass('activing')) {
                $(that).removeClass('activing');
            }
        });
*/    }

    /* REPLY DATA-API */
    $(function () {
        $('body').find('.reply-submit').each(toggleSubmit);
        $('body').on('click.reply.data-api', '[data-toggle="reply-extend"]', function ( e ) {
            var $this = $(this), href
            , target = $this.attr('data-target') || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '') //strip for ie7
            , option = $(target).data('reply') ? 'toggle' : $.extend({}, $(target).data(), $this.data())
            e.preventDefault()
            $(target).reply(option)
        });
        $('body').on('click.reply.data-api', '[data-toggle="reply-submit"]', Reply.prototype.submit);
    })
}( window.jQuery );





