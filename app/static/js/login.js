// var captchaWidgetId;
// var recaptcha_token = "";
// var onReCaptchaLoad = function () {
//     captchaWidgetId = grecaptcha.render('myCaptcha', {
//         'sitekey': '6LfWPykhAAAAAHg0pYSkTHNnzYI2bDlQAUPXwCzt',  // required   
//         'theme': 'light',  // optional   
//         'callback': 'verifyCallback'  // optional   
//     });
// };

// var verifyCallback = function (recaptcha) {
//     //    console.log(recaptcha);
//     recaptcha_token = recaptcha;
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

        // console.log(recaptcha_token);
        let to_backend_data = { "password": password.val(), "username": username.val()}
        console.log(to_backend_data)
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
                if (BackendStatus==200){
                    window.location.href = returnData.redirect;
                }else if(BackendMsg=="登入失敗"){
                    $(".list_log").html('<div class="alert alert-danger" role="alert">login_error</div>')
                    password.val("")
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }

        })

        setTimeout(function () {
            if ($(".alert")) {
                $(".alert").fadeOut(2500);
            }
        },300);

        console.log(username.val(), password.val())
        return false;
    })
})