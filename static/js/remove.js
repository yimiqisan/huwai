$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $(".remove").click(function() {
        var did = $(this).attr("id");
        var mid = did.replace("d-", "m-");
        var $p = $("#"+mid);
        var args = {'id': did.replace("d-","")};
        $.ajax({
            url: "/a/remove", 
            type: "POST", 
            dataType: "text",
            data: $.param(args), 
            beforeSend: function() {
                $p.css("color", "#D6EED8");
            },
            success: function() {
                $p.slideUp(300, function() {$p.remove();})
            }
        });
    });
});
