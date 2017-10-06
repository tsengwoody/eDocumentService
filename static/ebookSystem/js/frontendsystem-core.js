// let comploader={}; //全域組件載入紀錄


// function inicomp(name){
//     //初始化組件
//     let df = $.Deferred();

//     //infor
//     let o=inicomp_getinfor(name);

//     //pre
//     let dfs=[];
//     if(o['pre'].length>0){
//         for(let c of o['pre']){
//             let s=inicomp(c);
//             dfs.push(s);
//         }
//     }

//     //each
//     Promise.all(dfs)
//     .then(function(){

//         //core
//         return inicomp_load(name);

//     })
//     .then(function(){
//         df.resolve();
//     })

//     return df;
// }


// function inicomp_load(name){
//     //載入組件
//     let df = $.Deferred();

//     if(haskey(comploader,name)){
//         df.resolve();
//     }
//     else{
//         let o=inicomp_getinfor(name);
//         let timetag='?'+Date.now();

//         if(o['type']==='js'){
//             $.getScript(o['url']+timetag)
//             .done(function(){
//                 console.log('load: '+name+'['+o['type']+']')

//                 //true
//                 comploader[name]=true;

//                 df.resolve();
//             })
//         }
//         else if(o['type']==='html'){
//             $.get(o['url']+timetag)
//             .done(function(h){
//                 console.log('load: '+name+'['+o['type']+']')

//                 //append
//                 $('body').append(h);

//                 //true
//                 comploader[name]=true;

//                 df.resolve();
//             })
//         }

//     }

//     return df;
// }


// function inicomp_getinfor(name){
//     //取得組件資訊

//     let o;
//     if(name==='tinymce'){
//         o={
//             'url':'https://cdnjs.cloudflare.com/ajax/libs/tinymce/4.6.6/tinymce.min.js',
//             'type':'js',
//             'pre':[]
//         }
//     }
//     else if(name==='wiriseditor'){
//         o={
//             'url':'/static/ebookSystem/js/wiriseditor/wiriseditor.js',
//             'type':'js',
//             'pre':[]
//         }
//     }
//     else if(name==='mathjax'){
//         o={
//             'url':'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_SVG', //總套件62.9mb太大，直接用cdn
//             'type':'js',
//             'pre':[]
//         }
//     }
//     else if(name==='mxeditor'){
//         o={
//             'url':'/static/ebookSystem/comp/mxeditor.html',
//             'type':'html',
//             'pre':['tinymce','wiriseditor','mathjax']
//         }
//     }
//     else if(name==='mxdownloadbook'){
//         o={
//             'url':'/static/ebookSystem/comp/mxdownloadbook.html',
//             'type':'html',
//             'pre':[]
//         }
//     }

//     return o;
// }


function cint(v) {
    //轉整數

    if ($.isNumeric(v)) {
        return _.round(v);
    }

    return 0;
}


function cstr(v) {
    //轉字串

    if(iser(v)){
        return '';
    }
    return String(v);
}


function cstrtrim(v){
    //轉字串並刪除前後空白

    return String(v).trim();
}


function isundefined(v) {
    //判斷是否為undefined

    let c = Object.prototype.toString.call(v);
    return c === '[object Undefined]';
}


function isnull(v) {
    //判斷是否為null

    let c = Object.prototype.toString.call(v);
    return c === '[object Null]';
}


function isempty(v) {
    //判斷是否為空物件

    if (isobj(v)) {
        for (let k in v) {
            return false;
        }
        return true;
    }
    return false;
}


function iszerolength(v) {
    //判斷是否為無內容陣列

    if (isarr(v)) {
        if (v.length === 0) {
            return true;
        }
        return false;
    }
    return false;
}


function isnothing(v) {
    //判斷是否為空字串

    if (v === '') {
        return true;
    }
    return false;
}


function iser(v) {
    //判斷是否為泛用無效

    if (isundefined(v)) {
        return true;
    }
    if (isnull(v)) {
        return true;
    }
    if (isempty(v)) {
        return true;
    }
    if (isnothing(v)) {
        return true;
    }
    if (iszerolength(v)) {
        return true;
    }
    return false;
}


function isarrer(ar){
    //陣列元素是否皆為iser

    return _.every(ar, function(v){
        return iser(v);
    })
}


function isobjvalueer(obj){
    //字典物件內值是否皆為iser

    return _.every(_.values(obj), function(v){
        return iser(v);
    })
}



function iselmexist(id) {
    //判斷元素是否存在

    return !(document.getElementById(id) === null);
}


function iscontainaz09(c) {
    //判斷字串是否包含英文與數字

    let reg = /^[A-Za-z0-9]+$/;
    return reg.test(c);
}


function isarr(v) {
    //判斷是否為陣列

    let c = Object.prototype.toString.call(v);
    return c === '[object Array]';
}


function isfun(v) {
    //判斷是否為函數

    let c = Object.prototype.toString.call(v);
    return c === '[object Function]';
}


function isnum(v) {
    //判斷是否為數字

    return $.isNumeric(v);
}


function isstr(v) {
    //判斷是否為字串

    let c = Object.prototype.toString.call(v);
    return c === '[object String]';
}


function isobj(v) {
    //判斷是否為物件

    let c = Object.prototype.toString.call(v);
    return c === '[object Object]';
}


function binstr(s, ins) {
    //判斷字串s是否「包含、出現」任一字串陣列ins內元素

    if (!isstr(s)){
        return false;
    }

    //instr
    function instr(s, ins) {
        return s.indexOf(ins);
    }

    //不是陣列則自動轉陣列
    if (!isarr(ins)) {
        ins = [ins];
    }

    //判斷是否包含ins元素
    for (let k in ins) {
        let v = ins[k];
        if (instr(s, v) !== -1) {
            return true;
        }
    }

    return false;
}


function arrhas(ltar, ltcontain) {
    //判斷任一字串陣列ltar內元素，是否「等於」任一字串陣列ltcontain內元素

    //不是陣列則自動轉陣列
    if (isstr(ltar)) {
        ltar = [ltar];
    }
    else if (isarr(ltar)) {
        //預設輸入陣列
    }
    else {
        return false;
    }

    //不是陣列則自動轉陣列
    if (isstr(ltcontain)) {
        ltcontain = [ltcontain];
    }
    else if (isarr(ltcontain)) {
        //預設輸入陣列
    }
    else {
        return false;
    }

    //由ltar各元素當中，若存在ltcontain內任一元素則回傳true，反之回傳false
    for (let i = 0; i < ltar.length; i++) {
        for (let j = 0; j < ltcontain.length; j++) {
            if (ltar[i] === ltcontain[j]) {
                return true;
            }
        }
    }
    return false;
}


function haskey(obj, key) {
    //判斷物件是否有key屬性

    if (!isobj(obj)) {
        return false;
    }
    return (key in obj);
}


function prt(o){
    console.log(o2j(o));
}


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


function blob2str(bdata){
    //blob轉字串

    //df
    let df = $.Deferred();

    //reader
    let reader = new FileReader();

    //loadend
    reader.addEventListener('loadend',function(event){

        //result
        let text=event.target.result; //srcElement非標準屬性格式, 需改target

        //resolve
        df.resolve(text);

    });

    //readAsText
    reader.readAsText(bdata);

    return df;
}


function GenID() {
    return Math.uuid(32);
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
    //原ajaxSubmit.js的alertDialog, 強制轉用alertmessage

    //alertmessage
    alertmessage(json.status, json.message)
    .done(function(){
        if(haskey(json,'redirect_to')){

            //redirect
            window.location.href = json.redirect_to; 

        }
        else if(json.status!='error'){

            //reload
            location.reload();

        }
    })

}


function keyspace2enter(event,me){
    //空白space鍵轉click, 因瀏覽器中nvda使用space點擊無法觸發完整click事件
    //console.log(event.keyCode)
    if(event.keyCode===32){
        $(me).click();
    }
}


function dict2grid(ar,tabid){
    //字典陣列轉出基本table

    //head
    let head=ar[0];
    head=_.keys(head);

    //c
    let c='';
    c+='<table id="'+tabid+'">';
    c+='<thead>';
    _.each(head,function(key){
        c+='<th>'+key+'</th>';
    })
    c+='</thead>';
    c+='<tbody>';
    _.each(ar,function(v,k){
        c+='<tr>';
        _.each(head,function(key){
            c+='<td>'+v[key]+'</td>';
        })
        c+='</tr>';
    })
    c+='</tbody>';
    c+='</table>';

    return c;
}


function grid2bstable(tabid){
    //基本table賦予class與sytle

    //tab
    let tab=$('#'+tabid);

    //table
    tab.addClass('table table-striped table-hover').css({
        'margin':'10px 0px',
        //'white-space':'nowrap',
    });

    //thead
    tab.find('thead').css({
        'background-color':'#eee',
        'border-top':'2px solid #ddd',
    });

    //th
    tab.find('th').css({
        'text-align':'center',
        'vertical-align':'top',
        'padding':'10px 0px',
    });

    //td
    tab.find('td').css({
        'vertical-align':'top',
        'padding':'5px',
    });

}


function pagetab(data){
    //產生分頁頁籤

    let c='';
    c+='<ul class="nav nav-tabs">';

    //each li
    let li_active='active';
    let li_expanded='true';
    _.each(data,function(v,k){
        c+='<li class="'+li_active+'"><a onkeydown="keyspace2enter(event,this);" href="#'+v['id']+'" name="'+v['name']+'" prop="'+v['prop']+'" data-toggle="tab" aria-expanded="'+li_expanded+'">'+v['title']+'</a></li>';
        li_active='';
        li_expanded='false';
    })
    
    c+='</ul>';
	
    c+='<div class="tab-content">';

    //each div
    let div_active='active';
    _.each(data,function(v,k){
        c+='<div id="'+v['id']+'" class="tab-pane '+div_active+'" style="margin-top:20px;"></div>';
        div_active='';
    })
    
    c+='</div>';

    return c;
}


function pagetab_subtabfix(me){
    //修正多層分頁會於上層切換分頁時，導致次分頁aria-expanded都被改為ture，使nvda無法順利讀取

    //me
    me=$(me);

    //jid
    let jid=me.attr('href');

    //使用delay延遲強制變更aria-expanded屬性值
    _.delay(function(){
        $(jid).find('ul[class="nav nav-tabs"]').find('li').each(function(){
            let li=$(this);
            let expanded=li.hasClass('active');
            li.find('a').attr('aria-expanded',expanded);
        })
    },50)

}


function pagin(tabid){
    //添加表格分頁功能

    //tab
    let tab=$('#'+tabid);

    //trs
    let trs=tab.find('tbody').find('tr');

    //numrow
    let numrow=trs.length;

    //numperpage
    let numperpage=10;

    //check
    if(numrow<=numperpage){
        return;
    }

    //numpage
    let numpage=Math.ceil(numrow/numperpage);

    let c='';
    c+='<div style="text-align:center;">';
    c+='<ul id="'+tabid+'_pagination" class="pagination" style="margin:0px;" tabid="'+tabid+'" pagenow="1" numrow="'+numrow+'" numperpage="'+numperpage+'" numpage="'+numpage+'">';
    c+='<li class="prev" style="cursor:pointer;"><a onclick="pagin_change(\''+tabid+'\',\'-1\')">上一頁</a></li>';
    c+='<li class=""><a >1 / '+numpage+'</a></li>';
    c+='<li class="next" style="cursor:pointer;"><a onclick="pagin_change(\''+tabid+'\',\'+1\')">下一頁</a></li>';
    c+='</ul>';
    c+='</div>';
    
    //after
    tab.after(c);

    //change
    pagin_change(tabid,1)

}


function pagin_change(tabid,oper){
    //表格分頁切換

    let tab=$('#'+tabid);
    let pag=$('#'+tabid+'_pagination');
    let pagenow=cint(pag.attr('pagenow'));
    let numperpage=cint(pag.attr('numperpage'));
    let numpage=cint(pag.attr('numpage'));

    //pagenow
    if(String(oper)==='+1'){
        pagenow+=1;
    }
    else if(String(oper)==='-1'){
        pagenow-=1;
    }
    else{
        pagenow=cint(oper);
    }

    //check
    pagenow=Math.max(pagenow,1);
    pagenow=Math.min(pagenow,numpage);

    //save
    pag.attr('pagenow',pagenow);

    //show pagenow
    pag.find('li').eq(1).find('a').html(pagenow+' / '+numpage);

    //disabled li
    pag.find('li').removeClass('disabled');
    if(pagenow===1){
        pag.find('li').eq(0).addClass('disabled');
    }
    else if(pagenow===numpage){
        pag.find('li').eq(2).addClass('disabled');
    }

    //trs
    let trs=tab.find('tbody').find('tr');
    
    //each
    trs.each(function(i){
        let tr=$(this);
        let j=i+1;
        if( j >= numperpage*(pagenow-1)+1 && j <= numperpage*(pagenow)){
            tr.show();
        }
        else{
            tr.hide();
        }
    })

}


let gvselscr = {
    tar: '',
    iselect: -1, //目前找到符合者指標
};
function selscr_find(idtar, cdir) {
    //校對用移動至上下一個標記
    //需綁jquery-pp，並限定使用於當前頁


    //selector
    let selector =$("#"+idtar).contents().find('body'); //iframe -> body

    if (gvselscr.tar !== idtar) { 

        //重新設定
        gvselscr.tar = idtar;
        gvselscr.iselect = -1;

    }


    function selscr_selandscroll(obj) {

        //range select
        obj.range().select();

        //dtop, top為螢幕位置，故需再把第一個元素top考慮進來
        //let dtop = selector.children().eq(0).offset().top;

        //scrollTop
        selector.animate({
            //scrollTop: obj.offset().top - dtop,
            scrollTop: obj.offset().top,
        }, 300);

    }


    //removeClass selmatch
    selector.find('.selmatch').removeClass('selmatch');


    //針對下列四種標記搜尋
    //class="unknown"
    //class="mathml"
    //alt = "this is a picture"
    //<p>|----------|</p >
    selector.find('span.unknown, span.mathml, img[alt="this is a picture"], p:contains("|----------|")').addClass('selmatch');


    //selmatch
    let selmatch = selector.find('.selmatch');


    //cdir
    if (cdir === 'next') {
        gvselscr.iselect++;

        //超過next則取消
        if (gvselscr.iselect >= selmatch.length) {
            //gvselscr.iselect = selmatch.length - 1;
            //console.log("next找不到搜尋對象");
            gvselscr.iselect = 0;
        }

        //自動選擇
        selscr_selandscroll(selmatch.eq(gvselscr.iselect))

    }
    else if (cdir === 'previous') {
        gvselscr.iselect--;

        //超過previous則取消
        if (gvselscr.iselect < 0) {
            //gvselscr.iselect = 0;
            //console.log("previous找不到搜尋對象");
            gvselscr.iselect = selmatch.length - 1;
        }

        //自動選擇
        selscr_selandscroll(selmatch.eq(gvselscr.iselect))

    }
    else {
        console.log('cdir error : ' + cdir)
    }


}


function aj_get(url, transferData){
    //ajax get

    return aj_send('get', url, transferData);
}


function aj_post(url, transferData){
    //ajax post

    return aj_send('post', url, transferData);
}


function aj_delete(url, transferData){
    //ajax post

    return aj_send('delete', url, transferData);
}


function aj_send(type, url, transferData){
    //ajax傳送訊息

    //df
    let df = $.Deferred();

    //ajax
    $.ajax({
        url:url,
        type: type,
        data: transferData,
        beforeSend:function(jqXHR, settings){
            let csrf=$('input[name=csrfmiddlewaretoken]').val();
            jqXHR.setRequestHeader('X-CSRFToken', csrf);
            jqXHR.setRequestHeader("X-Requested-With", "XMLHttpRequest")
        }
    })
    .done(function(data){

        if(data['status']==='success'){
            df.resolve(data);
        }
        else if(data['status']==='error'){
            df.reject(data);
        }
        else{
            //console.log('aj_send: data.status error');
            //console.log(data);

            //reject
            let res={
                'status':'error',
                'message':'伺服器非預期回應: '+o2j(data),
            };
            df.reject(res);
        }

    })
    .fail(function(xhr){
        //console.log('aj_send: ajax error');
        //console.log(xhr);
        //console.log(xhr.responseText);

        //reject
        let res={
            'status':'error',
            'message':'伺服器錯誤回應: '+xhr.responseText,
        };
        df.reject(res);

    })

    return df;
}


function aj_binary(url, transferData){
    //ajax下載binary檔案

    //df
    let df = $.Deferred();

    //getdisposition
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

    //ajax
    $.ajax({
        url:url,
        type: "POST",
        data: transferData,
        dataType: "binary",
        beforeSend:function(jqXHR, settings){
            let csrf=$('input[name=csrfmiddlewaretoken]').val();
            jqXHR.setRequestHeader('X-CSRFToken', csrf);
            jqXHR.setRequestHeader("X-Requested-With", "XMLHttpRequest")
        }
    })
    .done(function(bdata,status,xhr){

        if(bdata.type==='application/octet-stream'){

            //downloadfile
            let filename=getdisposition(xhr);
            downloadfile(filename, bdata);

            //resolve
            let res={
                'status':'success',
                'message':'下載檔案成功',
            };
            df.resolve(res);

        }
        else{
            // console.log('aj_binary: bdata.type error');
            // console.log(bdata);
            // console.log(status);
            // console.log(xhr);

            //blob to string
            blob2str(bdata)
            .done(function(msg){

                //reject
                let res=j2o(msg); //為json訊息
                df.reject(res);

            })

        }

    })
    .fail(function(xhr){
        // console.log('aj_binary: ajax error');
        // console.log(xhr);
        // console.log(xhr.responseText); //會沒有responseText, 只好回傳xhr文字

        //reject
        let res={
            'status':'error',
            'message':'伺服器錯誤回應: '+o2j(xhr),
        };
        df.reject(res);

    })

    return df;
}


function aj_booklist(query_type, query_value){
    //API使用book_list查找書籍資訊

    //df
    let df = $.Deferred();

    //url
    let url='/ebookSystem/book_list'; //post會加「/」而get不會

    //transferData
    let transferData={
        'query_type':query_type,
        'query_value':query_value
    };

    //aj_get
    aj_get(url,transferData)
    .done(function(data){
        
        if(data['status']==='success'){

            //o
            let o=data['content']['book'];

            //p
            let p=[];
            _.each(o, function(v,k){
                p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
            })

            if(p.length>0){
                df.resolve(p);
            }
            else{
                df.reject('無書籍資料');
            }
        
        }
        else{
            //console.log(data['message']);
            df.reject('無書籍資料');
        }

    })
    .fail(function(msg){
        //console.log(msg)
        df.reject('無書籍資料');
    })
    
    return df;
}


function aj_isbnnet_ISBN(ISBN){
    //使用book_info API

    //df
    let df = $.Deferred();

    //transferData
    let transferData={
        'ISBN':ISBN,
        'source':'NCL',
    }

    //aj_send
    aj_send('POST', '/ebookSystem/book_info/'+ISBN+'/', transferData)
    .done(function(data){

        //message
        if(data.message==='查無資料'){

            //reject
            df.reject(data);

        }
        else{

            //book
            let book={
                'ISBN':cstr(data.ISBN),
                '書名':cstr(data.bookname),
                '作者':cstr(data.author),
                '出版社':cstr(data.house), 
                '出版日期':cstr(data.date),
                '裝訂方式':cstr(data.bookbinding),
                '圖書類號':cstr(data.chinese_book_category),
                '版次':cstr(data.order),
                '來源':cstr('NCL'),
            };

            //resolve
            df.resolve(book);
            
        }

    })
    .fail(function(data){

        //reject
        df.reject(data);

    })

    return df;
}


function aj_isbnnet(transferData){
    //查找[全國新書資訊網]書籍資訊

    return aj_querybooklist('NCL',transferData);
}


function aj_douban(value){
    //用value查找[豆瓣]書籍資訊

    let transferData={
        'search_query':value,
    };
    return aj_querybooklist('douban',transferData);
}


function aj_isbnnetanddouban_ISBN(ISBN){
    //用ISBN查找[全國新書資訊網]與[豆瓣]書籍資訊

    //df
    let df = $.Deferred();

    //df, d
    let df_isbnnet=$.Deferred();
    let df_douban=$.Deferred();
    let d_isbnnet=[];
    let d_douban=[];

    aj_isbnnet_ISBN(ISBN)
    .done(function(data){
        console.log('aj_isbnnet done ',data)
        d_isbnnet=[data]; //回傳為單一物件轉陣列

        //NCL優先，直接略過豆瓣查詢
        df_douban.resolve(); 

    })
    .fail(function(data){
        console.log('aj_isbnnet fail',data)
    })
    .always(function(){
        df_isbnnet.resolve();
    })

    //aj_douban
    aj_douban(ISBN)
    .done(function(data){
        console.log('aj_douban done ',data)
        d_douban=data;
    })
    .fail(function(data){
        console.log('aj_douban fail ',data)
    })
    .always(function(){
        df_douban.resolve();
    })

    //when
    $.when(df_isbnnet,df_douban)
    .done(function(){

        //r
        let r=[];
        _.each(d_isbnnet,function(v){
            r.push(v);
        })
        _.each(d_douban,function(v){
            r.push(v);
        })

        //no date
        if(r.length===0){

            //reject
            df.reject('無書籍資料');

        }
        else{

            //resolve
            df.resolve(r[0]); //只針對合併後第一本回傳，有NCL時，豆瓣會因回傳較慢被直接取消

        }

    })
   
    return df;
}


function aj_isbnnetanddouban(value){
    //用value查找[全國新書資訊網]與[豆瓣]書籍資訊

    //df
    let df = $.Deferred();

    //df, d
    let df_isbnnet=$.Deferred();
    let df_douban=$.Deferred();
    let d_isbnnet=[];
    let d_douban=[];

    //aj_isbnnet
    let transferData={
        'FO_SchRe1ation0':'Null',
        'FO_SearchField0':'Title',
        'FO_SearchValue0':value,
        'FO_SchRe1ation1':'OR',
        'FO_SearchField1':'ISBN',
        'FO_SearchValue1':value,
        'FO_SchRe1ation2':'AND',
        'FO_SearchField2':'',
        'FO_SearchValue2':'',
    };
    aj_isbnnet(transferData)
    .done(function(data){
        console.log('aj_isbnnet done ',data)
        d_isbnnet=data;
    })
    .fail(function(data){
        console.log('aj_isbnnet fail',data)
    })
    .always(function(){
        df_isbnnet.resolve();
    })

    //aj_douban
    aj_douban(value)
    .done(function(data){
        console.log('aj_douban done ',data)
        d_douban=data;
    })
    .fail(function(data){
        console.log('aj_douban fail ',data)
    })
    .always(function(){
        df_douban.resolve();
    })

    //when
    $.when(df_isbnnet,df_douban)
    .done(function(){

        //r
        let r=[];
        _.each(d_isbnnet,function(v){
            r.push(v);
        })
        _.each(d_douban,function(v){
            r.push(v);
        })

        //no date
        if(r.length===0){

            //reject
            df.reject('無書籍資料');

        }
        else{

            //resolve
            df.resolve(r);

        }

    })
   
    return df;
}


function aj_querybooklist(source,transferData){
    //使用get_book_info_list API

    //df
    let df = $.Deferred();

    //url
    let url='/ebookSystem/get_book_info_list/'; //post會加「/」而get不會

    //transferData
    // let transferData={
    //     'FO_SchRe1ation0':'Null',
    //     'FO_SearchField0':'Title',
    //     'FO_SearchValue0':'新手媽媽',
    //     'FO_SchRe1ation1':'AND',
    //     'FO_SearchField1':'',
    //     'FO_SearchValue1':'',
    //     'FO_SchRe1ation2':'AND',
    //     'FO_SearchField2':'',
    //     'FO_SearchValue2':'',
    // };
    transferData['source']=source;

    //aj_post
    aj_post(url,transferData)
    .done(function(data){
        //console.log(data)

        if(data['status']==='success'){

            //o
            let o=data['bookinfo_list'];

            //p
            let p=[];
            _.each(o, function(v,k){
                let r={
                    // 'ISBN':v[0],
                    // 'bookname':v[1], //書名
                    // 'author':v[2], //作者
                    // 'house':v[3], //出版社/出版機構
                    // 'date':v[4], //出版日期
                    // 'bookbinding':v[5], //裝訂冊數/裝訂方式
                    // 'classnumber':v[6], //圖書類號
                    // 'order':v[7], //版次/出版版次	
                    'ISBN':cstr(v[0]),
                    '書名':cstr(v[1]),
                    '作者':cstr(v[2]),
                    '出版社':cstr(v[3]), 
                    '出版日期':cstr(v[4]),
                    '裝訂方式':cstr(v[5]),
                    '圖書類號':cstr(v[6]),
                    '版次':cstr(v[7]),
                    '來源':cstr(source),
                };
                p.push(r);
            })

            if(p.length>0){
                df.resolve(p);
            }
            else{
                df.reject('無書籍資料');
            }
        
        }
        else{
            //console.log(data['message']);
            df.reject('無書籍資料');
        }

    })
    .fail(function(msg){
        //console.log(msg)
        df.reject('無書籍資料');
    })
    
    return df;
}

function aj_announcement(mode,aid,transferData){
    //公告API新增、更新、刪除

    //df
    let df = $.Deferred();

    //url
    let url;
    if(mode==='create'){
        //create不用給aid
        url='/genericUser/announcement_create'; //不能於最後有反斜線
    }
    else if(mode==='update'){
        url='/genericUser/announcement_update/'+aid+'/';
    }
    else if(mode==='delete'){
        url='/genericUser/announcement_delete/'+aid+'/';
    }
    else{

        //reject
        df.reject({'status':'error','message':' mode error'});
        
        return df;
    }
    
    //check
	let err=[];
    if(iser(transferData.title)){
        err.push('標題不能為空');
    }
    if(iser(transferData.category)){
        err.push('類別需選擇其中一種');
    }
    if(iser(transferData.content)){
        err.push('內容不能為空');
    }
    if(err.length>0){

        //msg
        let msg=_.chain(err)
        .map(function(v,k){
            return '<div style="margin-top:5px;">'+cstr(k+1)+': '+v+'</div>';
        })
        .join('')
        .value();
        msg='<div>輸入錯誤訊息如下：</div>'+msg;
        
        //reject
        df.reject({'status':'error','message':msg});

        return df;
    }

    //aj_post
    aj_post(url, transferData)
    .done(function(data){
        df.resolve(data);
    })
    .fail(function(data){
        df.reject(data);
    })

    return df;
}

