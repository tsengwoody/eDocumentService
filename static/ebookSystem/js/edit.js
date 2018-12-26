function addMark(strValue, editor) {

	var bm = editor.selection.getBookmark(0);
	var caretPos = getCursorPosition(editor);
	var textAreaTxt = editor.getContent();
	var subCarePos = textAreaTxt.substring(0, caretPos);
	var lastLinePos = -1
	var nextLine = ["\n", "<br />", "<br>", "</p>"];
	lastLinePos = -1;
	lastNextLineIndex = 0;
	for (var index in nextLine) {
		if (lastLinePos < subCarePos.lastIndexOf(nextLine[index])) {
			lastLinePos = subCarePos.lastIndexOf(nextLine[index]);
			lastNextLineIndex = index;
		}
	}
	lastLinePos += nextLine[lastNextLineIndex].length;
	setCursorPosition(editor, lastLinePos)
	editor.insertContent(strValue);

}

function detectIdel() {
	console.log("idel_min " + idel_min);
	if (idel_min > 10) {
		function_click = true;
		idel_min = 0;
		window.location.href = "/auth/logout/";
	}
	idel_min++;
}

function calMins() {
	let url = window.location.pathname
	let pk = url.split('/')
	pk = pk[pk.length-2]
	editlog_url = '/ebookSystem/edit_ajax/' +pk +'/';

	let transferData = {};
	transferData["online"] = change_count;
	transferData["page"] = $('#id_page').val();

	rest_aj_send('post', editlog_url, transferData)
	.done(function(data) {
		change_count = 0;
	})
}

function setCursorPosition(editor, index) {
	//get the content in the editor before we add the bookmark... 
	//use the format: html to strip out any existing meta tags
	var content = editor.getContent({ format: "html" });

	//split the content at the given index
	var part1 = content.substr(0, index);
	var part2 = content.substr(index);

	//create a bookmark... bookmark is an object with the id of the bookmark
	var bookmark = editor.selection.getBookmark(0);

	//this is a meta span tag that looks like the one the bookmark added... just make sure the ID is the same
	var positionString = '<span id="' + bookmark.id + '_start" data-mce-type="bookmark" data-mce-style="overflow:hidden;line-height:0px"></span>';
	//cram the position string inbetween the two parts of the content we got earlier
	var contentWithString = part1 + positionString + part2;

	//replace the content of the editor with the content with the special span
	//use format: raw so that the bookmark meta tag will remain in the content
	editor.setContent(contentWithString, ({ format: "raw" }));

	//move the cursor back to the bookmark
	//this will also strip out the bookmark metatag from the html
	editor.selection.moveToBookmark(bookmark);

	//return the bookmark just because
	return bookmark;
}

function getCursorPosition(editor) {
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
	var positionString = '<span id="' + elementID + '"></span>';
	editor.selection.setContent(positionString);

	//get the content with the special span but without the bookmark meta tag
	var content = editor.getContent({ format: "html" });
	//find the index of the span we placed earlier
	var index = content.indexOf(positionString);

	//remove my special span from the content
	editor.dom.remove(elementID, false);

	//move back to the bookmark
	editor.selection.moveToBookmark(bm);

	return index;
}

function rotateFormat() {

	let imagePage = $('#imagePage');
	let textPage = $('#textPage');

	if (imagePage.hasClass('col-md-6')) {
		//改上下

		imagePage.css('margin-bottom', '30px')
			.removeClass("col-md-6")
			.addClass("col-md-12")
		textPage.removeClass("col-md-6")
			.addClass("col-md-12")

	} else {
		//左右

		imagePage.css('margin-bottom', '0px')
			.removeClass("col-md-12")
			.addClass("col-md-6")
		textPage.removeClass("col-md-12")
			.addClass("col-md-6")

	}

}

var editor;

var function_click = false;
var idel_min = 0;
var change_count = 0;

function createHtmlEditor() {

	// Initialize TinyMCE
	tinymce.init({
		forced_root_block: "",
		force_br_newlines: false,
		force_p_newlines: false,
		selector: 'textarea',  // change this value according to your HTML
		toolbar1: '標記 | 載入全文  | 存檔 | 完成 | 關閉 | 切換版型 | 下載原始文字檔',
		toolbar2: 'undo redo | cut copy paste | bullist numlist | table | searchreplace | fontsizeselect ',
		fontsize_formats: '8pt 10pt 12pt 14pt 18pt 24pt 36pt',
		menubar: false,
		setup: function (editor) {

			editor.on('init', function (e) {
				editor.getBody().style.fontSize = '14pt';
			});

			editor.on('change', function (e) {
				idel_min = 0;
				change_count++;
			});

			editor.addButton('標記', {
				type: 'menubutton',
				text: '標記',
				icon: false,
				menu: [{
					text: '圖片標記',
					onclick: function () {
						var message = '<p><img id="' + $('#scanPageList :selected').val() + '" alt="this is a picture" height="42" width="42"></p>';
						addMark(message, editor);
						//editor.insertContent();
					}
				}, {
					text: '未知標記',
					onclick: function () {
						var message = '<span class="unknown" style="color: red;" id="' + $('#scanPageList :selected').val() + '">{???}</span>';
						editor.insertContent(message);

					}
				}, {
					text: '數學標記',
					onclick: function () {
						var message = '<p><span class="mathml" style="color:blue" id="' + $('#scanPageList :selected').val() + '">mathml</span></p>';
						addMark(message, editor);
					}
				}, {
					text: '進度標記',
					onclick: function () {
						var message = '<p>|----------|</p>';
						addMark(message, editor);
					}
				},
				]
			});

			editor.addButton('載入全文', {
				text: '載入全文',
				icon: false,
				onclick: function () {
					function_click = true;

					let url = window.location.pathname
					let pk = url.split('/')
					pk = pk[pk.length-2]
					url = '/ebookSystem/api/ebooks/' +pk +'/action/edit/'

					let transferData = {};
					transferData["type"] = 'load'
					transferData["finish"] = '';
					transferData["edit"] = '';
					transferData["page"] = '';

					rest_aj_send('post', url, transferData)
					.done(function(data) {
						alertmessage('success', data['message'])
						.done(function() {
							location.reload(); //重新載入網頁以更新資訊
						})
					})
					.fail(function(data){
						alertmessage('error', data['message']);
					})

				}
			});

			editor.addButton('存檔', {
				text: '存檔',
				name: 'save',
				icon: false,
				onclick: function () {
					if (editor.getContent().indexOf('<p>|----------|</p>') < 0)
						alertmessage('error', '未存檔成功，您提交的內容未包含特殊標記，無法得知校對進度，若已全數完成請按下完成按紐');
					else {
						function_click = true;
						editor.save();

						let url = window.location.pathname
						let pk = url.split('/')
						pk = pk[pk.length-2]
						url = '/ebookSystem/api/ebooks/' +pk +'/action/edit/'

						let transferData = {};
						transferData["type"] = 'save'
						transferData["finish"] = $('#id_finish').val();
						transferData["edit"] = $('#id_edit').val();
						transferData["page"] = $('#id_page').val();

						rest_aj_send('post', url, transferData)
						.done(function(data) {
							alertmessage('success', data['message'])
							.done(function() {
								location.reload(); //重新載入網頁以更新資訊
							})
						})
						.fail(function(data){
							alertmessage('error', data['message']);
						})
					}
				}
			});

			editor.addButton('完成', {
				text: '完成',
				name: 'finish',
				icon: false,
				onclick: function () {
					if (editor.getContent().indexOf('<p>|----------|</p>') > 0)
						alertmessage('error', '未存檔成功，您提交的內容包含特殊標記，若已完成請將內容中之特殊標記刪除，若未全數完成請按下存檔按紐');
					else {
						function_click = true;
						editor.save();

						let url = window.location.pathname
						let pk = url.split('/')
						pk = pk[pk.length-2]
						url = '/ebookSystem/api/ebooks/' +pk +'/action/edit/'

						let transferData = {};
						transferData["type"] = 'finish'
						transferData["finish"] = $('#id_finish').val();
						transferData["edit"] = $('#id_edit').val();
						transferData["page"] = $('#id_page').val();

						rest_aj_send('post', url, transferData)
						.done(function(data) {
							alertmessage('success', data['message'])
							.done(function() {
								window.location.href = '/routing/ebookSystem/service/';
							})
						})
						.fail(function(data){
							alertmessage('error', data['message']);
						})

					}
				}
			});

			editor.addButton('關閉', {
				text: '關閉',
				name: 'finish',
				icon: false,
				onclick: function () {
					alertconfirm('是否確定離開?')
					.done(function(){
						window.location.href = '/routing/ebookSystem/service/';
					})

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

			editor.addButton('下載原始文字檔', {
				text: '下載原始文字檔',
				name: 'downloadrawtext',
				icon: false,
				onclick: function () {

					//isbnpart
					let href = location.href;
					let s = sep(href, '/');
					let isbnpart = s.pop();

					//url
					let url = '/ebookSystem/api/ebooks/' + isbnpart + '/resource/OCR/origin';

					//aj_text
					aj_text(url,{})
					.done(function(){

						//alert
						alertmessage('success', '成功提交下載原始文字檔');
					})
				}
			});

		},
		plugins: ['save table searchreplace'],
	});
}

$(document).ready(function () {

	function_click = false;
	idel_min = 0;
	change_count = 0;

	var url = window.location.pathname;

	createHtmlEditor();
	calMins();
	setInterval(function () {
		calMins();
		detectIdel();
	}, 60000);

	$("#setValue .close").on("click", function () {
		$('#setValue').hide();
	});

	$(window).on('beforeunload', function (e) {
		console.log('a')
		if (function_click) {
			console.log('b')
			return;
		}
		function_click = false;
		return 'Are you sure you want to leave?';
	});

});