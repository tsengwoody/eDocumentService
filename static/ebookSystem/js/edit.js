function changePage(offset){
	page=document.getElementById("id_page");
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
	page=document.getElementById("id_page");
	imgScanPage=$('#scanPage')[0];
	src=imgScanPage.src;
	console.log(src);
	src=src.split('/');
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
function saveSubmit(event)
{
    if(typeof $('textarea').val()=='undefined')
    {
        event.preventDefault();
        alert("not contain keyword");
    }
    var str=$('textarea').val();
    if(str.indexOf("|----------|")<0)
    {
        event.preventDefault();
        alert("not contain keyword");
    }
}
function finishSubmit(event)
{
    if(typeof $('textarea').val()=='undefined')
    {
        event.preventDefault();
        alert("not contain keyword");
    }
    var str=$('textarea').val();
    if(str.indexOf("|----------|")>0)
    {
        event.preventDefault();
        alert("can not contain keyword");
    }
}

$( document ).ready(function() {
    console.log( "ready!" );
    $('#save_id').click(saveSubmit);
    $('#finish_id').click(finishSubmit);


    $('#zoomIN').click(function(){
        imgSize.value=(parseInt(imgSize.value)-10).toString()+'%';
        $('#scanPage').css('width',imgSize.value);

    });
    $('#zoomOUT').click(function(){

        imgSize.value=(parseInt(imgSize.value)+10).toString()+'%';
        $('#scanPage').css('width',imgSize.value);

    });



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