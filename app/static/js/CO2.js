$(document).ready(function () {
    var url_href = window.location.href
    var countInterval = setInterval(function interval() {
        $.ajax({
            url: url_href,
            type: "POST",
            // data: JSON.stringify({"control":"Getdata"}),
            dataType: "json",
            contentType: "application/json;charset=utf-8",
            success: function (returnData) {
                console.log(returnData);
                // console.log($('#TVOC >.data_box>.list_data'))
                let temperature= -46.85 + 175.72 * returnData.temperature / 65536
                let humidity= -6 + 125 * returnData.humidity / 65536
                $('#TVOC >.image_box>p>span').text(returnData.TVOC)
                $('#TVOC >.data_box>.list_data>span').text(returnData.TVOC)
                $('#humidity >.image_box>p>span').text(humidity.toFixed(2))
                $('#humidity >.data_box>.list_data>span').text(humidity.toFixed())
                $('#temperature >.image_box>p>span').text(temperature.toFixed(2))
                $('#temperature >.data_box>.list_data>span').text(temperature.toFixed(1))
                $('#co2 >.image_box>p>span').text(returnData.co2)
                $('#co2 >.data_box>.list_data>span').text(returnData.co2)
           
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        })
        return interval;
    }(), 5000)
})