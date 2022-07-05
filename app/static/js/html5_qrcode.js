$(document).ready(function () {
  const html5QrCode = new Html5Qrcode("reader");
  var url_domain = window.location.href
  const qrCodeSuccessCallback = (decodedText, decodedResult) => {
    /* handle success */
    console.log(decodedText, decodedResult)
    html5QrCode.stop()
  };

  function startQRcode() {
    html5QrCode.start(
      { facingMode: "environment" },
      {
        fps: 10,    // Optional frame per seconds for qr code scanning
        qrbox: { width: 200, height: 200 }  // Optional if you want bounded box UI
      },
      qrCodeMessage => {
        // do something when code is read
        console.log(qrCodeMessage)
        data_obj = JSON.parse(qrCodeMessage)
        if (!data_obj["mqtt_dongle_id"]) {
          alert('格式不符')
        } else {
          $('#QR_codedata').val(data_obj["mqtt_dongle_id"])
          html5QrCode.stop();
        }

      },
      errorMessage => {
        // parse error, ignore it.
      })
      .catch(err => {
        // Start failed, handle it.
      })
  };


  // If you want to prefer back camera
  // html5QrCode.start({ facingMode: "environment" }, config, qrCodeSuccessCallback);
  $('#start-scan').click(function () {
    startQRcode()
  })

  $('#end-scan').click(function () {
    html5QrCode.stop();
  })

  


  $('#bind').click(function () {
    let mqtt_id = $('#QR_codedata').val()
    let postdata = { "mqtt_id": mqtt_id }
    console.log(mqtt_id)
    $.ajax({
      url: url_domain + "/edit",
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
})


