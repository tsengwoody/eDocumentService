function resetValidationUI()
{
    console.log("resetValidationUI");
    if($(".invalidSpan").length)
    {
        $(".invalidSpan").remove();
    }
    if($(".danger").length)
        $(".danger").removeClass("danger");
}
$(document).ready(function() {
    console.log("ready!");
    if($('.datepicker').length)
        $('.datepicker').datepicker({dateFormat:"yy-mm-dd"});
    //if($('input[type="submit"]').length)
    //    $('input[type="submit"]').click(resetValidationUI);
    //if($('input[type="reset"]').length)
    //    $('input[type="reset"]').click(resetValidationUI);
    //$('input, select').on("invalid", function(e) {
    //    $(this).parent().parent().addClass("danger");
    //    $(this).parent().append("<span class='help-inline alert-danger invalidSpan'>"+e.target.validationMessage+"</span>");
    //    e.preventDefault();
    //});
});