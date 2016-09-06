function catchErrorHandling(buttonKey,buttonValue)
{
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
            //alert(xhr.status+" "+xhr.responseText);
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });

}
function alertDialog(json) {
    //console.log(json);
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
    //console.log(src);
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
function adjZoom(value) {
    if (parseInt(imgSize.value)+ parseInt(value)>0)
    {
        imgSize.value = (parseInt(imgSize.value)+ parseInt(value)).toString() + '%';
        $('#scanPage').css('width', imgSize.value);
    }
}
function addMark(strValue,editor) {

    var bm = editor.selection.getBookmark(0);    
    var caretPos = getCursorPosition(editor);
    var textAreaTxt = editor.getContent();
    var subCarePos = textAreaTxt.substring(0, caretPos);
    var lastLinePos =-1
    var nextLine = ["\n", "<br />", "<br>","</p>"];
    lastLinePos = -1;
    lastNextLineIndex=0;
    for(var index in nextLine)
    {
        if(lastLinePos < subCarePos.lastIndexOf(nextLine[index]))
        {
            lastLinePos = subCarePos.lastIndexOf(nextLine[index]);
            lastNextLineIndex=index;
        }
    }
    lastLinePos += nextLine[lastNextLineIndex].length;
    setCursorPosition(editor,lastLinePos)
    editor.insertContent(strValue);

}
function detectIdel()
{
    console.log(idel_min);
    if(idel_min>30)
    {
        function_click=true;
        idel_min=0;
        window.location.href = "/auth/logout/";
    }
    idel_min++;
}
function calMins()
{
    var url=window.location.pathname;
    var newUrl="/"+url.split('/')[1]+"/"+"edit_ajax"+"/"+url.split('/')[3]+"/";
    var transferData={};
    transferData["online"]="0";
    $.ajax({
        url: newUrl,
        type: "POST",
        data: transferData,
        success: function(json){
           //console.log(json);
        },
        error:function(xhr,errmsg,err){
            //alert(xhr.status+" "+xhr.responseText);
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}
function setCursorPosition(editor,index)
{
    //get the content in the editor before we add the bookmark... 
    //use the format: html to strip out any existing meta tags
    var content = editor.getContent({format: "html"});

    //split the content at the given index
    var part1 = content.substr(0, index);
    var part2 = content.substr(index);

    //create a bookmark... bookmark is an object with the id of the bookmark
    var bookmark = editor.selection.getBookmark(0);

    //this is a meta span tag that looks like the one the bookmark added... just make sure the ID is the same
    var positionString = '<span id="'+bookmark.id+'_start" data-mce-type="bookmark" data-mce-style="overflow:hidden;line-height:0px"></span>';
    //cram the position string inbetween the two parts of the content we got earlier
    var contentWithString = part1 + positionString + part2;

    //replace the content of the editor with the content with the special span
    //use format: raw so that the bookmark meta tag will remain in the content
    editor.setContent(contentWithString, ({format: "raw"}));

    //move the cursor back to the bookmark
    //this will also strip out the bookmark metatag from the html
    editor.selection.moveToBookmark(bookmark);

    //return the bookmark just because
    return bookmark;
}
function getCursorPosition(editor){
    //set a bookmark so we can return to the current position after we reset the content later
    var bm = editor.selection.getBookmark(0);    

    //select the bookmark element
    var selector = "[data-mce-type=bookmark]";
    var bmElements = editor.dom.select(selector);

    //put the cursor in front of that element
    editor.selection.select(bmElements[0]);
    editor.selection.collapse();

    //add in my special span to get the index...
    //we won't be able to use the bookmark element for this because each browser will put id and class attributes in different orders.
    var elementID = "######cursor######";
    var positionString = '<span id="'+elementID+'"></span>';
    editor.selection.setContent(positionString);

    //get the content with the special span but without the bookmark meta tag
    var content = editor.getContent({format: "html"});
    //find the index of the span we placed earlier
    var index = content.indexOf(positionString);

    //remove my special span from the content
    editor.dom.remove(elementID, false);            

    //move back to the bookmark
    editor.selection.moveToBookmark(bm);

    return index;
}
function rotateFormat()
{
    if ($('#imagePage').hasClass('col-md-6')) { //改上下
        $('#imagePage').removeClass("col-md-6");
        $('#imagePage').addClass("col-md-12");


        $('#textPage').removeClass("col-md-6");
        $('#textPage').addClass("col-md-12");
        
        $('#textPage').removeClass("towColumn");
        $('#textPage').addClass("oneColumn-text");

        $('#imagePage').removeClass("towColumn");
        $('#imagePage').addClass("oneColumn-image");
    } else { //左右
        $('#imagePage').removeClass("col-md-12");
        $('#imagePage').addClass("col-md-6");
        
        $('#textPage').removeClass("col-md-12");
        $('#textPage').addClass("col-md-6");
        
        $('#textPage').removeClass("oneColumn-text");
        $('#textPage').addClass("towColumn");

        $('#imagePage').removeClass("oneColumn-image");
        $('#imagePage').addClass("towColumn");
    }

}
var function_click = false;
var idel_min =0;
function createHtmlEditor(){

//http://blog.squadedit.com/tinymce-and-cursor-position/
  tinymce.init({
  forced_root_block : "", 
  force_br_newlines : false,
  force_p_newlines : false,
  selector: 'textarea',  // change this value according to your HTML
  toolbar1: 'skip_mark | mark | 存擋 | 完成 | 關閉 | 切換版型',
  toolbar2: 'undo redo | cut copy paste | bullist numlist | table | fontsizeselect',
  fontsize_formats: '8pt 10pt 12pt 14pt 18pt 24pt 36pt',
  menubar: false,
  setup: function (editor) {
    editor.addButton('skip_mark', {
      text: 'skip_mark',
      icon: false,
      onclick: function () {
        var message = '<p>{{{'+$('#scanPageList :selected').val()+'}}}</p>';
        addMark(message,editor);
      }
    });
    editor.on('change', function(e) {
        //console.log(idel_min);
        idel_min=0;
    });
    editor.addButton('mark', {
      text: 'mark',
      icon: false,
      onclick: function () {
        var message = '<p>|----------|</p>';
        addMark(message,editor);

      }
    });

    editor.addButton('存擋', {
      text: '存擋',
      name: 'save',
      icon: false,
      onclick: function () {
        if(editor.getContent().indexOf('<p>|----------|</p>')<0)
            alertMessageDialog('error',"未存擋成功，您提交的內容未包含特殊標記，無法得知校對進度，若已全數完成請按下完成按紐");
        else{
            function_click=true;
            editor.save();
            catchErrorHandling("save","");

        }
      }
    });
    editor.addButton('完成', {
      text: '完成',
      name: 'finish',
      icon: false,
      onclick: function () {
        if(editor.getContent().indexOf('<p>|----------|</p>')>0)
            alertMessageDialog('error',"未存擋成功，您提交的內容包含特殊標記，若已完成請將內容中之特殊標記刪除，若未全數完成請按下存擋按紐");
        else{
            function_click=true;
            editor.save();
            catchErrorHandling("finish","");
        }
      }
    });
    editor.addButton('關閉', {
      text: '關閉',
      name: 'finish',
      icon: false,
      onclick: function () {
        function_click=true;
        catchErrorHandling("close","");
      }
    });
    editor.addButton('切換版型', {
      text: '切換版型',
      name: 'rotateFormat',
      icon: false,
      onclick: function () {
        rotateFormat();
      }
    });

  },
  plugins: [
  'save table'],

});


}
$(document).ready(function() {
    console.log("ready!");
    function_click = false;
    idel_min =0;

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
    createHtmlEditor();
    calMins();
    setInterval(function(){ 
        calMins();
        detectIdel();
    }, 60000);

    $('#prePage').on("click", function() {
        changePage(-1);
    });
    //nextPage
    $('#nextPage').on("click", function() {
        changePage(1);
    });


    $('#zoomIN').on("click",function(){
        adjZoom(-10);
    });
    $('#zoomOUT').on("click",function(){
        adjZoom(10);
    });


    $(window).on('beforeunload', function(e){
      if(function_click)
        return;
      function_click=false;
      return 'Are you sure you want to leave?';
    });
});
