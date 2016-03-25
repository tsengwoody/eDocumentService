function alertError(message)
{
    alert(message);
}
function checkRegister()
{
    if($("#id_confirm_password").val()!=$("#id_password").val())
    {
        event.preventDefault();
        alertError("密碼不一致")
    }
}
function optradioChange()
{
    if(this.value=="Editor")
    {
        $('#editor_only').show();
    }else{
        $('#editor_only').hide();
    }
}
$(document).ready(function() {
    console.log("ready!");
    $('#id_register').click(checkRegister);
    $('input[type=radio][name=role]').change(optradioChange);
});