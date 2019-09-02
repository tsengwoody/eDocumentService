<template>
	<div>
		<div class="homeCarousel">
			<h2 class="sr-only">校園版首頁</h2>
			<div class="school-slide">
				<img
					src="static/ebookSystem/img/school/banner.png"
					alt="校園版 banner"
					title=""
					style="width: 100%" 
				>
				<div class="slide-icons">
					<a href="https://line.me/R/ti/g/eYf_3Ast89" target="_blank">
						<img src="static/ebookSystem/img/school/line.png" alt="連至 Line 帳號(開啟新視窗)">
					</a>
					<a href="https://www.facebook.com/forblind/" target="_blank">
						<img src="static/ebookSystem/img/school/fb-icon.png" alt="連至 Facebook 頁面(開啟新視窗)">
					</a>
					<a href="https://www.youtube.com/channel/UC8TV4EKxbSQPzx8nmTzfIag" target="_blank">
						<img src="static/ebookSystem/img/school/youtube.png" alt="連至 Youtube 頁面(開啟新視窗)">
					</a>
				</div>
			</div>
		</div>

		<h3>校園公佈欄列表</h3>
		<div style="width: 100%;">
			<div class="tool-box-area">
				<div class="tool-box">
					<a href="/genericUser/generics/recruit/" class="tool-box__link">
						<div class="tool-box__img">
							<img src="static/ebookSystem/img/school/sun.png" alt="志工招募" style="height:100%;">
						</div>
						<div class="tool-box__text" aria-hidden="true">志工招募</div>
					</a>
				</div>
			
				<div class="tool-box">
					<a href="/genericUser/generics/func_desc/" class="tool-box__link">
						<div class="tool-box__img">
							<img src="static/ebookSystem/img/school/wifi.png" alt="關於我們" style="height:100%;">
						</div>
						<div class="tool-box__text" aria-hidden="true">關於我們</div>
					</a>
				</div>
				<div class="tool-box">
					<a href="/routing/about/contact/" class="tool-box__link">
						<div class="tool-box__img">
							<img src="static/ebookSystem/img/school/pen.png" alt="聯絡我們" style="height:100%;">
						</div>
						<div class="tool-box__text" aria-hidden="true">聯絡我們</div>
					</a>
				</div>
				<div class="tool-box">
					<a href="/routing/genericUser/manager_school/" class="tool-box__link">
						<div class="tool-box__img">
							<img src="static/ebookSystem/img/school/tool.png" alt="校園管理" style="height:100%;">
						</div>
						<div class="tool-box__text" aria-hidden="true">校園管理</div>
					</a>
				</div>
				<div class="tool-box">
					<a href="/routing/ebookSystem/book_repository_school/" class="tool-box__link">
						<div class="tool-box__img">
							<img src="static/ebookSystem/img/school/boy.png" alt="讀者專區" style="height:100%;">
						</div>
						<div class="tool-box__text" aria-hidden="true">讀者專區</div>
					</a>
				</div>
				<div class="tool-box">
					<a href="#" class="tool-box__link">
						<div class="tool-box__img">
							<img src="static/ebookSystem/img/school/bird.png" alt="捐書捐款" style="height:100%;">
						</div>
						<div class="tool-box__text" aria-hidden="true">捐書捐款</div>
					</a>
				</div>
			</div>

			<div class="announcement-area">
				<table-div :datas="announcement_datas" :header="announcement_header">
					<template slot="action" slot-scope="props">
						<a
							class="btn btn-link"
							role="button"
							:href="'/routing/genericUser/announcement/' +props.item +'/'"
						>閱讀全文</a>
					</template>
				</table-div>
			</div>
		</div>
		<div style="clear: both;"></div>
	</div>
</template>

<script>

	module.exports = {
		components: {
			'table-div': components['table-div-order'],
		},
		data(){
			return {
				announcement_header: {
					title: '標題',
					datetime: '發佈日期',
					action: '動作',
				},
				announcement_datas: [],
			}
		},
		computed: {
		},
		mounted(){
			this.get_school_announcement()
		},
		methods: {
			get_school_announcement(){

				query = {'category': '校園公告'}

				genericUserAPI.announcementRest.filter(query)
				.then((response) => {
					let filter_data = []
					_.each(response.data, (v) => {
						let temp_data = {
							"id": v.id,
							"title": v['title'],
							"datetime": v['datetime'],
							"action": v.id,
						}
						filter_data.push(temp_data)
					})
					this.announcement_datas = filter_data
				})

			},
		},
	}
</script>

<style>

.tool-box-area {
	width: 30%; 
	float: right;
	text-align: center;
}

.announcement-area {
	float: left;
	width: 65%;
	margin: 0px 1rem;
}

@media (max-width: 1024px) {
	.tool-box-area {
		width: 100%; 
		float: none;
		margin-top: 1rem;
	}
}

@media (max-width: 700px) {
	.tool-box-area > .tool-box {
		width: 30%; 
		float: none;
		margin-top: 0.5rem;
		margin-right: 0;
	}
}

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
    margin: 0 0.5rem 1.2rem 0;
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
