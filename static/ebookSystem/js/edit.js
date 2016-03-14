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
        alert('超過頁數範圍惹~');
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
function dangerAlert(message)
{
    $("#alertMessage").html(message);
    $("#danger-alert").alert();
    $("#danger-alert").fadeTo(2000, 500).slideUp(500, function() {
        $("#danger-alert").hide();
    });
}

function saveSubmit(event) {
    if (typeof $('textarea').val() == 'undefined') {
        event.preventDefault();
        dangerAlert("textarea not found")
    }
    var str = $('textarea').val();
    if (str.indexOf("|----------|") < 0) {
        event.preventDefault();
        dangerAlert("not contain the keyword");
    }
}

function finishSubmit(event) {
    if (typeof $('textarea').val() == 'undefined') {
        event.preventDefault();
        dangerAlert("textarea not found");
    }
    var str = $('textarea').val();
    if (str.indexOf("|----------|") > 0) {
        event.preventDefault();
        dangerAlert("can't contain the keyword");
    }
}

$(document).ready(function() {
    console.log("ready!");

    $(".alert button.close").click(function (e) {
        $(this).parent().fadeOut('slow');
    });

    console.log(window.innerHeight);

    $("textarea").height($('.footer').position().top-$("textarea").offset().top-60);
    $(".scrollbarDiv").height(window.innerHeight-$('.footer').height()-$(".scrollbarDiv").offset().top-80);
   
    $('#prePage').on("click", function() {
        changePage(-1);
    });
    //nextPage
    $('#nextPage').on("click", function() {
        changePage(1);
    });

    $('#save_id').click(saveSubmit);
    $('#finish_id').click(finishSubmit);


    $('#zoomIN').click(function() {
        imgSize.value = (parseInt(imgSize.value) - 10).toString() + '%';
        $('#scanPage').css('width', imgSize.value);

    });
    $('#zoomOUT').click(function() {
        imgSize.value = (parseInt(imgSize.value) + 10).toString() + '%';
        $('#scanPage').css('width', imgSize.value);
    });



    $('#chagePost').click(function() {
        if ($('#imagePage').hasClass('col-md-6')) { //改上下
            $('#imagePage').removeClass("col-md-6");
            $('#imagePage').addClass("col-md-12");
            $(".scrollbarDiv").height((window.innerHeight-$('.footer').height()-$(".scrollbarDiv").offset().top-80)/2);
             
        } else {//左右
            $('#imagePage').removeClass("col-md-12");
            $('#imagePage').addClass("col-md-6");
            $(".scrollbarDiv").height(window.innerHeight-$('.footer').height()-$(".scrollbarDiv").offset().top-120);

        }

        if ($('#textPage').hasClass('col-md-6')) { //改上下
            $('#textPage').removeClass("col-md-6");
            $('#textPage').addClass("col-md-12");
            $("textarea").height($('.footer').position().top-$("textarea").offset().top-20);

        } else { //左右
            $('#textPage').removeClass("col-md-12");
            $('#textPage').addClass("col-md-6");
            $("textarea").height($('.footer').position().top-$("textarea").offset().top-100);

        }
        if($('#buttonGroup').hasClass("col-md-12")){
            $('#buttonGroup').removeClass("col-md-12");
            $('#buttonGroup').addClass("col-md-2");
            $('#dataContent').removeClass("col-md-12");
            $('#dataContent').addClass("col-md-10");
            $('#buttonGroup>div').removeClass("btn-group");
            $('#buttonGroup>div').addClass("btn-group-vertical");
        }else{
            $('#buttonGroup').removeClass("col-md-2");
            $('#buttonGroup').addClass("col-md-12");
            $('#dataContent').removeClass("col-md-10");
            $('#dataContent').addClass("col-md-12");
            $('#buttonGroup>div').removeClass("btn-group-vertical");
            $('#buttonGroup>div').addClass("btn-group");
        }
       
        console.log(window.innerHeight);
    });
});
