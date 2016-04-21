function gen_uuid() {
    var uuid = ""
    for (var i=0; i < 32; i++) {
        uuid += Math.floor(Math.random() * 16).toString(16); 
    }
    return uuid
}
function catchErrorHandling()
{
    var uuid=gen_uuid();
    $('#X-Progress-ID').val(uuid);
    console.log( $('#X-Progress-ID').val());
    var formData = new FormData($('form').get(0));
    
    $.ajax({
        url:".",
        type: "POST",
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        beforeSend:function(){
            $('#pleaseWaitDialog').modal('show');
        },
        success: function(json){
            $('#pleaseWaitDialog').modal('hide');
            alertDialog(json);
        },
        error:function(xhr,errmsg,err){
            $('#pleaseWaitDialog').modal('hide');
            alert(xhr.status+" "+xhr.responseText);
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
        window.setTimeout(function() {
                showProgress(uuid);
            }, 1000);

    
}
function showProgress(uuid)
{
    console.log(uuid);
    $.getJSON('/guest/upload_progress', {'X-Progress-ID': uuid},function(data,status,xhr){
        console.log(data);
        console.log(status);
        console.log(xhr.responseText);

        if(data){
            var progress = (parseInt(data.uploaded) / parseInt(data.length))*100;
            $('#uploadProgressBar').css('width', progress+'%').attr('aria-valuenow', progress);
            $('#uploadProgressText').text(progress+'% Complete (success)');
           
        }else{
            
            return;
        }
         window.setTimeout(function() {
                showProgress(uuid);
            }, 1000);

    });
}
function alertDialog(json) {
    var str=(json.status=='error')?'danger':'success'
    var dialog='#'+str+'Dialog';
    $(dialog+" .alertMessage").html(json.message);
    $(dialog).on('shown.bs.modal', function () {
        $(dialog+" .close").focus();
    });
    $(dialog).modal();
    $(dialog).on('hide.bs.modal', function () {
        if(json.hasOwnProperty('redirect_to'))
            window.location.href = json.redirect_to; 
        else
            location.reload();
    });
}
// This function gets cookie with a given name
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
    //showProgress();
   // $('#pleaseWaitDialog').modal('show');
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
    if($('.datepicker').length)
        $('.datepicker').datepicker({dateFormat:"yy-mm-dd"});
    $('form').on('submit',function(event){
        event.preventDefault();
        console.log("form submitted!");  // sanity check
        catchErrorHandling();
    });

});