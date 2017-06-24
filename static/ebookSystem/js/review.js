function activaTab(tab){
	$('.nav-pills a[href="#' + tab + '"]').tab('show');
};

// function changePage(offset) {
// 	page = document.getElementById("id_page");
// 	imgScanPage = $('#scanPage')[0];
// 	src = imgScanPage.src;
// 	src = src.split('/');
// 	dirname = ''
// 	for (i = 0; i < src.length - 1; i++) dirname = dirname + src[i] + '/';
// 	filename = src[src.length - 1];
// 	extensionName = filename.split('.')[1];
// 	filename = filename.split('.')[0];
// 	scanPageList = document.getElementById("scanPageList");
// 	if (scanPageList.selectedIndex + offset >= 0 && scanPageList.selectedIndex + offset < scanPageList.length) {
// 		scanPageList.selectedIndex = scanPageList.selectedIndex + offset;
// 		page.value = scanPageList.selectedIndex;
// 		imgScanPage.src = dirname + scanPageList.options[scanPageList.selectedIndex].value;
// 	} else {
// 		//dangerAlert('超過頁數範圍惹~');
// 		alertMessageDialog('error','超過頁數範圍惹~');
// 	}
// }

// function changePageSelect() {
// 	page = document.getElementById("id_page");
// 	imgScanPage = $('#scanPage')[0];
// 	src = imgScanPage.src;
// 	console.log(src);
// 	src = src.split('/');
// 	dirname = ''
// 	for (i = 0; i < src.length - 1; i++)
// 		dirname = dirname + src[i] + '/';
// 	filename = src[src.length - 1];
// 	extensionName = filename.split('.')[1];
// 	filename = filename.split('.')[0];
// 	scanPageList = document.getElementById("scanPageList");
// 	page.value = scanPageList.selectedIndex;
// 	imgScanPage.src = dirname + scanPageList.options[scanPageList.selectedIndex].value;
// }

function review_doc_scrto(ipart, btop) {

	//scroll to top
	function totop(ele){
		ele.scrollTop(0);
	}

	//scroll to bottom
	function tobot(ele){
		ele.scrollTop(ele[0].scrollHeight);
	}

	//element
	let sel=$('#'+'step2_part'+ipart+'_select');
	let opts=sel.find('option');
	let divimg=$('#'+'step2_part'+ipart+'_divimg');
	let divtext=$('#'+'step2_part'+ipart+'_divtext');

	//two mode
	if(btop==='true'){
		let opt=$(opts[0]);
		opt[0].selected = true; 
		sel.change();
		totop(divimg);
		totop(divtext);
	}
	else{
		let opt=$(opts[opts.length-1]);
		opt[0].selected = true; 
		sel.change();
		tobot(divimg);
		tobot(divtext);
	}

}

function review_doc_changeimg(ipart, ioffset){

	//element
	let img=$('#'+'step2_part'+ipart+'_img');
	let sel=$('#'+'step2_part'+ipart+'_select');
	let opt=sel.find('option:selected');

	//optnew
	let optnew;
	if(ioffset===1){
		optnew=opt.next(); 
	}
	else if(ioffset===-1){
		optnew=opt.prev(); 
	}

	//change
	if(optnew.length>0){
		optnew[0].selected = true;
		optnew.parent().change();
	}
	else{
		//alert('超過頁數範圍');
		let json={
			status:'error',
			message:'超過頁數範圍'
		};
		alertDialog(json);
	}
	
}

function review_doc_viewimg(ipart){

	//element
	let img=$('#'+'step2_part'+ipart+'_img');
	let sel=$('#'+'step2_part'+ipart+'_select');
	let fn=sel.find('option:selected').val();

	//src
	let srcori=img.attr('src');
	let s=srcori.split('/');
	s.pop();
	let path=s.join('/') +'/';
	let src=path+fn;

	//set src
	img.attr('src',src);

}


$(document).ready(function() {
	console.log("ready!");

	//initial page
	$('ul[class="nav nav-tabs"]').eq(0).children('li').eq(0).addClass('active');
	$('div[class="tab-pane"]').eq(0).addClass('active');

	//activaTab('step2');
	$('#step1_next_id').click(function(){
		activaTab('step2');
	});
	$('#step2_next_id').click(function(){
		activaTab('step3');
	});
	// $('#prePage').on("click", function() {
	// 	changePage(-1);
	// });
	// //nextPage
	// $('#nextPage').on("click", function() {
	// 	changePage(1);
	// });
	if($('#includedContent').length>0)
		$("#includedContent").load($('#url').val()); 

});