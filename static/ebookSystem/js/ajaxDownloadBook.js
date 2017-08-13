function downloadbook(me, ebook, action){
    //書庫頁面之下載按鈕

    //me
    me=$(me)

    //dw
    function dw(){

        //ISBN
        let ISBN=me.attr('ISBN');

        //password
        let password=$('#modal_downloadbook_inp_password').val();

        //transferData
        let transferData={
            // download:ISBN,
            action:action,
            password:password,
        };

        //url
        let url='';
        if(ebook===false){
            url='/ebookSystem/book_download/'+ISBN;
        }
        else{
            url='/ebookSystem/ebook_download/'+ISBN;
        }
        
        //generalajax
        generalajax(url, transferData);

        //clear
        $('#modal_downloadbook_inp_password').val('');

        //show
        $('#modal_downloadbook').modal('hide');

    }

    //click
    $('#modal_downloadbook_btn_submit').off().on('click', dw);

    //enter
    $("#modal_downloadbook_inp_password").off().on('keypress',function(e){
        code = (e.keyCode ? e.keyCode : e.which);
        if (code === 13){
            e.preventDefault();
            dw();
        }
    });

    //show
    $('#modal_downloadbook').modal('show');

}


function generalalerterror(msg){
    let json={};
    json.status='error';
    json.message=msg;
    alertDialog(json);
}


function getdisposition(xhr){
    let filename='';
    let disposition = xhr.getResponseHeader('Content-Disposition');
    if (disposition && disposition.indexOf('attachment') !== -1) {
        let filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
        let matches = filenameRegex.exec(disposition);
        if (matches != null && matches[1]) {
            filename = matches[1].replace(/['"]/g, '');
        }
    }
    return filename;
}


function generalajax(url, transferData){
    console.log(url)
    $.ajax({
        //url:".",
        url:url,
        type: "POST",
        data: transferData,
        dataType: "binary",
        beforeSend:function(jqXHR, settings){
            let csrf=$('input[name=csrfmiddlewaretoken]').val();
            //onsole.log(csrf)

            jqXHR.setRequestHeader('X-CSRFToken', csrf);

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
