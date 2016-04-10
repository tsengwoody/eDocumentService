function changePage(offset) {
    page = document.getElementById("id_page");
    imgScanPage = $('#scanPage')[0];
    src = imgScanPage.src;
    src = src.split('/');
    dirname = ''
    for (i = 0; i < src.length - 1; i++) dirname = dirname + src[i] + '/';
    filename = src[src.length - 1];
    extensionName = filename.split('.')[1];
    filename = filename.split('.')[0];
    scanPageList = document.getElementById("scanPageList");
    if (scanPageList.selectedIndex + offset >= 0 && scanPageList.selectedIndex + offset < scanPageList.length) {
        scanPageList.selectedIndex = scanPageList.selectedIndex + offset;
        page.value = scanPageList.selectedIndex;
        imgScanPage.src = dirname + scanPageList.options[scanPageList.selectedIndex].value;
    } else {
        //dangerAlert('超過頁數範圍惹~');
        alertDialog('error','超過頁數範圍惹~');
    }
}

function changePageSelect() {
    page = document.getElementById("id_page");
    imgScanPage = $('#scanPage')[0];
    src = imgScanPage.src;
    console.log(src);
    src = src.split('/');
    dirname = ''
    for (i = 0; i < src.length - 1; i++)
        dirname = dirname + src[i] + '/';
    filename = src[src.length - 1];
    extensionName = filename.split('.')[1];
    filename = filename.split('.')[0];
    scanPageList = document.getElementById("scanPageList");
    page.value = scanPageList.selectedIndex;
    imgScanPage.src = dirname + scanPageList.options[scanPageList.selectedIndex].value;
}

function alertDialog(status,message) {
    var str=(status=='error')?'danger':'success'
    var dialog='#'+str+'Dialog';
    console.log(dialog);
    $(dialog+" .alertMessage").html(message);
    $(dialog).modal();
    $(dialog+' .close').focus();
    $(dialog+' .close').attr('autofocus',true);

}

function saveSubmit(event) {
    //console.log($("#danger-alert"));
    if (typeof $('#id_content').val() == 'undefined') {
        event.preventDefault();
        //dangerAlert("textarea not found")
        alertDialog('error',"textarea not found");
    }
    var str = $('#id_content').val();
    if (str.indexOf("|----------|") < 0) {
        event.preventDefault();
        //dangerAlert("未save成功，您提交的內容未包含特殊標記，無法得知校對進度，若已全數完成請按下finish按紐");
        alertDialog('error',"未save成功，您提交的內容未包含特殊標記，無法得知校對進度，若已全數完成請按下finish按紐");
    }
}

function finishSubmit(event) {
    if (typeof $('#id_content').val() == 'undefined') {
        event.preventDefault();
        dangerAlert("textarea not found");
    }
    var str = $('#id_content').val();
    if (str.indexOf("|----------|") > 0) {
        event.preventDefault();
        //dangerAlert("未finish成功，您提交的內容包含特殊標記，若已完成請將內容中之特殊標記刪除，若未全數完成請按下save按紐");
        alertDialog('error',"未finish成功，您提交的內容包含特殊標記，若已完成請將內容中之特殊標記刪除，若未全數完成請按下save按紐");
    }
}
function adjZoom(value) {
    imgSize.value = (parseInt(imgSize.value)+ parseInt(value)).toString() + '%';
    $('#scanPage').css('width', imgSize.value);
}
function addMark() {
    var caretPos = document.getElementById("id_content").selectionStart;
    var textAreaTxt = $("#id_content").val();
    var lastLinePos=textAreaTxt.substring(0, caretPos).lastIndexOf("\n");
    var txtToAdd = "\n|----------|";
    $("#id_content").val(textAreaTxt.substring(0, lastLinePos) + txtToAdd + textAreaTxt.substring(lastLinePos));
    document.getElementById("id_content").selectionStart=lastLinePos+1;
    document.getElementById("id_content").selectionEnd=lastLinePos+txtToAdd.length;
    
}

$(document).ready(function() {
    console.log("ready!");
    $('#prePage').on("click", function() {
        changePage(-1);
    });
    //nextPage
    $('#nextPage').on("click", function() {
        changePage(1);
    });
    $('#save_id').click(saveSubmit);
    $('#finish_id').click(finishSubmit);
    $('#mark_id').click(addMark);
    $('#zoomIN').on("click",function(){
        adjZoom(-10);
    });
    $('#zoomOUT').on("click",function(){
        adjZoom(10);
    });
    $('#chagePost').click(function() {
        $('#id_content').removeAttr('style');
        if ($('#imagePage').hasClass('col-md-6')) { //改上下
            $('#imagePage').removeClass("col-md-6");
            $('#imagePage').addClass("col-md-12");
            $('#textPage').removeClass("col-md-6");
            $('#textPage').addClass("col-md-12");
            $('#textPage').removeClass("towColumn");
            $('#textPage').addClass("oneColumn");
        } else { //左右
            $('#imagePage').removeClass("col-md-12");
            $('#imagePage').addClass("col-md-6");
            $('#textPage').removeClass("col-md-12");
            $('#textPage').addClass("col-md-6");
            $('#textPage').removeClass("oneColumn");
            $('#textPage').addClass("towColumn");

        }
        if ($('#buttonGroup').hasClass("col-md-12")) { //改上下
            $('#buttonGroup').removeClass("col-md-12");
            $('#buttonGroup').addClass("col-md-2");
            $('#dataContent').removeClass("col-md-12");
            $('#dataContent').addClass("col-md-10");
            $('#buttonGroup>div').removeClass("btn-group");
            $('#buttonGroup>div').addClass("btn-group-vertical");
        } else {
            $('#buttonGroup').removeClass("col-md-2");
            $('#buttonGroup').addClass("col-md-12");
            $('#dataContent').removeClass("col-md-10");
            $('#dataContent').addClass("col-md-12");
            $('#buttonGroup>div').removeClass("btn-group-vertical");
            $('#buttonGroup>div').addClass("btn-group");
        }

    });
});
