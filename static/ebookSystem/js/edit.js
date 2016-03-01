function changePage(offset){
	page=document.getElementById("id_page");
	iframeList=document.getElementsByName("scanPage");
	src=iframeList[0].src;
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
	iframeList[0].src=dirname+scanPageList.options[scanPageList.selectedIndex].value;
	} else {alert('超過頁數範圍惹~');}
}
function changePageSelect() {
	page=document.getElementById("id_page");
	iframeList=document.getElementsByName("scanPage");
	src=iframeList[0].src;
	src=src.split('/');
	dirname=''
	for (i = 0;i < src.length-1; i++) dirname=dirname+src[i]+'/';
	filename=src[src.length-1];
	extensionName=filename.split('.')[1];
	filename=filename.split('.')[0];
	scanPageList=document.getElementById("scanPageList");
	page.value=scanPageList.selectedIndex;
	iframeList[0].src=dirname+scanPageList.options[scanPageList.selectedIndex].value;
}