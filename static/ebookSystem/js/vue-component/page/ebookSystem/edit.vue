<template>
	<div class="row" id="id_ebook_image">
		<div id="imagePage" :class="imageClass" style="margin-bottom: 1em; padding-bottom: 1em;">
			<viewer ref="viewer" 
				:pk="pk" 
				:images="image"
				:edited_page="old_edited_page"
				:height="viewerHeight"
				@changed="changePage"
			></viewer>
			
			<hr/>

			<div style="position: absolute; bottom: 0; right: 50%; cursor: n-resize; display: block;"
				@mousedown="startAdjustHeight($event)"
			>
				<i class="fa fa-angle-double-down" aria-hidden="true" style="font-size:1.5em;"></i>
			</div>

		</div>

		<div id="textPage" :class="textClass">
			<textarea
				id="id_finish" 
				name="finish"
				style="display: none"
			>{{ current_editrecord.finish }}</textarea>
			<editor 
				autocomplete="off" 
				id="id_edit" 
				name="edit"
				@input="editorChange"
				:init="tinymce_init"
				v-model="current_editrecord.edit"
				:style="{height: editorHeight + 'px'}"
			></editor>
		</div>
	</div>
</template>

<script type="text/javascript"> 

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

	function beforeunloadFun(event) {
		event.returnValue = 'Are you sure you want to leave?';
	}

	module.exports = {
		components: {
			'editor': Editor,
			'viewer': components['viewer'],
		},
		data(){
			return {
				pk: null,
				old_edited_page: 0,
				edited_page: 0,
				image: {},
				imgSize: 100,
				idel_min: 0,
				change_count: 0,
				current_editrecord: {},
				textClass: 'col-md-6 col-sm-12',
				imageClass: 'col-md-6 col-sm-12',
				old_position: {},
				new_position: {},
				isMousedown: false,
				viewerHeight: 455,
				editorHeight: 400,
			}
		},
		computed: {
			tinymce_init(){
				const self = this;
				return {
					forced_root_block: "",
					force_br_newlines: false,
					force_p_newlines: false,
					selector: 'editor',  // change this value according to your HTML
					toolbar1: '標記 | 載入全文  | 存檔 | 完成 | 關閉 | 切換版型 | 還原校對內容',
					toolbar2: 'undo redo | cut copy paste | bullist numlist | table | searchreplace | fontsizeselect ',
					fontsize_formats: '8pt 10pt 12pt 14pt 18pt 24pt 36pt',
					menubar: false,

					setup: function (editor) {
						editor.on('init', function (e) {
							editor.getBody().style.fontSize = '14pt';
						});

						editor.on('ResizeEditor', function(e) {
							const iframeHeight = e.target.editorContainer.clientHeight;
							const editorHeight = Math.round(iframeHeight - 100);
							localStorage.setItem("book_editor_height", editorHeight);
						});

						// 圖片標記路徑目前無效，id 是圖片檔名 (目前沒有特別作用)
						editor.addButton('標記', {
							type: 'menubutton',
							text: '標記',
							icon: false,
							menu: [{
								text: '圖片標記',
								onclick: function () {
									var message = '<p><img id="' + $('#scanPageList :selected').text() + '" alt="this is a picture" height="42" width="42"></p>';
									addMark(message, editor);
									//editor.insertContent();
								}
							}, 
							{
								text: '未知標記',
								onclick: function () {
									var message = '<span class="unknown" style="color: red;" id="' + $('#scanPageList :selected').val() + '">{???}</span>';
									editor.insertContent(message);

								}
							}, 
							{
								text: '數學標記',
								onclick: function () {
									var message = '<p><span class="mathml" style="color:blue" id="' + $('#scanPageList :selected').val() + '">mathml</span></p>';
									addMark(message, editor);
								}
							}, 
							{
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
								const url = '/ebookSystem/api/ebooks/' + self.pk +'/action/edit/';
								let transferData = {
									type: 'load',
									finish: '',
									edit: '',
									page: '',
								};

								rest_aj_send('post', url, transferData)
								.done(function(data) {
									alertmessage('success', data['message'])
									.done(function() {
										self.reloadPage();
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
									editor.save();
									const url = '/ebookSystem/api/ebooks/' + self.pk +'/action/edit/'
									let transferData = {
										type: 'save',
										finish: $('#id_finish').val(),
										edit: $('#id_edit').val(),
										page: self.edited_page,
									};

									rest_aj_send('post', url, transferData)
									.done(function(data) {
										alertmessage('success', data['message'])
										.done(function() {
											self.reloadPage();
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
									editor.save();
									const url = '/ebookSystem/api/ebooks/' + self.pk +'/action/edit/';
									let transferData = {
										type: 'finish',
										finish: $('#id_finish').val(),
										edit: $('#id_edit').val(),
										page: self.edited_page,
									};

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
								.done(() => {
									window.location.href = '/routing/ebookSystem/service/';
								})
							}
						});

						editor.addButton('切換版型', {
							text: '切換版型',
							name: 'rotateFormat',
							icon: false,
							onclick: function () {
								if (self.imageClass.indexOf('col-md-6') > -1) {
									//改上下
									self.imageClass = 'col-md-12';
									self.textClass = 'col-md-12'
								} else {
									//左右
									self.imageClass = 'col-md-6 col-sm-12';
									self.textClass = 'col-md-6 col-sm-12';
								}
								self.$refs.viewer.refreshViewer();
							}
						});

						editor.addButton('還原校對內容', {
							text: '還原校對內容',
							name: 'recover_content',
							icon: false,
							onclick: function () {
								let href = window.location.href;
								let s = sep(href, '/');
								let pk = s.pop();

								alertconfirm('是否確定還原校對內容，執行後現有的校對資料將被還原?')
								.done(() => {
									ebookSystemAPI.ebookAction.recoverContent({pk,})
									.then(res => {
										alertmessage('success', res.data['detail'])
										self.reloadPage()
									})
									.catch(res => {
										alertmessage('error', o2j(res.response.data));
									})


								})

							}
						});

					},
					plugins: ['save table searchreplace'],
				}
			},
		},
		created(){
			const preEditorHeight = localStorage.getItem("book_editor_height");
			const preViewerHeight = localStorage.getItem("viewer_height");
			if (preEditorHeight) {
				this.editorHeight = Math.round(preEditorHeight);
			}
			if (preViewerHeight) {
				this.viewerHeight = Math.round(preViewerHeight);
			}
		},
		mounted(){
			const urlList = window.location.pathname.split('/');
			this.pk = urlList[urlList.length-2];
			this.reloadPage();
			this.recordPerMins();
			setInterval(() => {
				this.recordPerMins();
				this.detectIdel();
			}, 60000);

			window.addEventListener("beforeunload", beforeunloadFun);
		},
		beforeDestroy() {
			window.removeEventListener("beforeunload", beforeunloadFun);
		},
		methods: {
			reloadPage(){
				Promise.all([
					ebookSystemAPI.ebookRest.read(this.pk),
					ebookSystemAPI.ebookAction.readEdit({pk: this.pk}),
				])
				.then(res => {
					this.image = res[0].data.scan_image;
					this.old_edited_page = res[0].data.edited_page;
					this.edited_page = res[0].data.edited_page;
					const bookName = res[0].data.bookname;
					const part = res[0].data.ISBN_part.split('-')[1];
					document.title = '編輯' + bookName + '-part' + part;

					this.current_editrecord = {
						finish: res[1].data.finish,
						edit: res[1].data.edit,
					};
				})
			},
			changePage(value){
				this.edited_page = value;
			},
			recordPerMins: function() {
				// 每 60s 傳送 change count 給後端
				const self = this;
				const editlog_url = '/ebookSystem/api/ebooks/' + self.pk + '/action/editlog/';
				const transferData = {
					online: self.change_count,
					page: self.edited_page,	// 要改成 nowPage
				};

				rest_aj_send('post', editlog_url, transferData)
				.done(function(data) {
					self.change_count = 0;
				})
			},
			detectIdel(){
				// 每 60s 計算使用者閒置時間
				if (this.idel_min > 30) {
					this.idel_min = 0;
					window.removeEventListener("beforeunload", beforeunloadFun);
					window.location.href = "/auth/logout/";
				}
				this.idel_min++;
			},
			editorChange(){
				this.idel_min = 0;
				this.change_count++;
			},
			startAdjustHeight(e){
				e.preventDefault();

				this.isMousedown = true;
				this.old_position = {x: e.clientX, y: e.clientY};

				document.addEventListener('mousemove', this.movingHeight)
				document.addEventListener('mouseup', this.endAdjustHeight)
			},
			movingHeight(e){
				e.preventDefault();
				this.new_postion = {x: e.clientX, y: e.clientY};

				if (this.old_position && this.isMousedown) {
					const diff_height = (this.new_postion.y - this.old_position.y);
					this.viewerHeight = this.viewerHeight + diff_height;
					this.old_position = {x: e.clientX, y: e.clientY};
				}
			},
			endAdjustHeight(){
				this.isMousedown = false;

				this.$emit('updateHeight');
				localStorage.setItem("viewer_height", Math.round(this.viewerHeight));
				document.removeEventListener('mousemove', this.movingHeight)
				document.removeEventListener('mouseup', this.endAdjustHeight)
			},
		},
	}
</script>

<style>
nav[role=navigation], footer[role=footer] {
	display: none;
}

.container {
	width: 95%;
}

#textPage {
	margin-bottom: 100px;
}

hr {
    display: block;
    height: 1px;
    border: 0;
    border-top: 1px solid #ccc;
    margin: 0.5em 0 0 0;
    padding: 0;
}

@media (min-width: 992px)
.container {
    width: 970px;
}

@media (min-width: 768px)
.container {
    width: 750px;
}
input#id_page {
	height: 34px;
	padding: 6px 12px;
	color: #555;
	border: 1px solid #ccc;
	box-shadow: inset 0 1px 1px rgba(0,0,0,.075);
	border-radius: 4px;
}
div#sizeControl {
	margin: 5px 0;
}
</style>
