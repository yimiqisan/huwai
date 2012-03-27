$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    Alert.init();
});


var Alert = {
    init: function(){
        Alert.list();
    },
    
    list: function() {
        var args = {};
        var e = $('#alert');
        $.postJSON("/a/alert/", "GET", args, function(response) {
            if (response.error){
                return alert(response.error);
            }
            ms = response.messages;
            if (ms.length > 0){
                for (var i=0; i<ms.length; i++) {
                    noty({
                        text: "<a id=r-"+ ms[i]['id'] +"' onclick='Alert.click(this);return false;' subject="+ms[i]['subject']+">"+ms[i]['suffix']+"</a>",
                        layout: "topRight",
                        type: "success",
                        timeout: 50000,
                        onClose: function(){},
                    });
                }
            }
        });
    },
    
    click: function(e) {
        var args = {};
        var subject = $(e).attr('subject');
        args['subject'] = subject
        $.postJSON("/a/alert/", 'POST', args, function(response) {
            if (response.error){
                disabled.enable();
                return alert(response.error);
            }
            $(e).css('display', 'none');
            window.location.href = '/alert/'+subject;
        });
    }
};
