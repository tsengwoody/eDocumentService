function activaTab(tab){
    $('.nav-pills a[href="#' + tab + '"]').tab('show');
};
$(document).ready(function() {
    console.log("ready!");
    //activaTab('step2');
    $('#step1_next_id').click(function(){
        activaTab('step2');
    });
    $('#step2_next_id').click(function(){
        activaTab('step3');
    });
});