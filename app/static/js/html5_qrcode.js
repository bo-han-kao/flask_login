$(document).ready(function () {
  const html5QrCode = new Html5Qrcode("reader");
  var url_domain = window.location.href
  const qrCodeSuccessCallback = (decodedText, decodedResult) => {
    /* handle success */
    console.log(decodedText, decodedResult)

  };

  function startQRcode() {
    html5QrCode.start(
      { facingMode: "user" },
      {
        fps: 10,    // Optional frame per seconds for qr code scanning
        qrbox: { width: 200, height: 200 }  // Optional if you want bounded box UI
      },
      qrCodeMessage => {
        // do something when code is read
        console.log(qrCodeMessage)
        data_obj = JSON.parse(qrCodeMessage)
        console.log(typeof(data_obj))
        if (data_obj["GW2"]) {
          let str = '';
          str += ' <div class="alert alert-success" id="msg" role="alert">'
          str += 'sucess to scan'
          str += '</div>'
          $('#alertbox').html(str)
          $('#QR_codedata').val(data_obj["GW2"])
          $('#msg').fadeOut(3000);
          html5QrCode.stop();
          $('#end-scan').addClass("d-none")
          $('#start-scan').removeClass("d-none")
          
        } else {
          let str = '';
          str += ' <div class="alert alert-danger" id="msg" role="alert">'
          str += ' paload error'
          str += '</div>'
          $('#alertbox').html(str)
          $('#msg').fadeOut(5000);
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
    qrCodeSuccessCallback()
    startQRcode();
    $(this).addClass("d-none")
    $('#QR_codedata').val("")
    $('#end-scan').removeClass("d-none")
  })

  $('#end-scan').click(function () {
    html5QrCode.stop();
    $(this).addClass("d-none")
    $('#start-scan').removeClass("d-none")
  })

  $('#bind').click(function () {
    let mqtt_id = $('#QR_codedata').val()
    let postdata = { "mqtt_id": mqtt_id }
    $('#QR_codedata').val("")
    // console.log(mqtt_id)
    $.ajax({
      url: url_domain + "/edit",
      type: "POST",
      dataType: "json",
      contentType: "application/json;charset=utf-8",
      data: JSON.stringify(postdata),
      success: function (returnData) {
        console.log(returnData);
        let str = '';
        str += ' <div class="alert alert-success" id="msg" role="alert">'
        str += ' success to bind dongle'
        str += '</div>'
        $('#alertbox').html(str)
        $('#msg').fadeOut(5000);
      },
      error: function (xhr, ajaxOptions, thrownError) {
        console.log(xhr.status);
        console.log(thrownError);
      }
    })
  })
})


