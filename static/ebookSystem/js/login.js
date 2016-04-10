function alertDialog(status,message) {
    var str=(status=='error')?'danger':'success'
    var dialog='#'+str+'Dialog';
    console.log(dialog);
    $(dialog+" .alertMessage").html(message);
    $(dialog).modal();
    $(dialog+' .close').focus();
    $(dialog+' .close').attr('autofocus',true);

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

            alertDialog(json.status,json.message);
           if(json.hasOwnProperty('redirect_to'))
            {
                $('.close').click(function() {
                    window.location.href = json.redirect_to;
                }); 
            }
        },
        error:function(xhr,errmsg,err){
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });

}
$( document ).ready(function() {
    console.log( "login ready!" );
 //   $('.close').click(function() {
  //      $(this).parent().hide();
  //      $(this).parent().removeClass('in'); // hides alert with Bootstrap CSS3 implem
  //  });
    $('form').on('submit',function(event){
        event.preventDefault();
        console.log("form submitted!");  // sanity check
        catchErrorHandling();
    });
});
