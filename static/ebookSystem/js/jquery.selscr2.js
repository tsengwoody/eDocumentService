'use strict';
//需綁jquery與jquery.pp
//呂昱達(2017/08/01)


//全域變數紀錄目前查詢位置
let gvselscr = {
    tar: '',
    //find: '',
    iselect: -1, //目前找到符合者指標
};


function selscr_find(idtar, cdir) {


    //selector
    let selector =$("#"+idtar).contents().find('body'); //iframe -> body

    if (gvselscr.tar !== idtar) { // || gvselscr.find !== cfind

        //重新設定
        gvselscr.tar = idtar;
        //gvselscr.find = cfind;
        gvselscr.iselect = -1;

    }


    function selscr_selandscroll(obj) {

        //select
        obj.range().select();

        //dtop, top為螢幕位置，故需再把第一個元素top考慮進來
        let dtop = selector.children().eq(0).offset().top;

        //scrollTop
        selector.animate({
            scrollTop: obj.offset().top - dtop
        }, 300);

    }


    //removeClass selmatch
    selector.find('.selmatch').removeClass('selmatch');


    //針對下列四種標記搜尋
    //class="unknown"
    //class="mathml"
    //alt = "this is a picture"
    //<p>|----------|</p >
    selector.find('span[class="unknown"], span[class="mathml"], img[alt="this is a picture"], p:contains("|----------|")').addClass('selmatch');


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
