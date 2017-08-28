function o2j(v) {
    //物件轉json文字

    let c = '';
    try {
        c = JSON.stringify(v);
        //c = JSON.stringify(v, null, '\t');
    }
    catch (err) {
    }

    return c;
}


function j2o(v) {
    //json文字轉物件

    let c = {};
    try {
        c = JSON.parse(v);
    }
    catch (err) {
    }

    return c;
}


function utoa(str) {
    //任意字串轉base64字串

    //btoa
    let r = window.btoa(unescape(encodeURIComponent(str)));

    return r;
}


function atou(str) {
    //base64字串轉任意字串

    //atob
    let r = decodeURIComponent(escape(window.atob(str)));

    return r;
}


function o2b(obj) {
    //物件轉base64字串

    let r = '';
    try {
        r = utoa(o2j(obj));
    }
    catch (err) {
    }

    return r;
}


function b2o(str) {
    //base64字串轉物件

    let r = {};
    try {
        r = j2o(atou(str));
    }
    catch (err) {
    }

    return r;
}


function GenID() {
    let p = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let c = "";
    let n = 32;
    for (let i = 0; i < n; i++) {
       c += p.charAt(Math.floor(Math.random() * p.length));
    }
    return c;
    //return Math.uuid(32);
}


function downloadfile(cfn, bindata) {
	//下載binary資料成為檔案
	//使用標籤a與blob物件直接將bindata下載成為檔案

	//tag a
	let downloadLink = document.createElement('a');
	let blob = new Blob([bindata]);
	let url = URL.createObjectURL(blob);
	downloadLink.href = url;
	downloadLink.download = cfn;

	//download
	document.body.appendChild(downloadLink);
	downloadLink.click();
	document.body.removeChild(downloadLink);

}


function alertDialog(json) {
    //原ajaxSubmit.js的alertDialog
    
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
            if(json.status!='error')
                location.reload();
    });
}


function alertok(msg){
    //alertDialog顯示ok訊息, 需引用utils/dialog.html

    let json={};
    json.status='success';
    json.message=msg;
    alertDialog(json);
}


function alerterr(msg){
    //alertDialog顯示error訊息, 需引用utils/dialog.html

    let json={};
    json.status='error';
    json.message=msg;
    alertDialog(json);
}


function aj_post(url, transferData){
    //ajax get

    return $.ajax({
        url:url,
        type: "POST",
        data: transferData,
        beforeSend:function(jqXHR, settings){
            let csrf=$('input[name=csrfmiddlewaretoken]').val();
            jqXHR.setRequestHeader('X-CSRFToken', csrf);
            jqXHR.setRequestHeader("X-Requested-With", "XMLHttpRequest")
        }
    });
}


function aj_binary(url, transferData, f){
    //console.log(url)
    
    return $.ajax({
        url:url,
        type: "POST",
        data: transferData,
        dataType: "binary",
        beforeSend:function(jqXHR, settings){
            let csrf=$('input[name=csrfmiddlewaretoken]').val();
            jqXHR.setRequestHeader('X-CSRFToken', csrf);
            jqXHR.setRequestHeader("X-Requested-With", "XMLHttpRequest")
        },
        success: function(bdata,status,xhr){
            //console.log(bdata);

            if(bdata.type==='application/octet-stream'){
                let filename=getdisposition(xhr);
                downloadfile(filename, bdata);
            }
            else{
                generalalerterror('密碼錯誤或準備文件失敗');
            }

        },
        error:function(xhr,errmsg,err){
            generalalerterror(xhr.responseText);
        }
    });
}
