$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $(".remove").click(function() {
        var $p = $(this).parent().parent();
        var $this = $(this);
        var args = {'id': $p.attr("id").replace("m-","")};
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
