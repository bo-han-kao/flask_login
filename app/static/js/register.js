// var captchaWidgetId;   
// var recaptcha_token="";
// var onReCaptchaLoad = function() {   
  
//             captchaWidgetId = grecaptcha.render( 'myCaptcha', {   
//                 'sitekey' : '6LfWPykhAAAAAHg0pYSkTHNnzYI2bDlQAUPXwCzt',  // required   
//                 'theme' : 'light',  // optional   
//                 'callback': 'verifyCallback'  // optional   
//             });   
// };   
  
// var verifyCallback = function( recaptcha ) {   
//     //    console.log(recaptcha);
//        recaptcha_token=recaptcha;
// };  

$(document).ready(function () {
    var url_href = window.location.href
  
    $('#eye_img').parent().click(
        function () {
            if ($("#eye_img").attr("src") == "/static/img/register/open_eye.svg") {
                $("#password").attr("type", "text");
                $("#eye_img").attr("src", "/static/img/register/close_eye.svg")
            } else {
                $("#password").attr("type", "password");
                $("#eye_img").attr("src", "/static/img/register/open_eye.svg")
            }
        }
    )

    $('#form_data').submit(function () {
        let username = $("input[name='user']");
        let password = $("input[name='password']");
        let confirm = $("input[name='confirm']");
        // console.log(recaptcha_token);
        if (password.val() == confirm.val()) {
            let to_backend_data = { "password": password.val(), "username": username.val()}
            $.ajax({
                url: url_href,
                type: "POST",
                data: JSON.stringify(to_backend_data),
                dataType: "json",
                contentType: "application/json;charset=utf-8",
                success: function (returnData) {
                    console.log(returnData)
                    BackendStatus = returnData.status
                    BackendMsg = returnData.msg
                    if (BackendStatus == 200) {
                        window.location.href = returnData.redirect;
                    } else if (BackendMsg == "duplicate_name") {
                        $(".list_log").html('<div class="alert alert-danger" role="alert">duplicate name</div>')
                    } else if (BackendMsg == "duplicate_Line_id") {
                        $(".list_log").html('<div class="alert alert-danger" role="alert">duplicate Line</div>')
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }

            })
        } else {
            $(".list_log").html('<div class="alert alert-danger" role="alert">驗證密碼錯誤</div>')
            confirm.val("");
        }

        setTimeout(function () {
            if ($(".alert")) {
                $(".alert").fadeOut(2500);
            }
        }, 100);

        console.log(username.val(), password.val(), confirm.val())
        return false;
    })
    // $.ajax({
    //     url: url_href,
    //     type: "POST",
    //     // data: JSON.stringify({"control":"Getdata"}),
    //     dataType: "json",
    //     contentType: "application/json;charset=utf-8",
    //     success: function (returnData) {
    //         console.log(returnData);
    //     },
    //     error: function (xhr, ajaxOptions, thrownError) {
    //         console.log(xhr.status);
    //         console.log(thrownError);
    //     }
    // })

})