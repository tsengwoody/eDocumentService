function formSubmit()
{
    $.ajax({
        url:".",
        type: "POST",
        data: $("form").serialize(),
        success: function(json){
            console.log(json);
            alertDialog(json);
        },
        error:function(xhr,errmsg,err){
            alert(xhr.status+" "+xhr.responseText);
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });

}
function buttonSubmit(buttonKey,buttonValue)
{
    
    var transferData={};
    transferData[buttonKey]=buttonValue;
    //alert(buttonKey);
    $.ajax({
        url:".",
        type: "POST",
        data: transferData,
        success: function(json){
            alertDialog(json);
        },
        error:function(xhr,errmsg,err){
            alert(xhr.status+" "+xhr.responseText);
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}
function formAndButtonSubmit(buttonKey,buttonValue)
{
    var transferData={};
    transferData[buttonKey]=buttonValue;
    $.ajax({
        url:".",
        type: "POST",
        data: $("form").serialize()+'&'+buttonKey+'='+buttonValue,
        success: function(json){
            console.log(json);
            alertDialog(json);
        },
        error:function(xhr,errmsg,err){
            //alert(xhr.status+" "+xhr.responseText);
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });

}
function alertDialog(json) {
    console.log(json.status);
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
            if(json.status!='error')
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
    $('*:submit.send_form').on('click',function(event)
    {
        console.log("send_form");
        event.preventDefault();
        formSubmit();
    });
    $('*:submit.send_button').on('click',function(event)
    {
        console.log("send_button");
        event.preventDefault();
        buttonSubmit($(this).attr('name'),$(this).val());

    });
    $('*:submit.send_form_button').on('click',function(event)
    {
        console.log("send_form_button");
        event.preventDefault();
        formAndButtonSubmit($(this).attr('name'),$(this).val());

    });

});