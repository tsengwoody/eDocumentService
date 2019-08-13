<template>
	<div>
		<div class="homeCarousel">
			<h2 class="sr-only">校園版首頁</h2>
			<div class="school-slide">
				<img
					src="static/ebookSystem/img/school/banner.png"
					alt=""
					title=""
					style="width: 100%" 
				>
				<div class="slide-icons">
					<a href="https://line.me/R/ti/g/eYf_3Ast89" target="_blank">
						<img src="static/ebookSystem/img/school/line.png" alt="link to Line account">
					</a>
					<a href="https://www.facebook.com/forblind/" target="_blank">
						<img src="static/ebookSystem/img/school/fb-icon.png" alt="link to Facebook page">
					</a>
					<a href="https://www.youtube.com/channel/UC8TV4EKxbSQPzx8nmTzfIag" target="_blank">
						<img src="static/ebookSystem/img/school/youtube.png" alt="link to Youtube page">
					</a>
				</div>
			</div>
		</div>

		<form class="form-inline form-row">
			<div class="form-group">
				列表排序：依
				<label>
					<input type="radio" name="sortField"> 發佈日期
				</label>

				<label>
					<input type="radio" name="sortField"> 點閱次數
				</label>

				<button class="btn btn-default u-margin-left-sm">排序</button>
			</div>
		</form>

		<form class="form-inline form-row">
			<div class="form-group">
				
				<div class="form-group">
					<label for="sel1">發佈單位：依</label>
					<select class="form-control">
						<option>org 1</option>
						<option>org 2</option>
						<option>org 3</option>
						<option>org 4</option>
					</select>
				</div>

				<label class="u-margin-left-sm">
					關鍵字：<input type="text" class="form-control">
				</label>

				<button class="btn btn-default u-margin-left-sm">搜尋</button>
			</div>
		</form>

		<h3>校園公佈欄列表</h3>
		<div class="row">
			
			<div style="float: left;width: 65%;margin: 0px 1rem;">
				<table-div :datas="datas" :header="header">
				</table-div>
			</div>
			

			<div style="width: 30%; float: left;">
				<div class="col-sm-4">
					<a href="#" class="tool-box">
						<div class="tool-box__img">
							<img src="static/ebookSystem/img/school/sun.png" alt="" style="height:100%;">
						</div>
						<div class="tool-box__text">志工招募</div>
					</a>
				</div>
			
				<div class="col-sm-4">
					<a href="#" class="tool-box">
						<div class="tool-box__img">
							<img src="static/ebookSystem/img/school/wifi.png" alt="" style="height:100%;">
						</div>
						<div class="tool-box__text">關於我們</div>
					</a>
				</div>
				<div class="col-sm-4">
					<a href="#" class="tool-box">
						<div class="tool-box__img">
							<img src="static/ebookSystem/img/school/pen.png" alt="" style="height:100%;">
						</div>
						<div class="tool-box__text">聯絡我們</div>
					</a>
				</div>
				<div class="col-sm-4">
					<a href="#" class="tool-box">
						<div class="tool-box__img">
							<img src="static/ebookSystem/img/school/tool.png" alt="" style="height:100%;">
						</div>
						<div class="tool-box__text">校園管理</div>
					</a>
				</div>
				<div class="col-sm-4">
					<a href="#" class="tool-box">
						<div class="tool-box__img">
							<img src="static/ebookSystem/img/school/boy.png" alt="" style="height:100%;">
						</div>
						<div class="tool-box__text">讀者專區</div>
					</a>
				</div>
				<div class="col-sm-4">
					<a href="#" class="tool-box">
						<div class="tool-box__img">
							<img src="static/ebookSystem/img/school/bird.png" alt="" style="height:100%;">
						</div>
						<div class="tool-box__text">捐書捐款</div>
					</a>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

	module.exports = {
		components: {
			'table-div': components['table-div-order'],
		},
		data: function() {
			return {
				header: {
					title: '標題',
					publishDate: '發佈日期',
					org: '發佈單位',
					readCount: '點閱次數',
				},
				datas: [
					{
						title: 'aaa',
						publishDate: '2019/06/24',
						org: 'org 1',
						readCount: '12',
					},
					{
						title: 'bbb',
						publishDate: '2019/06/24',
						org: 'org 2',
						readCount: '13',
					},
				]
			}
		},
		computed: {
		},
		mounted(){
		},
		methods: {
		},
	}
</script>

<style>

a:hover {
	color:inherit;
	text-decoration: none;
}

.u-margin-left-sm {
	margin-left: 1rem;
}

.tool-box {
	display: inline-block;    
	width: 100px;
    height: 100px; 
    border: 2px solid black;     
    margin: 0 1.2rem 1.2rem 0;
 	text-align: center;
 	border-radius: 3px;
}

.tool-box__img {
	height: 70px;
    width: 100%;
    margin-top: 0.2rem;
    margin-bottom: 0.3rem;
}

.tool-box__text {
	margin-top: 0.2rem;
    color: red;
    font-weight: 600;
    letter-spacing: 2px;
}

.school-slide {
	display: block;
    position: relative;
}

.slide-icons {
	position: absolute;
    right: 1rem;
    bottom: 0.5rem;
}

.slide-icons img {
	height: 3rem;
	margin-left: 1rem;
}

label {
    font-weight: 500;
}

.form-row {
	margin: 1rem;
}

ul.navigation {
  list-style: none; 
  padding: 0;
}
ul.navigation li {
  display: inline;
}

div.introduction-area {
	display: flex;
    justify-content: space-between;
	padding-top: 20px;
}
</style>
