'use strict';

function urlparam() {
	//解析網址參數

	//url
	let url = location.search;

	//ar
	let ar = {};
	if (url.indexOf("?") != -1) {
		let param = url.split("?");
		let data = param[1].split("&");
		for (let i = 0; i < data.length; i++) {
			let s = data[i].split("=");
			ar[s[0]] = s[1];
		}
	}

	return ar;
}

function sep(c, t) {
	//將字串c使用t分割，並回傳非空字串結果s

	//check, 預設使用空白分割
	if (iser(t)) {
		t = ' ';
	}

	//split
	let s = c.split(t);

	//pull
	_.pull(s, '');

	return s;
}

function cint(v) {
	//轉整數

	if ($.isNumeric(v)) {
		return _.round(v);
	}

	return 0;
}

function cdbl(v) {
	//轉浮點數

	if ($.isNumeric(v)) {
		return _.toFinite(v);
	}

	return 0;
}

function cstr(v) {
	//轉字串

	if (iser(v)) {
		return '';
	}
	return String(v);
}

function cstrtrim(v) {
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

function isarrer(ar) {
	//陣列元素是否皆為iser

	return _.every(ar, function (v) {
		return iser(v);
	})
}

function isobjvalueer(obj) {
	//字典物件內值是否皆為iser

	return _.every(_.values(obj), function (v) {
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

	if (!isstr(s)) {
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

function prt(o) {
	console.log(o2j(o));
}

function o2j(v) {
	//物件轉json文字

	let c = '';
	try {
		//c = JSON.stringify(v);
		c = JSON.stringify(v, null, '\t');
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

function blob2str(bdata) {
	//blob轉字串

	//df
	let df = GenDF();

	//reader
	let reader = new FileReader();

	//loadend
	reader.addEventListener('loadend', function (event) {

		//result
		let text = event.target.result; //srcElement非標準屬性格式, 需改target

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

function GenDF() {
	return $.Deferred();;
}

function alertDialog(json) {
	//原ajaxSubmit.js的alertDialog, 強制轉用alertmessage

	//alertmessage
	alertmessage(json.status, json.message)
		.done(function () {
			if (haskey(json, 'redirect_to')) {

				//redirect
				window.location.href = json.redirect_to;

			}
			else if (json.status != 'error') {

				//reload
				location.reload();

			}
		})

}

function keyspace2enter(event, me) {
	//空白space鍵轉click, 因瀏覽器中nvda使用space點擊無法觸發完整click事件

	if (event.keyCode === 32) {
		$(me).click();
	}
}

function arr2dict(v) {
	//陣列轉字典物件

	let keys = _.take(v)[0];
	let d = _.tail(v);
	let r = [];
	_.each(d, function (v) {
		let rr = {};
		_.each(keys, function (k, i) {
			rr[k] = v[i];
		})
		r.push(rr);
	})
	return r;
}

function arrarymerge(ar1, ar2, key) {
	//合併物件陣列

	//ts
	let t1 = _.map(ar1, key);
	let t2 = _.map(ar2, key);
	let ts = _.flatten([t1, t2]);
	ts = _.uniq(ts);

	//each
	let ar = [];
	_.each(ts, function (tar) {

		//f
		let f = {};
		f[key] = tar;

		//r1,r2
		let r1 = _.find(ar1, f);
		let r2 = _.find(ar2, f);

		//merge
		let r = _.merge(r1, r2);

		//push
		ar.push(r);

	})

	return ar;
}

function dtarrsortkeys(dtarr, keys) {
	//重排取物件陣列keys

	let r = [];
	_.each(dtarr, function (v, k) {
		let o = {};
		_.each(keys, function (kk) {
			o[kk] = v[kk];
		})
		r.push(o);
	})
	return r;
}

function base642bin(c) {
	//base64字串轉binary

	return base64js.toByteArray(c);
}

function bin2base64(b) {
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

function downloadfile(cfn, bindata) {
	//下載binary資料成為檔案, 使用標籤a與blob物件直接將bindata下載成為檔案

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

function downloadtext(cfn, ccont) {
	//下載text資料成為utf-8檔案

	//tag a
	let a = document.createElement('a');
	let blob = new Blob(['\ufeff', ccont]);
	let url = URL.createObjectURL(blob);
	a.href = url;
	a.download = cfn;

	//download
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);

}

function readfile(me) {
	//讀取檔案

	//df
	let df = GenDF();

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

function trapfocus() {
	//trap focus

	let element = this;
	let namespace = element.attr('id');
	let focusableEls = element.find('a, object, :input, iframe, [tabindex]');
	let firstFocusableEl = focusableEls.first()[0];
	let lastFocusableEl = focusableEls.last()[0];
	let KEYCODE_TAB = 9;
	element.on('keydown.' + namespace, function (e) {
		let isTabPressed = (e.key === 'Tab' || e.keyCode === KEYCODE_TAB);

		if (!isTabPressed) {
			return;
		}

		if (e.shiftKey) {
			//shift + tab
			if (document.activeElement === firstFocusableEl) {
				lastFocusableEl.focus();
				e.preventDefault();
			}
		}
		else {
			//tab
			if (document.activeElement === lastFocusableEl) {
				firstFocusableEl.focus();
				e.preventDefault();
			}
		}

	});
}

function untrapfocus() {
	//un-trap focus

	let element = this;
	let namespace = element.attr('id');
	element.off('keydown.' + namespace);
}

(function ($) {
	//註冊trapfocus,untrapfocus
	$.fn.extend({
		trapfocus: trapfocus,
		untrapfocus: untrapfocus
	});
})(jQuery);

let modalinfors = [];
function lm_add(o) {

	//lastone
	let loso = null;
	let oy = null;
	let st = null;
	if (modalinfors.length > 0) {
		loso = _.last(modalinfors).selfobj;
		oy = loso.css('overflow-y');
		st = loso.scrollTop();
	}

	//r
	let r = {
		'selfobj': o,
		'lastone-selfobj': loso,
		'lastone-overflow-y': oy,
		'lastone-scroll-top': st,
	};

	//push
	modalinfors.push(r);

	//trapfocus
	_.delay(function () {
		o.trapfocus();
	}, 750)

}

function lm_minu() {


	//pop
	let ss = modalinfors.pop();

	//loso
	let loso = ss['lastone-selfobj'];
	if (loso !== null) {

		//hidden body overflow-y
		$('body').css('overflow-y', 'hidden');

		//overflow-y
		loso.css('overflow-y', ss['lastone-overflow-y']);

		//scroll-top
		_.delay(function () {

			//等視窗捲軸出現才恢復
			loso.scrollTop(ss['lastone-scroll-top'])

		}, 750)

	}
	else {

		//reset body overflow-y
		$('body').css('overflow-y', '');

	}

	//last
	if (modalinfors.length > 0) {

		//r
		let r = _.last(modalinfors);

		//trapfocus
		_.delay(function () {
			let selfobj = r['selfobj'];
			selfobj.trapfocus();
		}, 750)

	}

}

function dict2grid(ar, tabid) {
	//字典陣列轉出基本table

	//head

	let head = ar[0];
	head = _.keys(head);

	//c
	let c = '';
	c += '<table id="' + tabid + '">';
	c += '<thead>';
	_.each(head, function (key) {
		c += '<th>' + key + '</th>';
	})
	c += '</thead>';
	c += '<tbody>';
	_.each(ar, function (v, k) {
		c += '<tr>';
		_.each(head, function (key) {
			c += '<td>' + v[key] + '</td>';
		})
		c += '</tr>';
	})
	c += '</tbody>';
	c += '</table>';

	return c;
}

function grid2bstable(tabid) {
	//基本table賦予class與sytle

	//tab
	let tab = $('#' + tabid);

	//table
	tab.addClass('table table-hover table-rwd').css({
		'margin': '10px 0px',
	});

	//thead
	let thead = tab.find('thead');
	thead.css({
		'background-color': '#eee',
	});

	//thead tr
	thead.find('tr').addClass('tr-only-hide');

	//tr border
	tab.find('tr').css({
		'border': '0px', //清除bs預設tr的border
		'border-bottom': '1px solid #ddd',
	});

	//ths
	let ths = tab.find('th');
	ths.css({
		'text-align': 'center',
		'vertical-align': 'top',
		'padding': '10px 0px',
		'border': '0px', //清除bs預設th的border
		'border-top': '1px solid #ddd',
	});

	//tds
	let tds = tab.find('td');
	tds.css({
		'vertical-align': 'top',
		'padding': '5px',
	});

	//vths
	let vths = [];
	ths.each(function () {
		let th = $(this);
		vths.push(th.text());
	})

	//tbody trs
	let trs = tab.find('tbody').find('tr');

	//td add data-th
	trs.each(function () {
		let tr = $(this);
		let tds = tr.find('td');
		_.each(vths, function (v, k) {
			tds.eq(k).attr('data-th', v);
		})
	})

}

function pagetab(data) {
	//產生分頁頁籤

	let c = '';
	c += '<ul class="nav nav-tabs">';

	//each li
	let li_active = 'active';
	let li_expanded = 'true';
	_.each(data, function (v, k) {
		c += '<li class="' + li_active + '"><a onkeydown="keyspace2enter(event,this);" href="#' + v['id'] + '" name="' + v['name'] + '" prop="' + v['prop'] + '" data-toggle="tab" aria-expanded="' + li_expanded + '">' + v['title'] + '</a></li>';
		li_active = '';
		li_expanded = 'false';
	})

	c += '</ul>';

	c += '<div class="tab-content">';

	//each div
	let div_active = 'active';
	_.each(data, function (v, k) {
		c += '<div id="' + v['id'] + '" class="tab-pane ' + div_active + '" style="margin-top:20px;"></div>';
		div_active = '';
	})

	c += '</div>';

	return c;
}

function pagetab_subtabfix(me) {
	//修正多層分頁會於上層切換分頁時，導致次分頁aria-expanded都被改為ture，使nvda無法順利讀取

	//me
	me = $(me);

	//jid
	let jid = me.attr('href');

	//使用delay延遲強制變更aria-expanded屬性值
	_.delay(function () {
		$(jid).find('ul[class="nav nav-tabs"]').find('li').each(function () {
			let li = $(this);
			let expanded = li.hasClass('active');
			li.find('a').attr('aria-expanded', expanded);
		})
	}, 300)

}

let gvselscr = {
	tar: '',
	iselect: -1, //目前找到符合者指標
};
function selscr_find(idtar, cdir) {
	//校對用移動至上下一個標記
	//需綁jquery-pp，並限定使用於當前頁


	//selector
	let selector = $("#" + idtar).contents().find('html'); //iframe -> html, 各瀏覽器預設使用捲軸為html

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

		//自動切換至標記內指定圖片
		let pic = obj.attr('id');
		let sel = $('#scanPageList');
		sel.find('option[value="' + pic + '"]').prop('selected', true);
		sel.change();

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

function aj_getcsrf() {
	//csrf

	let csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
	let csrftoken = getCookie('csrftoken');
	return {
		'csrf': csrfmiddlewaretoken,
		'X-CSRFToken': csrftoken,
		'X-Requested-With': 'XMLHttpRequest',
	};
}

//sameOrigin
function sameOrigin(url) {
	// test that a given url is a same-origin URL, url could be relative or scheme relative or absolute
	let host = document.location.host; // host + port
	let protocol = document.location.protocol;
	let sr_origin = '//' + host;
	let origin = protocol + sr_origin;
	// Allow absolute or scheme relative URLs to same origin
	return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
		(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
		// or any other URL that isn't scheme relative or absolute i.e relative.
		!(/^(\/\/|http:|https:).*/.test(url));
}

//csrfSafeMethod
function csrfSafeMethod(method) {
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)); // these HTTP methods do not require CSRF protection
}

function aj_send(type, url, transferData) {
	//ajax傳送訊息

	//df
	let df = GenDF();

	//ajax
	$.ajax({
		url: url,
		type: type,
		data: transferData,
		//ata: JSON.stringify(transferData),
		//contentType: 'application/json', //default: 'application/x-www-form-urlencoded; charset=UTF-8'
		beforeSend: function (jqXHR, settings) {
			if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
				let g = aj_getcsrf();
				jqXHR.setRequestHeader('X-CSRFToken', g.csrf);
				jqXHR.setRequestHeader('X-Requested-With', g.XMLHttpRequest)
			}
		},
	})
		.done(function (data) {

			if (data['status'] === 'success') {
				//console.log('resolve',data)
				df.resolve(data);
			}
			else if (data['status'] === 'error') {
				//console.log('reject',data)
				df.reject(data);
			}
			else {
				//console.log('aj_send: data.status error');
				//console.log(data);

				//reject
				let res = {
					'status': 'error',
					'message': '伺服器非預期回應: ' + o2j(data),
				};
				//console.log('reject',res)
				df.reject(res);
			}

		})
		.fail(function (xhr) {
			//console.log('aj_send: ajax error');
			//console.log(xhr);
			//console.log(xhr.responseText);

			//reject
			let res = {
				'status': 'error',
				'message': '伺服器錯誤回應: ' + xhr.responseText,
			};
			//console.log('reject',res)
			df.reject(res);

		})

	return df;
}

function aj_disposition(xhr) {
	//由 Content-Disposition 取得 filename

	let filename = '';
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

function aj_text(url, transferData) {
	//ajax下載text檔案

	//df
	let df = GenDF();

	//ajax
	$.ajax({
		url: url,
		type: "GET",
		data: transferData,
		beforeSend: function (jqXHR, settings) {
			let csrf = $('input[name=csrfmiddlewaretoken]').val();
			jqXHR.setRequestHeader('X-CSRFToken', csrf);
			jqXHR.setRequestHeader("X-Requested-With", "XMLHttpRequest")
		}
	})
		.done(function (cdata, status, xhr) {
			// console.log('cdata', cdata);
			// console.log('status', status);
			// console.log('xhr', xhr);

			//downloadtext
			let filename = aj_disposition(xhr);
			downloadtext(filename, cdata);

			//resolve
			let res = {
				'status': 'success',
				'message': '下載檔案成功',
			};
			df.resolve(res);

		})
		.fail(function (xhr) {
			//console.log(xhr);

			//reject
			let res = {
				'status': 'error',
				'message': '伺服器錯誤回應: ' + o2j(xhr),
			};
			df.reject(res);

		})

	return df;
}

function aj_binary(url, transferData) {
	//ajax下載binary檔案

	//df
	let df = GenDF();

	//ajax
	$.ajax({
		url: url,
		type: "POST",
		data: transferData,
		dataType: "binary",
		beforeSend: function (jqXHR, settings) {
			let csrf = $('input[name=csrfmiddlewaretoken]').val();
			jqXHR.setRequestHeader('X-CSRFToken', csrf);
			jqXHR.setRequestHeader("X-Requested-With", "XMLHttpRequest")
		},
		'error': function (xhr) {
			//reject
			let res = {
				'status': 'error',
				'message': '伺服器錯誤回應: ' +xhr.status,
			};
			df.reject(res);
		},
		success: function(bdata, textStatus, xhr) {
			if (bdata.type === 'application/octet-stream') {

				//downloadfile
				let filename = aj_disposition(xhr);
				downloadfile(filename, bdata);

				//resolve
				let res = {
					'status': 'success',
					'message': '下載檔案成功',
				};
				df.resolve(res);

			}
			else {

				//blob to string
				blob2str(bdata)
					.done(function (msg) {

						//reject
						let res = j2o(msg); //為json訊息
						df.reject(res);

					})

			}
		},
	})

	return df;
}

function aj_booklist_dict(key2head, k) {
	//書籍中英鍵值轉換

	let o = {
		'ISBN': 'ISBN',
		'bookname': '書名',
		'bookbinding': '裝訂冊數',
		'order': '版次',
		'author': '作者',
		'house': '出版社',
		'date': '出版日期',
		'chinese_book_category': '中文圖書分類號',
		'source': '來源',
	};
	let p = {
		'ISBN': 'ISBN',
		'書名': 'bookname',
		'裝訂冊數': 'bookbinding',
		'版次': 'order',
		'作者': 'author',
		'出版社': 'house',
		'出版日期': 'date',
		'中文圖書分類號': 'chinese_book_category',
		'來源': 'source',
	};

	let q;
	if (key2head) {
		q = o;
	}
	else {
		q = p;
	}

	if (haskey(q, k)) {
		return q[k];
	}
	else {
		return k
	}

}

function aj_booklist_dict_array(ar, key2head) {
	//書籍中英鍵值物件轉換

	function forobj(o) {
		let r = {};
		_.each(o, function (vv, kk) {
			let knew = aj_booklist_dict(key2head, kk);
			r[knew] = vv;
		})
		return r;
	}

	let r = [];
	_.each(ar, function (vv, kk) {
		r.push(forobj(vv));
	})

	return r;
}

function aj_isbnnet_ISBN(ISBN) {
	//使用book_info API

	//df
	let df = GenDF();

	//transferData
	let transferData = {
		'ISBN': ISBN,
		'source': 'NCL',
	}

	//aj_send
	aj_send('POST', '/ebookSystem/book_info/' + ISBN + '/', transferData)
		.done(function (data) {

			//message
			if (data.message === '查無資料') {

				//reject
				df.reject(data);

			}
			else {

				//book
				let book = {
					'ISBN': cstr(data.ISBN),
					'書名': cstr(data.bookname),
					'作者': cstr(data.author),
					'出版社': cstr(data.house),
					'出版日期': cstr(data.date),
					'裝訂方式': cstr(data.bookbinding),
					'圖書類號': cstr(data.chinese_book_category),
					'版次': cstr(data.order),
					'來源': cstr('NCL'),
				};

				//resolve
				df.resolve(book);

			}

		})
		.fail(function (data) {

			//reject
			df.reject(data);

		})

	return df;
}

function aj_isbnnet(transferData) {
	//查找[全國新書資訊網]書籍資訊

	return aj_querybooklist('NCL', transferData);
}

function aj_douban(value) {
	//用value查找[豆瓣]書籍資訊

	let transferData = {
		'search_query': value,
	};
	return aj_querybooklist('douban', transferData);
}

function aj_isbnnetanddouban_ISBN(ISBN) {
	//用ISBN查找[全國新書資訊網]與[豆瓣]書籍資訊

	//df
	let df = GenDF();

	//df, d
	let df_isbnnet = GenDF();
	let df_douban = GenDF();
	let d_isbnnet = [];
	let d_douban = [];

	aj_isbnnet_ISBN(ISBN)
		.done(function (data) {
			console.log('aj_isbnnet done ', data)
			d_isbnnet = [data]; //回傳為單一物件轉陣列

			//NCL優先，直接略過豆瓣查詢
			df_douban.resolve();

		})
		.fail(function (data) {
			console.log('aj_isbnnet fail', data)
		})
		.always(function () {
			df_isbnnet.resolve();
		})

	//aj_douban
	aj_douban(ISBN)
		.done(function (data) {
			console.log('aj_douban done ', data)
			d_douban = data;
		})
		.fail(function (data) {
			console.log('aj_douban fail ', data)
		})
		.always(function () {
			df_douban.resolve();
		})

	//when
	$.when(df_isbnnet, df_douban)
		.done(function () {

			//r
			let r = [];
			_.each(d_isbnnet, function (v) {
				r.push(v);
			})
			_.each(d_douban, function (v) {
				r.push(v);
			})

			//no date
			if (r.length === 0) {

				//reject
				df.reject('無書籍資料');

			}
			else {

				//resolve
				df.resolve(r[0]); //只針對合併後第一本回傳，有NCL時，豆瓣會因回傳較慢被直接取消

			}

		})

	return df;
}

function aj_isbnnetanddouban(value) {
	//用value查找[全國新書資訊網]與[豆瓣]書籍資訊

	//df
	let df = GenDF();

	//df, d
	let df_isbnnet = GenDF();
	let df_douban = GenDF();
	let d_isbnnet = [];
	let d_douban = [];

	//aj_isbnnet
	let transferData = {
		'FO_SchRe1ation0': 'Null',
		'FO_SearchField0': 'Title',
		'FO_SearchValue0': value,
		'FO_SchRe1ation1': 'OR',
		'FO_SearchField1': 'ISBN',
		'FO_SearchValue1': value,
		'FO_SchRe1ation2': 'AND',
		'FO_SearchField2': '',
		'FO_SearchValue2': '',
	};
	aj_isbnnet(transferData)
		.done(function (data) {
			console.log('aj_isbnnet done', data)
			d_isbnnet = data;
		})
		.fail(function (data) {
			console.log('aj_isbnnet fail', data)
		})
		.always(function () {
			df_isbnnet.resolve();
		})

	//aj_douban
	aj_douban(value)
		.done(function (data) {
			console.log('aj_douban done', data)
			d_douban = data;
		})
		.fail(function (data) {
			console.log('aj_douban fail', data)
		})
		.always(function () {
			df_douban.resolve();
		})

	//when
	$.when(df_isbnnet, df_douban)
		.done(function () {

			//r
			let r = [];
			_.each(d_isbnnet, function (v) {
				r.push(v);
			})
			_.each(d_douban, function (v) {
				r.push(v);
			})

			//no date
			if (r.length === 0) {

				//reject
				df.reject('無書籍資料');

			}
			else {

				//resolve
				df.resolve(r);

			}

		})

	return df;
}


function aj_querybooklist(source, transferData) {
	//使用get_book_info_list API

	//df
	let df = GenDF();

	//url
	let url = '/ebookSystem/get_book_info_list/'; //post會加「/」而get不會

	//transferData
	// let transferData={
	//	 'FO_SchRe1ation0':'Null',
	//	 'FO_SearchField0':'Title',
	//	 'FO_SearchValue0':'新手媽媽',
	//	 'FO_SchRe1ation1':'AND',
	//	 'FO_SearchField1':'',
	//	 'FO_SearchValue1':'',
	//	 'FO_SchRe1ation2':'AND',
	//	 'FO_SearchField2':'',
	//	 'FO_SearchValue2':'',
	// };
	transferData['source'] = source;

	//aj_post
	aj_send('post', url, transferData)
		.done(function (data) {
			//console.log(data)

			if (data['status'] === 'success') {

				//o
				let o = data['bookinfo_list'];

				//p
				let p = [];
				_.each(o, function (v, k) {
					let r = {
						// 'ISBN':v[0],
						// 'bookname':v[1], //書名
						// 'author':v[2], //作者
						// 'house':v[3], //出版社/出版機構
						// 'date':v[4], //出版日期
						// 'bookbinding':v[5], //裝訂冊數/裝訂方式
						// 'classnumber':v[6], //圖書類號
						// 'order':v[7], //版次/出版版次	
						'ISBN': cstr(v[0]),
						'書名': cstr(v[1]),
						'作者': cstr(v[2]),
						'出版社': cstr(v[3]),
						'出版日期': cstr(v[4]),
						'裝訂方式': cstr(v[5]),
						'圖書類號': cstr(v[6]),
						'版次': cstr(v[7]),
						'來源': cstr(source),
					};
					p.push(r);
				})

				if (p.length > 0) {
					df.resolve(p);
				}
				else {
					df.reject('無書籍資料');
				}

			}
			else {
				//console.log(data['message']);
				df.reject('無書籍資料');
			}

		})
		.fail(function (msg) {
			//console.log(msg)
			df.reject('無書籍資料');
		})

	return df;
}

function aj_booksetpriority(password, ISBN, priority) {
	//使用API book_action

	//df
	let df = GenDF();

	//url
	let url = '/ebookSystem/book_action/';

	//transferData
	let transferData = {
		'action': 'set_priority',
		'ISBN': ISBN,
		'password': password,
		'priority': priority,
	};

	//aj_post
	aj_send('post', url, transferData)
		.done(function (data) {
			df.resolve(data);
		})
		.fail(function (data) {
			df.reject(data);
		})

	return df;
}

function rest_aj_send(type, url, transferData) {
	//ajax傳送訊息

	//df
	let df = GenDF();

	//ajax
	$.ajax({
		url: url,
		type: type,
		data: transferData,
		//ata: JSON.stringify(transferData),
		//contentType: 'application/json', //default: 'application/x-www-form-urlencoded; charset=UTF-8'
		beforeSend: function (jqXHR, settings) {
			if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
				let g = aj_getcsrf();
				jqXHR.setRequestHeader('X-CSRFToken', g['X-CSRFToken']);
				jqXHR.setRequestHeader('X-Requested-With', g.XMLHttpRequest)
			}
		},
		'error': function (xhr) {

			//reject
			let res = {
				'status': xhr.status,
				'message': '伺服器錯誤回應: ' +xhr.status +' - ' +xhr.responseText,
			};

			df.reject(res);

		},
		success: function(data, textStatus, xhr) {
			if (xhr.status >= 200 && xhr.status < 300) {
				let res = {
					'status': xhr.status,
					'data': data,
					'message': '',
				};
				if(!iser(data)){
					if (data.hasOwnProperty('detail')){
						res['message'] = '伺服器成功操作: ' +xhr.status +' - ' +data['detail']
					}
				}
				else {
					res['message'] = '伺服器成功操作: ' +xhr.status +' - '
				}

				df.resolve(res);
			}
			else {
				//reject
				let res = {
					'status': 'error',
					'message': o2j(data),
				};

				df.reject(res);
			}
		}
	})

	return df;

}

function rest_aj_send_memory(type, url, data, memory) {
	//用key作紀錄

	//df
	let df = GenDF();

	rest_aj_send(type, url, data)
	.done(function(data) {
		data['memory'] = memory
		df.resolve(data)
	})
	.fail(function(xhr, result, statusText){
		data['key'] = key
		df.reject(data)
	})
	return df
}

function rest_aj_upload(url, transferData) {
	//ajax傳送訊息

	//df
	let df = GenDF();

	//FormData
	let formData = new FormData();
	_.each(transferData, function (v, k){
		formData.append(k, v);
	})

	//gen uuid
	let uuid=gen_uuid();


	let refreshIntervalId="";

	//ajax
	$.ajax({
		url: url,
		type: 'POST',
		data: formData,
		cache: false,
		processData: false,
		contentType: false,
		headers: { 'X-Progress-ID': uuid },
		beforeSend: function (jqXHR, settings) {
			if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
				let g = aj_getcsrf();
				jqXHR.setRequestHeader('X-CSRFToken', g.csrf);
				jqXHR.setRequestHeader('X-Requested-With', g.XMLHttpRequest)
			}

			//show progress bar
			$('#pleaseWaitDialog').modal('show');

		},
		'error': function (xhr) {

			//hide progress bar
			$('#pleaseWaitDialog').modal('hide');
			if(refreshIntervalId!="")
				clearInterval(refreshIntervalId);

			//reject
			let res = {
				'status': xhr.status,
				'message': '伺服器錯誤回應: ' +xhr.status +' - ' +xhr.responseText,
				'data': '',
			};

			df.reject(res);

		},
		success: function(data, textStatus, xhr) {

			//hide progress bar
			$('#pleaseWaitDialog').modal('hide');
			if(refreshIntervalId!="")
				clearInterval(refreshIntervalId);

			if (xhr.status >= 200 && xhr.status < 300) {
				let res = {
					'status': xhr.status,
					'message': '',
					'data': data,
				};
				if (data.hasOwnProperty('detail')){
					res['message'] = '伺服器成功操作: ' +xhr.status +' - ' +data['detail']
				}
				else {
					res['message'] = '伺服器成功操作: ' +xhr.status +' - '
				}

				df.resolve(res);
			}
			else {
				//reject
				let res = {
					'status': 'error',
					'message': o2j(data),
					'data': o2j(data),
				};

				df.reject(res);
			}
		}
	})

	showProgress(uuid)
	refreshIntervalId=setInterval(function() {
		showProgress(uuid);
	},1000);

	return df;

}

function gen_uuid() {
	var uuid = ""
	for (var i=0; i < 32; i++) {
		uuid += Math.floor(Math.random() * 16).toString(16); 
	}
	return uuid
}

function showProgress(uuid) {
	$.getJSON('/genericUser/upload_progress', {'X-Progress-ID': uuid},function(data,status,xhr){
		if(data){
			var progress =parseInt((parseInt(data.uploaded) / parseInt(data.length))*100);
			//console.log(progress);
			$('#uploadProgressBar').css('width', progress+'%').attr('aria-valuenow', progress);
			$('#uploadProgressText').text(progress+'% Complete (success)');
		}else{
			return;
		}
	});
}

(function($) {
	$.extendObjectArray = (destArr, srcArr, key) => {
		srcArr.forEach(srcObj => (existObj => {
			if (existObj.length) {
				$.extend(true, destArr[destArr.indexOf(existObj[0])], srcObj);
			} else {
				destArr.push(srcObj);
			}
		})(destArr.filter(v => v[key] === srcObj[key])));
		return destArr;
	};
})(jQuery);

function compare(key, order){
	function desc(a,b) {
		if (a[key] < b[key])
			return 1;
		if (a[key] > b[key])
			return -1;
		return 0;
	}
	function asc(a,b) {
		if (a[key] < b[key])
			return -1;
		if (a[key] > b[key])
			return 1;
		return 0;
	}
	if(order==='desc'){return desc}
	if(order==='asc'){return asc}
	return asc
}

function fill_cell(array, fields, value){
	_.each(array, function(v){
		_.each(fields, function(field){
		if(!v.hasOwnProperty(field))
			v[field] = value
		})
	})
}

function genMonth(v){
	let today = new Date()
	let year, month, date

	year = today.getFullYear()
	month = today.getMonth()+1
	date = today.getDate()

	let year_begin, month_begin, year_end, month_end

	if(month-v<=0){
		year_begin = year -1
		month_begin = month-v+12
	}
	else {
		year_begin = year
		month_begin = month-v
	}

	if(month-v+1<=0){
		year_end = year -1
		month_end = month-v+1+12
	}
	else {
		year_end = year
		month_end = month-v+1
	}

	let begin_time, end_time

	if(!(v===0)){
		begin_time = year_begin.toString() +'-' +month_begin.toString() +'-01'
		end_time = year_end.toString() +'-' +month_end.toString() +'-01'
	}
	else {
		begin_time = year.toString() +'-' +month.toString() +'-01'
		end_time = year.toString() +'-' +month.toString() +'-' +(date+1).toString()
	}

	return {
		'begin_time': begin_time,
		'end_time': end_time,
	}

}