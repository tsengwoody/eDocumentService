function dangerAlert(message) {
    $("#alertMessage").html(message);
    $("#alertDialog").modal();
    $('#alertDialog .close').focus();
    $('#alertDialog .close').attr('autofocus',true);
}
function catchErrorHandling()
{
    $.ajax({
        url:".",
        type: "POST",
        data:{username:$("input[name='username']").val(),password:$("input[name='password']").val()},
        //JSON.stringify
        success: function(json){
            $("input[name='username']").val('');
            $("input[name='password']").val('');
           // $("#result").append("<a href=/article/"+json.id+">"+json.title+"</a>");
            if(json.status=='success')
            {
                window.location.href = json.message;
                return;
            }else if(json.status=='error')
                dangerAlert(json.message);
        },
        error:function(xhr,errmsg,err){
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });

}
$( document ).ready(function() {
    console.log( "login ready!" );
    $('form').on('submit',function(event){
        event.preventDefault();
        console.log("form submitted!");  // sanity check
        catchErrorHandling();
    });
});
