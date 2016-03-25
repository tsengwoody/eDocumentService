function replaceValidationUI()
{
    $(".help-inline").remove();
    $(".danger").removeClass("danger");
    //$('input:valid').parent().parent().addClass("success");
}
$(document).ready(function() {
    console.log("ready!");
    $('input[type="submit"]').click(replaceValidationUI);
    $('input, select').on("invalid", function(e) {
        $(this).parent().parent().addClass("danger");
        $(this).parent().append("<span class='help-inline alert-danger'>"+e.target.validationMessage+"</span>");
        e.preventDefault();
    });
});