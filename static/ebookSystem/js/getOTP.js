var otpID;
function getOTP(sender) {

    var otpURL = "/genericUser/verify_contact_info/";
    var transferData={};
    transferData["generate"]=sender.val();
    console.log(transferData);

    
    $.ajax({
        url: otpURL,
        type: "POST",
        data: transferData,
        beforeSend:function(jqXHR, settings){
            jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            $('#id_get_otp_load').show();
            sender.addClass("disabled");
        },
        success: function(json) {
            $('#id_send_info').text("已傳送到"+$('#id_send_value').val());
            $('#id_get_otp_load').hide();
            $('#id_get_otp').html('取得驗證碼<span class="badge">600</span>');
            var w=600;
            otpID=setInterval(function(){ 
                if(w==0){
                    clearInterval(id);
                    $('#id_send_info').text('');
                    sender.removeClass("disabled");
                    $('#id_get_otp').html('取得驗證碼');
                }else{
                    w--;
                    $('#id_get_otp').html('取得驗證碼<span class="badge">'+w+'</span>');
                }
            }, 1000);
            //TODO: 顯示倒數計時，使用setTimeOut
            
        },
        error: function(xhr, errmsg, err) {
            alert(xhr.status + ": " + xhr.responseText);
            console.log(xhr.status + ": " + xhr.responseText);
             $('#id_get_otp_load').hide();
             sender.removeClass("disabled");
        }
    });
}

function verifyOTP(sender) {

    var otpURL = "/genericUser/verify_contact_info/";
    var transferData={};
    transferData["verification_code"]=$('#recipient-code').val();
    transferData["type"]=sender.val();
    
    $.ajax({
        url: otpURL,
        type: "POST",
        data: transferData,
        beforeSend:function(jqXHR, settings){
            jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            $('#id_get_otp').removeClass('disabled');
            $('#id_send_info').text('');
            sender.removeClass("disabled");
            $('#id_get_otp').html('取得驗證碼');
            clearInterval(otpID);
            
        },
        success: function(json) {
            alertDialog(json);
            $('#otpModal').modal('toggle');
            $('#recipient-code').val('');
        },
        error: function(xhr, errmsg, err) {
            $('#recipient-code').val('');
            alert(xhr.status + ": " + xhr.responseText);
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}


$( document ).ready(function() {
    console.log( "document ready!" );

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#otpModal').on('show.bs.modal', function (event) {
          var button = $(event.relatedTarget) // Button that triggered the modal
          var recipient = button.data('whatever') // Extract info from data-* attributes 
          console.log(button.data('sendto'));
          console.log(recipient);
            if(recipient=="email")
                $('#otpModalLabel').text("信箱驗證碼");
            if(recipient=="phone")
                $('#otpModalLabel').text("手機驗證碼");
           $('#id_get_otp').val(recipient);
           $('#send_otp').val(recipient);
           $('#id_send_value').val(button.data('sendto'));
    });
    $('#id_get_otp').on("click",function(event){
        //console.log($(this).val());
        getOTP($(this));
    });
    $('#send_otp').on("click",function(event){
        //console.log($(this).val());
        verifyOTP($(this));
    });
});