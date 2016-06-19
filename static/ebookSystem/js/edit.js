function catchErrorHandling(buttonKey,buttonValue)
{
    console.log($("form"));
    
    var transferData={};
    transferData[buttonKey]=buttonValue;
    $.ajax({
        url:".",
        type: "POST",
        data: $("form").serialize()+'&'+buttonKey+'='+buttonValue,
        success: function(json){
            alertDialog(json);
        },
        error:function(xhr,errmsg,err){
            alert(xhr.status+" "+xhr.responseText);
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });

}
function alertDialog(json) {
    console.log(json);
    var str=(json.status=='error')?'danger':'success'
    var dialog='#'+str+'Dialog';
    $(dialog+" .alertMessage").html(json.message);
    $(dialog).on('shown.bs.modal', function () {
        $(dialog+" .close").focus();
    });
    $(dialog).modal();
    $(dialog).on('hide.bs.modal', function () {
        if(json.hasOwnProperty('redirect_to'))
            window.location.href = json.redirect_to; 
        else
            location.reload();
    });
}
// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$( document ).ready(function() {


});
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
        alertMessageDialog('error','超過頁數範圍惹~');
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

function alertMessageDialog(status,message) {
    var str=(status=='error')?'danger':'success'
    var dialog='#'+str+'Dialog';
    $(dialog+" .alertMessage").html(message);
    $(dialog).on('shown.bs.modal', function () {
        $(dialog+" .close").focus();
    });
    $(dialog).modal();

}

function saveSubmit() {
    //$('#textPage > textarea').val()
    if (typeof $('#id_content').val() == 'undefined') {
        alertMessageDialog('error',"textarea not found");
        return false;
    }
    var str = $('#id_content').val();
    if (str.indexOf("\n|----------|\n") < 0) {
        alertMessageDialog('error',"未save成功，您提交的內容未包含特殊標記，無法得知校對進度，若已全數完成請按下finish按紐");
        return false;
    }
    return true;
}

function finishSubmit() {
    if (typeof $('#id_content').val() == 'undefined') {
        alertMessageDialog("error","textarea not found");
        return false;
    }
    var str = $('#id_content').val();
    if (str.indexOf("|----------|") > 0) {
        alertMessageDialog('error',"未finish成功，您提交的內容包含特殊標記，若已完成請將內容中之特殊標記刪除，若未全數完成請按下save按紐");
        return false;
    }
    return true;
}
function adjZoom(value) {
    imgSize.value = (parseInt(imgSize.value)+ parseInt(value)).toString() + '%';
    $('#scanPage').css('width', imgSize.value);
}
function addMark(strValue) {
    var caretPos = document.getElementById("id_content").selectionStart;
    var textAreaTxt = $("#id_content").val();
    var lastLinePos=textAreaTxt.substring(0, caretPos).lastIndexOf("\n");
    var txtToAdd = strValue;
    if(lastLinePos==-1)
    {
        txtToAdd=txtToAdd+"\n";
        lastLinePos=0;
    }
    $("#id_content").val(textAreaTxt.substring(0, lastLinePos) + txtToAdd + textAreaTxt.substring(lastLinePos));
    document.getElementById("id_content").selectionStart=lastLinePos+1;
    document.getElementById("id_content").selectionEnd=lastLinePos+txtToAdd.length;
}
function calSeconds()
{
    var url=window.location.pathname;
    var newUrl="/"+url.split('/')[1]+"/"+"edit_ajax"+"/"+url.split('/')[3]+"/"+url.split('/')[4]+"/";
    var transferData={};
    transferData["online"]="0";
    //transferData["user_status"]="edit";
    //console.log(newUrl);
    $.ajax({
        url: newUrl,
        type: "POST",
        data: transferData,
        success: function(json){
           //console.log(json);
        },
        error:function(xhr,errmsg,err){
            alert(xhr.status+" "+xhr.responseText);
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}
function skip_mark_click(editor)
{
    editor.insertContent("\n<<<"+$('#scanPageList :selected').val()+">>>");
    //addMark("\n<<<"+$('#scanPageList :selected').val()+">>>")
}
function getIsVaild(obj)
{
    if(obj.attr('name')=="save")
        return saveSubmit();
    else
        return finishSubmit();
    return true;
}
function createHtmlEditor(){
  tinymce.init({
  selector: 'textarea',  // change this value according to your HTML
  toolbar1: 'skip_mark | mark | 存擋',
  toolbar2: 'undo redo | cut copy paste | bullist numlist | table',
  menubar: false,
  setup: function (editor) {
    editor.addButton('skip_mark', {
      text: 'skip_mark',
      icon: false,
      onclick: function () {
        var message = '<p>{{{'+$('#scanPageList :selected').val()+'}}}</p>';
        editor.insertContent(message);
      }
    });

    editor.addButton('mark', {
      text: 'mark',
      icon: false,
      onclick: function () {
        var message = '<p>|----------|</p>';
        editor.insertContent(message);
      }
    });

    editor.addButton('存擋', {
      text: '存擋',
      name: 'save',
      icon: false,
      onclick: function () {
        console.log(editor.getContent());
        console.log(editor.getContent().indexOf('<p>|----------|</p>'));
        if(editor.getContent().indexOf('<p>|----------|</p>')<0)
            alertMessageDialog('error',"未save成功，您提交的內容未包含特殊標記，無法得知校對進度，若已全數完成請按下finish按紐");
        else{
            editor.save();
            catchErrorHandling("save","");
        }
      }
    });



  },

  plugins: [
  'save table']
});
}
$(document).ready(function() {
    console.log("ready!");
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $('button:submit').on('click',function(event){
        event.preventDefault();
        console.log("form submitted!");  // sanity check
        if(getIsVaild($(this))==true)
            catchErrorHandling($(this).attr('name'),$(this).val());
    });
    createHtmlEditor();
    calSeconds();
    setInterval(function(){ 
        calSeconds();
    }, 60000);

    $('#prePage').on("click", function() {
        changePage(-1);
    });
    //nextPage
    $('#nextPage').on("click", function() {
        changePage(1);
    });

    $('#skip_mark_id').click(skip_mark_click);

    $('#mark_id').on("click",function(){
        addMark("\n|----------|");
    });
    $('#zoomIN').on("click",function(){
        adjZoom(-10);
    });
    $('#zoomOUT').on("click",function(){
        adjZoom(10);
    });

    console.log($('#stereotype_id').attr("value"));
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
