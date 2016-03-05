function changePage(offset){
	//alert("changePage");
	page=document.getElementById("id_page");
	//console.log(page);
	//imgScanPage=document.getElementsByName("scanPage");
	imgScanPage=$('#scanPage')[0];
	src=imgScanPage.src;

	src=src.split('/');
	dirname=''
	for (i = 0;i < src.length-1; i++) dirname=dirname+src[i]+'/';
		filename=src[src.length-1];
		extensionName=filename.split('.')[1];
		filename=filename.split('.')[0];
		scanPageList=document.getElementById("scanPageList");
	if(scanPageList.selectedIndex+offset>=0&&scanPageList.selectedIndex+offset<scanPageList.length) {
		scanPageList.selectedIndex=scanPageList.selectedIndex+offset;
		page.value=scanPageList.selectedIndex;
		imgScanPage.src=dirname+scanPageList.options[scanPageList.selectedIndex].value;
	} else {
		alert('超過頁數範圍惹~');
	}
}
function changePageSelect() {
	//alert("changePageSelect");
	page=document.getElementById("id_page");
	//iframeList=document.getElementsByName("scanPage");
	imgScanPage=$('#scanPage')[0];
	src=imgScanPage.src;
	console.log(src);
	src=src.split('/');
	//alert(src);
	dirname=''
	for (i = 0;i < src.length-1; i++) 
		dirname=dirname+src[i]+'/';
	filename=src[src.length-1];
	extensionName=filename.split('.')[1];
	filename=filename.split('.')[0];
	scanPageList=document.getElementById("scanPageList");
	page.value=scanPageList.selectedIndex;
	imgScanPage.src=dirname+scanPageList.options[scanPageList.selectedIndex].value;
}
$( document ).ready(function() {
    console.log( "ready!" );
    $('#chagePost').click(function(){
    	if($('#imagePage').hasClass('col-md-6'))
    	{
    		$('#imagePage').removeClass("col-md-6");
    		$('#imagePage').addClass("col-md-12");
    	}else{
    		$('#imagePage').removeClass("col-md-12");
    		$('#imagePage').addClass("col-md-6");
    	}

    	if($('#textPage').hasClass('col-md-6'))
    	{
    		$('#textPage').removeClass("col-md-6");
    		$('#textPage').addClass("col-md-12");
    	}else{
    		$('#textPage').removeClass("col-md-12");
    		$('#textPage').addClass("col-md-6");
    	}

    });
});