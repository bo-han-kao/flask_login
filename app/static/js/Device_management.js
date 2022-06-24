$(document).ready(function () {
    var url_domain = window.location.href
    console.log(url_domain)
    $("#checkall").click(function () {
        if ($("#checkall").prop("checked")) {
            $("input[name='Checkbox[]']").each(function () {
                $(this).prop("checked", true);
            })
        } else {
            $("input[name='Checkbox[]']").each(function () {
                $(this).prop("checked", false);//把所有的核方框的property都取消勾選
            })
        }
    })


    $("#send_data").click(function () {
        let postdata=[];
        console.log($("input[name='Checkbox[]']"))
        $("input[name='Checkbox[]']").each(function () {
            let devicename=$(this).parent().parent().attr("id")
            if($(this).prop("checked")){
                console.log("被選取")
                postdata.push({"devicename":devicename,"status":true})
               
            }else{
                console.log("沒選取")
                postdata.push({"devicename":devicename,"status":false})
            }
        })
        console.log(postdata)
        $.ajax({
            url:url_domain+"/edit",
            type:"POST",
            dataType:"json",
            contentType: "application/json;charset=utf-8",
            data:JSON.stringify(postdata),
            success: function (returnData) {
                console.log(returnData);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        })
    })
});

