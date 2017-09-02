$(document).ready(function(){
    let url='/static/ebookSystem/js/frontendsystem-core.js';
    let timetag='?'+Date.now();
    $.getScript(url+timetag)
})



// <button id="test" class="btn btn-default" type="button" onclick="testedit(this)">測試文件編輯功能</button>

// <script>

// 	//初始化套件wiris, tinymce
// 	$(document).ready(function(){
				
// 		_.delay(function(){

// 			//mxeditor
// 			inicomp('mxeditor');

// 			//d
// 			let d=[
// 				{
// 					'kind':'normal',
// 					'data': '<p>WIRIS EDITOR es un editor visual (WYSIWYG) :</p>',
// 				},
// 				{
// 					'kind':'mathml',
// 					'data': '<math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac bevelled="true"><mrow><mi>a</mi><mi>a</mi></mrow><mrow><mi>L</mi><mi>a</mi><mi>T</mi><mi>e</mi><mi>X</mi></mrow></mfrac></math>',
// 				},
// 				{
// 					'kind':'normal',
// 					'data': '<p>It\'s been an exciting year! Last May, we expanded Firebase into our unified app platform, building on the original backend-as-a-service and adding products to help developers grow their user base, as well as test and monetize their apps. Hearing from developers like Wattpad, who built an app using Firebase in only 3 weeks, makes all the hard work worthwhile.</p>',
// 				},
// 						{
// 					'kind':'normal',
// 					'data': '<p>Other:</p>',
// 				},
// 				{
// 					'kind':'mathml',
// 					'data': '<math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><msqrt><msup><mi>a</mi><mn>2</mn></msup><mo>+</mo><msup><mi>b</mi><mrow><mn>0</mn><mo>.</mo><mn>5</mn></mrow></msup><mo>-</mo><mn>4</mn><mi>a</mi><mi>c</mi></msqrt><mrow><mn>2</mn><mi>n</mi></mrow></mfrac></math>',
// 				},
// 			];
// 			$('#test').val(o2b(d));

// 		},1000)

// 	});


// 	function testedit(me){
// 		me=$(me);
// 		let d_in=b2o(me.val());
// 		editor_show(me,d_in,function(d_out){
// 			me.val(o2b(d_out));
// 		});
// 	}


// </script>
