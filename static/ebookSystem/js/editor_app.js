/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports, __webpack_require__) {

	module.exports = __webpack_require__(1);


/***/ },
/* 1 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';

	var _mathEditor = __webpack_require__(2);

	var _mathEditor2 = _interopRequireDefault(_mathEditor);

	var _normalEditor = __webpack_require__(3);

	var _normalEditor2 = _interopRequireDefault(_normalEditor);

	var _previewPanel = __webpack_require__(4);

	var _previewPanel2 = _interopRequireDefault(_previewPanel);

	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

	window.onload = function () {
		var mathEditor = new _mathEditor2.default();
		var normalEditor = new _normalEditor2.default();
		var previewPanel = new _previewPanel2.default(normalEditor, mathEditor);

		document.getElementById('button_to_panel').addEventListener("click", previewPanel.setContent);
	};

/***/ },
/* 2 */
/***/ function(module, exports) {

	'use strict';

	Object.defineProperty(exports, "__esModule", {
		value: true
	});

	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

	var MathEditor = function MathEditor() {
		var _this = this;

		_classCallCheck(this, MathEditor);

		this.getEditorType = function () {
			return "math";
		};

		this.getContent = function () {
			return _this.editor.getMathML();
		};

		this.resetContent = function () {
			_this.editor.setMathML("<math></math>");
		};

		this.setContent = function (html) {
			_this.editor.setMathML(html);
		};

		this.editor = com.wiris.jsEditor.JsEditor.newInstance({ 'language': 'en' });
		this.editor.insertInto(document.getElementById('mathEditor'));
	};

	exports.default = MathEditor;

/***/ },
/* 3 */
/***/ function(module, exports) {

	'use strict';

	Object.defineProperty(exports, "__esModule", {
		value: true
	});

	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

	var NormalEditor = function NormalEditor() {
		_classCallCheck(this, NormalEditor);

		this.getEditorType = function () {
			return "normal";
		};

		this.getContent = function () {
			return tinymce.activeEditor.getContent();
		};

		this.resetContent = function () {
			tinymce.activeEditor.setContent('');
		};

		this.setContent = function (html) {
			tinymce.activeEditor.setContent(html);
		};

		tinymce.init({
			selector: "#normalEditor",
			plugins: ['advlist autolink lists link image charmap print preview hr anchor pagebreak', 'searchreplace wordcount visualblocks visualchars code fullscreen', 'insertdatetime media nonbreaking save table contextmenu directionality', 'emoticons template paste textcolor colorpicker textpattern imagetools codesample toc'],
			toolbar: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media | forecolor backcolor emoticons | codesample'
		});
	};

	exports.default = NormalEditor;

/***/ },
/* 4 */
/***/ function(module, exports) {

	'use strict';

	Object.defineProperty(exports, "__esModule", {
		value: true
	});

	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

	var PreviewPanel = function PreviewPanel(normalEditor, mathEditor) {
		var _this = this;

		_classCallCheck(this, PreviewPanel);

		this.setContent = function () {
			var type = $('.nav-tabs .active').text();
			var editor = type === "normal" ? _this.normalEditor : _this.mathEditor;
			var html = editor.getContent();
			var newEle = document.createElement('div');

			if (_this.selectedEle !== "") {
				if (_this.selectedEle.className.split(' ')[0] === type) {
					_this.selectedEle.innerHTML = html;
					editor.resetContent();
					_this.selectedEle.className = _this.selectedEle.className.split(' ')[0];
					_this.selectedEle = "";
					return;
				} else {
					_this.selectedEle.className = _this.selectedEle.className.split(' ')[0];
					_this.selectedEle = "";
				}
			}

			newEle.className = type;
			newEle.innerHTML = html;
			newEle.addEventListener("click", type == 'normal' ? _this.handleContentToEditor(_this.normalEditor) : _this.handleContentToEditor(_this.mathEditor));

			_this.container.appendChild(newEle);
			editor.resetContent();
		};

		this.handleContentToEditor = function (editor) {
			return function (e) {
				if (_this.selectedEle !== "") {
					_this.selectedEle.className = _this.selectedEle.className.split(' ')[0];
				}
				var type = editor.getEditorType();

				var targetEle = e.target;
				while (targetEle.className !== type) {
					targetEle = targetEle.parentElement;
				}
				_this.selectedEle = targetEle;
				_this.selectedEle.className += ' selectedEle';

				editor.setContent(_this.selectedEle.innerHTML);
				if (type === 'math') {
					$('.nav-tabs a[href="#mathEditorTab"]').tab('show');
				} else if (type === 'normal') {
					$('.nav-tabs a[href="#normalEditorTab"]').tab('show');
				}
			};
		};

		this.container = document.getElementById('previewPanel');
		this.normalEditor = normalEditor;
		this.mathEditor = mathEditor;
		this.selectedEle = "";
	};

	exports.default = PreviewPanel;

/***/ }
/******/ ]);