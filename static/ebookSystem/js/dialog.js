$( document ).ready(function() {
    console.log( "document ready!" );
    if($('.modal.fade.in').length>0)
    {
        $('.modal.fade.in').on('shown.bs.modal', function () {
            $('.modal.fade.in .close').focus();
        });
        $('.modal.fade.in').modal();
    }
    $('[data-toggle="tooltip"]').tooltip();
});