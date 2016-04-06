function checkRegister()
{
    if($("#id_confirm_password").val()!=$("#id_password").val())
    {
        $('#id_confirm_password, #id_password').each(function() {
            this.setCustomValidity("Password Must be Matching.");
        });

    }else{
        $('#id_confirm_password, #id_password').each(function() {
            this.setCustomValidity("");
        });
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