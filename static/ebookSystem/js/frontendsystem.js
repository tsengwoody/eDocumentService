'use strict';


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


function urlparam() {
    //解析網址參數

    //url
    let url = location.search;

    //ar
    let ar = {};
    if (url.indexOf("?") != -1) {
        var param = url.split("?");
        var data = param[1].split("&");
        for (let i = 0; i < data.length; i++) {
            var s = data[i].split("=");
            ar[s[0]] = s[1];
        }
    }
    
    return ar;
}


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


function replace(c, t, r) {
    //取代字串
   
    let o = new RegExp(t, 'g');
    let rr = String(c).replace(o, r);

    return rr;
}


function strleft(c, n) {
    //取字串左邊n個字元
    return c.substr(0, n);
}


function strright(c, n) {
    //取字串右邊n個字元
    return c.substr(c.length - n, n);
}


function strmid(c, s, n) {
    //取字串中位置s開始後n個字元
    return c.substring((s - 1), (s + n - 1));
}


function strdelleft(c, n) {
    //刪除字串左邊n個字元
    return strright(c, c.length - n);
}


function strdelright(c, n) {
    //刪除字串右邊n個字元
    return strleft(c, c.length - n);
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


function arr2dict(v){
    //陣列轉字典物件

    let keys=_.take(v)[0];
    let d=_.tail(v);
    let r=[];
    _.each(d,function(v){
        let rr={};
        _.each(keys,function(k,i){
            rr[k]=v[i];
        })
        r.push(rr);
    })
    return r;
}


function arrarymerge(ar1,ar2,key){
    //合併物件陣列

    //ts
    let t1=_.map(ar1,key);
    let t2=_.map(ar2,key);
    let ts=_.flatten([t1,t2]);
    ts=_.uniq(ts);

    //each
    let ar=[];
    _.each(ts,function(tar){

        //f
        let f={};
        f[key]=tar;

        //r1,r2
        let r1=_.find(ar1,f);
        let r2=_.find(ar2,f);

        //merge
        let r=_.merge(r1, r2);

        //push
        ar.push(r);

    })

    return ar;
}


function base642bin(c){
    //base64字串轉binary

    return base64js.toByteArray(c);
}


function bin2base64(b){
    //binary轉base64字串

    return base64js.fromByteArray(b);
}


function bs2barr(bs) {
    //Binary String Array轉Binary Uint8 Array，應用於input file使用readAsBinaryString讀檔之資料

    let n = bs.length;
    let arr = new Uint8Array(n);
    for (let i = 0; i < n; i++) {
        arr[i] = bs.charCodeAt(i);
    }
    return arr;
}


function readfile(me) {
    //讀取檔案

    //df
    let df = $.Deferred();

    //file
    let file = me.files[0];

    //name
    let name = file.name;

    //reader
    let reader = new FileReader();

    //onload
    reader.onload = function (event) {

        //bindata
        let bindata = event.target.result;

        //resolve
        df.resolve(bindata);

    };

    //readAsBinaryString
    reader.readAsBinaryString(file);

    return df;
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
    tab.addClass('table table-hover table-rwd').css({
        'margin':'10px 0px',
    });

    //thead
    let thead=tab.find('thead');
    thead.css({
        'background-color':'#eee',
    });

    //thead tr
    thead.find('tr').addClass('tr-only-hide');

    //tr border
    tab.find('tr').css({
        'border':'0px', //清除bs預設tr的border
        'border-bottom':'1px solid #ddd',
    });

    //ths
    let ths=tab.find('th');
    ths.css({
        'text-align':'center',
        'vertical-align':'top',
        'padding':'10px 0px',
        'border':'0px', //清除bs預設th的border
        'border-top':'1px solid #ddd',
    });

    //tds
    let tds=tab.find('td');
    tds.css({
        'vertical-align':'top',
        'padding':'5px',
    });

    //vths
    let vths=[];
    ths.each(function(){
        let th=$(this);
        vths.push(th.text());
    })

    //tbody trs
    let trs=tab.find('tbody').find('tr');

    //td add data-th
    trs.each(function(){
        let tr=$(this);
        let tds=tr.find('td');
        _.each(vths,function(v,k){
            tds.eq(k).attr('data-th',v);
        })
    })

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
            tr.css('display',''); //透過tr的class來決定display，使能支援rwd class
            //tr.show();
        }
        else{
            tr.hide();
        }
    })

}


function dtarrsortkeys(dtarr,keys){
    //重排取物件陣列keys

    let r=[];
    _.each(dtarr,function(v,k){
        let o={};
        _.each(keys,function(kk){
            o[kk]=v[kk];
        })
        r.push(o);
    })
    return r;
}


function gentable(divid,tabid,ar){
    //於div內由資料ar快速產生有樣式與具分頁功能的table

    //dict2grid
    let h=dict2grid(ar,tabid);

    //table html
    $('#'+divid).html(h);

    //table style
    grid2bstable(tabid);

    //pagin
    pagin(tabid);

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
        },
    })
    .done(function(data){

        if(data['status']==='success'){
            //console.log('resolve',data)
            df.resolve(data);
        }
        else if(data['status']==='error'){
            //console.log('reject',data)
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
            c//onsole.log('reject',res)
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
        //console.log('reject',res)
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


function aj_booklist_dict(key2head,k){
    let o={
        'ISBN':'ISBN',
        'bookname':'書名',
        'bookbinding':'裝訂冊數',
        'order':'版次',
        'author':'作者',
        'house':'出版社',
        'date':'出版日期',
        'chinese_book_category':'中文圖書分類號',
        'source':'來源',
    };
    let p={
        'ISBN':'ISBN',
        '書名':'bookname',
        '裝訂冊數':'bookbinding',
        '版次':'order',
        '作者':'author',
        '出版社':'house',
        '出版日期':'date',
        '中文圖書分類號':'chinese_book_category',
        '來源':'source',
    };

    let q;
    if(key2head){
        q=o;
    }
    else{
        q=p;
    }

    if(haskey(q,k)){
        return q[k];
    }
    else{
        return k
    }

}


function aj_booklist_dict_array(ar,key2head){

    function forobj(o){
        let r={};
        _.each(o,function(vv,kk){
            let knew=aj_booklist_dict(key2head,kk);
            r[knew]=vv;
        })
        return r;
    }

    let r=[];
    _.each(ar,function(vv,kk){
        r.push(forobj(vv));
    })

    return r;
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

// let r=[{"ISBN":"9789869534239","書名":"新手媽媽的育兒療癒科學: 面對產後憂鬱、不安與孤獨、嬰兒夜哭、反抗期、夫妻失和等問題,用科學事實來建立妳的輕鬆教養術!","作者":"NHK特別採訪小組著; 張佩瑩譯","出版社":"大家","出版日期":"2017-11-01","裝訂方式":"平裝","圖書類號":"428","版次":"初版","來源":"NCL"},{"ISBN":"9789574350605","書名":"新手媽媽坐月子到宅服務創新方案規劃與執行","作者":"杜佩紋著","出版社":"杜佩紋","出版日期":"2017-10-01","裝訂方式":"平裝","圖書類號":"429","版次":"","來源":"NCL"},{"ISBN":"9789869359382","書名":"新手媽媽哺乳親餵的24堂課","作者":"Jack Newman, Teresa Pitman作; 葉織茵、劉宜佳、鄭勝得翻譯","出版社":"臺灣愛思唯爾","出版日期":"2017-06-01","裝訂方式":"平裝","圖書類號":"428","版次":"初版","來源":"NCL"},{"ISBN":"9789865786731","書名":"第一胎照書養!新手媽媽的第一本懷孕手冊","作者":"陳艾竹編","出版社":"維他命文化","出版日期":"2016-11-01","裝訂方式":"平裝","圖書類號":"429","版次":"初版","來源":"NCL"},{"ISBN":"9789869237673","書名":"新手媽媽必備的第1本DVD寶寶按摩指南","作者":"小谷博子監修; 沙子芳譯","出版社":"睿其書房","出版日期":"2016-02-01","裝訂方式":"平裝附數位影音光碟","圖書類號":"428","版次":"初版","來源":"NCL"},{"ISBN":"9789866062582","書名":"嬰兒副食品聖經: 新手媽媽必學205道副食品食譜","作者":"趙小英著; 李靜宜譯","出版社":"橘子文化","出版日期":"2013-10-01","裝訂方式":"平裝","圖書類號":"428","版次":"初版","來源":"NCL"},{"ISBN":"9789868932197","書名":"好孕一點都不難:  解決新手媽媽困擾的實踐全書","作者":"池下育子等監修","出版社":"方舟文化","出版日期":"2013-09-01","裝訂方式":"平裝","圖書類號":"429","版次":"初版","來源":"NCL"},{"ISBN":"9789868889682","書名":"新手媽媽一試就成功: 寶寶食譜全圖解","作者":"鍾毓珊著","出版社":"幸福文化","出版日期":"2013-05-01","裝訂方式":"平裝","圖書類號":"428","版次":"初版","來源":"NCL"},{"ISBN":"9789868905573","書名":"幹嘛要有小孩?: 一位新手媽媽的真實告白","作者":"潔西卡.瓦蘭提作; 陳品秀譯","出版社":"行人文化實驗室","出版日期":"2013-05-01","裝訂方式":"平裝","圖書類號":"544","版次":"初版","來源":"NCL"},{"ISBN":"9789575659684","書名":"餵母乳 不煩惱!新手媽媽看這裡就對了!","作者":"赤すぐ編輯部文字; 統一翻譯社翻譯","出版社":"臺視文化","出版日期":"2013-03-01","裝訂方式":"平裝","圖書類號":"428","版次":"初版","來源":"NCL"},{"ISBN":"9789868892613","書名":"寶寶出生關鍵100天照顧秘笈: 小兒名醫與10位新手媽媽的對談","作者":"陳素華總編輯","出版社":"聲活工坊文化","出版日期":"2013-01-01","裝訂方式":"平裝附光碟片","圖書類號":"","版次":"","來源":"NCL"},{"ISBN":"9789863012276","書名":"新手媽媽一定要學的哺乳經(簡體字版)","作者":"磊立同行著","出版社":"大眾國際書局","出版日期":"2012-12-01","裝訂方式":"平裝","圖書類號":"","版次":"","來源":"NCL"},{"ISBN":"9789866247521","書名":"新手媽媽一定要學的哺乳經","作者":"磊立同行著","出版社":"養沛文化館","出版日期":"2012-08-01","裝訂方式":"平裝","圖書類號":"428","版次":"初版","來源":"NCL"},{"ISBN":"9789866701344","書名":"為什麼媽媽需要粉紅色手提包?: 新手媽媽的優雅生活","作者":"史黛芬妮.施奈德(Stephanie Schneider)著; 謝靜怡譯","出版社":"飛寶國際文化","出版日期":"2009-11-01","裝訂方式":"精裝","圖書類號":"192","版次":"初版","來源":"NCL"},{"ISBN":"9789868171985","書名":"新手媽媽的第一本書: 胎教","作者":"沈靜作","出版社":"喜樂亞","出版日期":"2006-08-01","裝訂方式":"平裝附光碟片","圖書類號":"429","版次":"一版","來源":"NCL"},{"ISBN":"9789861610504","書名":"第一次當媽媽就上手: 新手媽媽完全生活指南","作者":"Debra Glibert Rosenberg, Mary Susan Miller合著; 李明芝譯","出版社":"信誼基金","出版日期":"2005-06-01","裝訂方式":"平裝","圖書類號":"544","版次":"初版","來源":"NCL"},{"ISBN":"9789572965818","書名":"新手媽媽的280天","作者":"石芳瑜著","出版社":"華谷文化","出版日期":"2004-06-01","裝訂方式":"平裝","圖書類號":"429","版次":"初版","來源":"NCL"},{"ISBN":"9789572897713","書名":"新手媽媽育兒寶典","作者":"周晴芸編著","出版社":"咖啡田文化館","出版日期":"2003-10-01","裝訂方式":"平裝","圖書類號":"428","版次":"初版","來源":"NCL"},{"ISBN":"9789576488641","書名":"新手媽媽必讀手冊","作者":"塚田一郎著; 盛勤譯","出版社":"書泉","出版日期":"2001-08-01","裝訂方式":"平裝","圖書類號":"429","版次":"初版","來源":"NCL"},{"ISBN":"9789578253711","書名":"新手媽媽百科","作者":"嬰兒與母親編輯部編著","出版社":"婦幼家庭","出版日期":"2001-05-01","裝訂方式":"平裝","圖書類號":"","版次":"1版","來源":"NCL"},{"ISBN":"9789578253568","書名":"新手媽媽","作者":"嬰兒與母親編輯部編著","出版社":"婦幼家庭","出版日期":"2000-12-01","裝訂方式":"平裝","圖書類號":"429","版次":"1版","來源":"NCL"},{"ISBN":"9789578253063","書名":"新手媽媽育嬰指南","作者":"嬰兒與母親雜誌社編輯部撰文","出版社":"婦幼家庭","出版日期":"1999-01-01","裝訂方式":"平裝","圖書類號":"428","版次":"1版","來源":"NCL"},{"ISBN":"9789578456778","書名":"新手媽媽育兒經","作者":"張震山作","出版社":"藝賞圖書","出版日期":"1998-11-01","裝訂方式":"平裝","圖書類號":"","版次":"初版","來源":"NCL"}];
// df.resolve(r);
// return df;

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
        console.log('aj_isbnnet done',data)
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
        console.log('aj_douban done',data)
        d_douban=data;
    })
    .fail(function(data){
        console.log('aj_douban fail',data)
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


function aj_borrowbook(me,action){
    //使用library_action API進行借還閱

    //df
    //let df = $.Deferred();

    //me
    me=$(me);

    //transferData
    let transferData={
        'action':action,
    };

    //url
    let url='/ebookSystem/library_action'; //不能於最後有反斜線
    if(action==='check_out'){
        transferData['ISBN']=me.attr('ISBN');
    }
    else if(action==='check_in'){
        transferData['id']=me.attr('id');
    }
    else{
        //df.reject({'status':'error','message':' mode error'});
        //return df;
    }

    //aj_post
    aj_post(url, transferData)
    .done(function(data){
        alertmessage(data.status, data.message)
        .done(function(){
            if(action==='check_in'){
                location.reload(); //歸還需重新載入網頁以更新資訊
            }
        });
        //df.resolve(data);
    })
    .fail(function(data){
        alertmessage(data.status, data.message);
        //df.reject(data);
    })

    //return df;
}


function aj_user_dict(){
    //user API key轉換資訊
    let d={
        'birthday':'生日',
        'education':'教育',
        'email':'郵件',
        'org':'單位',
        'phone':'手機',
        'username':'使用者名稱',
        'name':'姓名', //'first_name'+'last_name'
        'is_book':'訂閱訊息',
        'auth_email':'驗證電子郵件',
        'auth_phone':'驗證手機',
        'is_active':'登錄權限',
        'is_editor':'校對權限',
        'is_guest':'來賓權限',
    };
    return d;
}


function aj_user_key2head(key){
    //user API的key轉中文
    let d=aj_user_dict();
    if(haskey(d,key)){
        return d[key];
    }
    return key;
}


function aj_user_head2key(head){
    //user API的中文轉key
    let d=aj_user_dict();
    d=_.invert(d);
    if(haskey(d,head)){
        return d[head];
    }
    return head;
}


function aj_user_key2head_array(ar){
    //陣列物件key轉中文

    //r
    let r=[];
    _.each(ar,function(v,k){
            
        //add name
        if(haskey(v,'first_name') && haskey(v,'last_name')){
            v['name']=v['first_name']+v['last_name'];
        }

        //newkey
        let o={};
        _.each(v,function(value,key){
            let newkey=aj_user_key2head(key);
            o[newkey]=value;
        })

        //push
        r.push(o);

    })

    return r;
}


function aj_user_head2key_array(ar){
    //陣列物件中文轉key

    //r
    let r=[];
    _.each(ar,function(v,k){
            
        //newkey
        let o={};
        _.each(v,function(value,key){
            let newkey=aj_user_head2key(key);
            o[newkey]=value;
        })

        //push
        r.push(o);

    })

    return r;
}


function aj_user_querylist_combine(){
    //使用API user_list結合info,role取得使用者資訊

    //df
    let df = $.Deferred();

    //when
    $.when(aj_user_querylist('info'),aj_user_querylist('role'))
    .done(function(ar1,ar2){

        //arrarymerge
        let ar=arrarymerge(ar1,ar2,'id');

        //resolve
        df.resolve(ar);

    })
    .fail(function(msg){
        //reject
        df.reject(msg);
    })

    return df;
}


function aj_user_querylist(action){
    //使用API user_list

    //df
    let df = $.Deferred();

    //url
    let url='/genericUser/user_list/';

    //transferData
    let transferData={
        'query_field':'all',
        'query_value':'',
        'action':action,
    };

    //aj_get
    aj_get(url, transferData)
    .done(function(data){

        //ar
        let ar=aj_user_key2head_array(data['content']);

        //resolve
        df.resolve(ar);

    })
    .fail(function(data){
        df.reject(data['message']);
    })

    return df;
}


function aj_user_queryid(id,action){
    //使用API user_view

    //df
    let df = $.Deferred();

    //url
    let url='/genericUser/user_view/'+id+'/';

    //transferData
    let transferData={
        'action':action,
    };

    //aj_get
    aj_get(url, transferData)
    .done(function(data){
        
        //d
        let d=[data['content']];
        //console.log(d)

        //ar
        let ar=aj_user_key2head_array(d);
        
        //resolve
        df.resolve(ar);

    })
    .fail(function(data){
        df.reject(data['message']);
    })

    return df;
}


function aj_user_updateid(id,action,transferData){
    //使用API user_update

    //df
    let df = $.Deferred();
    
    //url
    let url='/genericUser/user_update/'+id+'/';

    //transferData
    transferData['action']=action;

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


function aj_booksetpriority(password,ISBN,priority){
    //使用API book_action

    //df
    let df = $.Deferred();
    
    //url
    let url='/ebookSystem/book_action/';

    //transferData
    let transferData={
        'action':'set_priority',
        'ISBN':ISBN,
        'password':password,
        'priority':priority,
    };

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


function aj_bookdeleterepository(password,ISBN){
    //使用API book_delete

    //df
    let df = $.Deferred();
    
    //url
    let url='/ebookSystem/book_delete/';

    //transferData
    let transferData={
        'ISBN':ISBN,
        'password':password,
    };

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

