$(document).ready(function () {

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
        let postdata={};
        console.log($("input[name='Checkbox[]']"))
        $("input[name='Checkbox[]']").each(function () {
            if($(this).prop("checked")){
                console.log("被選取")
                console.log($(this).parent().parent().attr("id"))
               
            }else{
                console.log("沒選取")
                console.log($(this).parent().parent().attr("id"))
            }
        })
    })
});

