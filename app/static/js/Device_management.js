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

    $("img").click(function () {
        let device_mac = $(this).parent().parent().attr("id")
        const swalWithBootstrapButtons = Swal.mixin({
            customClass: {
                confirmButton: 'btn btn-success',
                cancelButton: 'btn btn-danger'
            },
            buttonsStyling: false
        })

        swalWithBootstrapButtons.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'No, cancel!',
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {
                swalWithBootstrapButtons.fire(
                    'Deleted!',
                    'Your file has been deleted.',
                    'success'
                )
                $.ajax({
                    url: url_href + "/delete",
                    type: "POST",
                    dataType: "json",
                    contentType: "application/json;charset=utf-8",
                    data: JSON.stringify({ "delete_mac": device_mac }),
                    success: function (returnData) {
                        console.log(returnData);
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        console.log(xhr.status);
                        console.log(thrownError);
                    }
                })
                $(this).parent().parent().remove()
            } else if (
                /* Read more about handling dismissals below */
                result.dismiss === Swal.DismissReason.cancel
            ) {
                swalWithBootstrapButtons.fire(
                    'Cancelled',
                    'Your imaginary file is safe :)',
                    'error'
                )
            }
        })
    })

    var countInterval = setInterval(function interval() {
        $.ajax({
            url: "/powermeter_list_device",
            type: "GET",
            dataType: "json",
            contentType: "application/json;charset=utf-8",
            success: function (returnData) {
                // console.log(returnData)
                try {
                    let old_meterdata = $("tr[name='PowerMeter']")
                    if (old_meterdata.length != 0) {
                        old_meterdata.remove()
                    }
                    let str = "";
                    for (let i = 0; i < returnData.length; i++) {
                        // console.log(returnData[i].device)
                        str += '<tr id=' + returnData[i].device + ' name=' + returnData[i].deviceType + '>'
                        str += ' <th class="thead-sub"></th>'
                        str += ' <td class="thead-uuid" ><a href="/powermeter?devicename=' + returnData[i].device + '">' + returnData[i].device + '</a></td>'
                        str += ' <td class="thead-type">' + returnData[i].deviceType + '</td>'
                        str += ' <th class="thead-delete" ></th>'
                        str += '</tr>'
                    }

                    $('tbody').append(str)
                } catch (error) {
                    console.log("returnData")
                }


            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        })
        return interval;
    }(), 5000);


    $("#send_data").click(function () {
        let postdata = [];
        // console.log($("input[name='Checkbox[]']"))
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

        Swal.fire(
            'success',
            '',
            'success'
          )
    })

    $("#clear_data").click(function () {
     
        const swalWithBootstrapButtons = Swal.mixin({
            customClass: {
                confirmButton: 'btn btn-success',
                cancelButton: 'btn btn-danger'
            },
            buttonsStyling: false
        })

        swalWithBootstrapButtons.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'No, cancel!',
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {
                swalWithBootstrapButtons.fire(
                    'Deleted!',
                    'Your file has been deleted.',
                    'success'
                )
                $.ajax({
                    url: url_href + "/deleteall",
                    type: "POST",
                    dataType: "json",
                    contentType: "application/json;charset=utf-8",
                    data: JSON.stringify(),
                    success: function (returnData) {
                        console.log(returnData);
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        console.log(xhr.status);
                        console.log(thrownError);
                    }
                })

                $("input[name='Checkbox[]']").each(function () {
                    $(this).parent().parent().remove()
                })

            } else if (
                /* Read more about handling dismissals below */
                result.dismiss === Swal.DismissReason.cancel
            ) {
                swalWithBootstrapButtons.fire(
                    'Cancelled',
                    'Your imaginary file is safe :)',
                    'error'
                )
            }
        })
    })

});

