$(document).ready(function () {
    var url_href = window.location.href
    var date = new Date();
    var swiper = new Swiper(".mySwiper", {
        pagination: {
            el: ".swiper-pagination",
            dynamicBullets: true,
        },
    });

    function today() {    
        result = date.toLocaleString();
        today_data = result.split(" ")[0]
        $('.watch_date>p').text(today_data)
        // console.log(result)
    }

    function now_time() {
        let date1 = new Date();
        result = date1.toLocaleString('chinese',{hour12:false});
        now_time_data=result.split(" ")[1]
        // console.log(now_time_data)
        return(now_time_data)
    }

    var countInterval = setInterval(function interval() {
        $.ajax({
            url: url_href,
            type: "POST",
            dataType: "json",
            contentType: "application/json;charset=utf-8",
            success: function (returnData) {
                console.log(returnData);
                $('.heart_rate>p>span').text(returnData.Heart_rate)
                $('.blood_oxygen>p>span').text(returnData.Blood_Oxygen)
                $('.temperature>p>span').text(returnData.Temperature / 100)
                $('.Respiration_rate>p>span').text(returnData.Respiration_rate)
                $('.Stress>p>span').text(returnData.Stress)
                $('.steps>p>span').text(returnData.Steps)
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }
        })
        return interval;
    }(), 5000)

    var countInterval1 = setInterval(function interval1() {
        now_time_data=now_time()
        $('.view_time>p').text(now_time_data)
        return interval1;
    }(),1000)

    today();
    
})