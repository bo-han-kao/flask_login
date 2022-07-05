$(document).ready(function () {
    var url_href = window.location.href
    var countInterval = setInterval(function interval() {
        $.ajax({
            url: url_href,
            type: "POST",
            dataType: "json",
            contentType: "application/json;charset=utf-8",
            success: function (returnData) {
                console.log(returnData);
                $('.watt_hour_val').text(returnData.watt_hour/10)
                $('.watt_val').text(returnData.watt/10)
                $('.amp.val').text(returnData.current/10)
                $('.volt_val').text(returnData.volt/10)
                $('.hz_val').text(returnData.frequency/10)
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        })
        return interval;
    }(), 5000)
})