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
    $('.guest_mode').hide();
    $('.editor_mode').hide();
    $('input[type=checkbox][name=role]:checked').each(function(){
        console.log($(this).val());
        if($(this).val()=='Editor')
            $('.editor_mode').show();
        if($(this).val()=='Guest')
            $('.guest_mode').show();

    });
}
$(document).ready(function() {
    console.log("ready!");
    $(document).ready(function() {
    if($('.datepicker').length)
        $('.datepicker').datepicker({dateFormat:"yy-mm-dd"});
    });
    $('#id_register').click(checkRegister);
    optradioChange();
    $('input[type=checkbox][name=role]').change(optradioChange);
});