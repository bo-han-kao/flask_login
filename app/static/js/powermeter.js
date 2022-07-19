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


    $('.page1_toggle').click(function () {
        var mainParent = $(this).parent('.toggle-btn');
        let select_device = $("#select_device").val();
        let page2_toggle_state = "";
        if ($(mainParent).find('input.cb-value').is(':checked')) {
          $(mainParent).addClass('active');
          console.log("page2 on")
          page2_toggle_state = "ON";
        } else {
          console.log("page2 off")
          $(mainParent).removeClass('active');
          page2_toggle_state = "OFF";
        }
    
        let relay_status = {
          "relay_status": page2_toggle_state
        }
    
        // $.ajax({
        //   type: "POST",
        //   url: url_href+"/powermeter_relay",
        //   data: JSON.stringify(relay_status),
        //   dataType: "json",
        //   contentType: "application/json;charset=utf-8",
        //   success: function (returndata) {
        //     console.log(returndata)
        //   },
        //   error: function (XMLHttpRequest, textStatus, errorThrown) {
        //     console.log(XMLHttpRequest.responseText);
        //   }
        // })
    
      })
})