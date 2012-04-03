var Event = {
    checka: function(){
        $("input[type=submit]").click(function(){
            $(".error").removeClass("error");
            //check title
            if (!$("input[name=title]").val()){alert('请填写标题');$("input[name=title]").parent().parent().addClass('error');$("input[name=title]").select();return false;}
            //check place
            if (!$("input[name=place]").val()){alert('请填写地点');$("input[name=place]").parent().parent().addClass('error');$("input[name=place]").select();return false;}
            //check schedule_tl
            if (!$("textarea[name=schedule_tl]").val()){alert('请填写行程安排');$("textarea[name=schedule_tl]").parent().parent().addClass('error');$("textarea[name=schedule_tl]").select();return false;}
            //check spend_tl
            if (!$("textarea[name=spend_tl]").val()){alert('请填写费用明细');$("textarea[name=spend_tl]").parent().parent().addClass('error');$("textarea[name=spend_tl]").select();return false;}
            //check date
            var now = new Date();
            var y = parseInt($("#begin_time_year").val());
            var m = parseInt($("#begin_time_month").val());
            var d = parseInt($("#begin_time_day").val());
            var h = parseInt($("#begin_time_hour").val());
            var i = parseInt($("#begin_time_minute").val());
            var sdate = new Date(y,m-1,d,h,i);
            if (now > sdate){alert('您填写的活动时间已过!');return false;}
            //check date
            $(".event-form").submit();
            return false;
        });
    },
    
    checkb: function(){
        $("input[type=submit]").click(function(){
            //check people number
            var fr = $("input[name=fr]").val()
            var to = $("input[name=to]").val()
            if (fr > to){alert('人数起止不正确');$("input[name=fr]").select();return false;}
            var now = new Date();
            var y = parseInt($("#close_time_year").val());
            var m = parseInt($("#close_time_month").val());
            var d = parseInt($("#close_time_day").val());
            var h = parseInt($("#close_time_hour").val());
            var i = parseInt($("#close_time_minute").val());
            var edate = new Date(y,m-1,d,h,i);
            var y = parseInt($("#collect_time_year").val());
            var m = parseInt($("#collect_time_month").val());
            var d = parseInt($("#collect_time_day").val());
            var h = parseInt($("#collect_time_hour").val());
            var i = parseInt($("#collect_time_minute").val());
            var cdate = new Date(y,m-1,d,h,i);
            if (edate <= now){alert("报名截止时间应该晚于当前时间!");return false;}
            if (cdate <= edate){alert("活动开始时间应该晚于报名截止时间!");return false;}
            $("#event form").submit();
            return false;
        });
    },
};
