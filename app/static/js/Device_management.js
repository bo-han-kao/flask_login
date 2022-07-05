$(document).ready(function () {
    var url_href = window.location.href
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
        let postdata = [];
        console.log($("input[name='Checkbox[]']"))
        $("input[name='Checkbox[]']").each(function () {
            let devicename = $(this).parent().parent().attr("id")
            if ($(this).prop("checked")) {
                postdata.push({ "devicename": devicename, "status": true })
            } else {
                postdata.push({ "devicename": devicename, "status": false })
            }
        })
        console.log(postdata)
        $.ajax({
            url: url_href + "/edit",
            type: "POST",
            dataType: "json",
            contentType: "application/json;charset=utf-8",
            data: JSON.stringify(postdata),
            success: function (returnData) {
                console.log(returnData);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        })

    })
    var countInterval=setInterval(function interval() {
        $.ajax({
            url: "/powermeter_list_device",
            type: "GET",
            dataType: "json",
            contentType: "application/json;charset=utf-8",
            success: function (returnData) {
                try {
                    let old_meterdata = $("tr[name='PowerMeter']")
                    if (old_meterdata.length != 0) {
                        old_meterdata.remove()
                    }
                    let str = "";
                    for (let i = 0; i < returnData.length; i++) {
                        console.log(returnData[i].device)
                        str += '<tr id=' + returnData[i].device + ' name=' + returnData[i].deviceType + '>'
                        str += ' <th class="col-2"><input type="checkbox"   aria-label="Checkbox for following text input" disabled></th>'
                        str += ' <td class="col-6" ><a href="/powermeter?devicename=' + returnData[i].device + '">' + returnData[i].device + '</a></td>'
                        str += ' <td class="col-4">' + returnData[i].deviceType + '</td>'
                        str += '</tr>'
                    }

                    $('tbody').append(str)
                } catch (error) {
                    console.log("returnData")
                }
                if ($("tr[name='PowerMeter']")) {
                    console.log("存在")
                } else {
                    console.log("不存在")
                }

            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        })
        return interval;
    }(), 5000);

});

