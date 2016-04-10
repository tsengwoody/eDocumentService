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
    if($('.datepicker').length)
        $('.datepicker').datepicker({dateFormat:"yy-mm-dd"});
});