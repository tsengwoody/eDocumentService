<template>
	<div>
		<div class="homeCarousel">
			<h2 class="sr-only">首頁</h2>
			<template v-for="(item, index) in bannercontentlist">
				<div class="slides active" v-if="index==0">
					<a :href="item.url">
						<img
							:src="`/genericUser/api/bannercontents/` +item.id +`/resource/cover/image`"
							:alt="item.title"
							:title="item.title"
							style="height: 480px;width:940px" 
						>
					</a>
				</div>
				<div class="slides" v-if="index!=0">
					<a :href="item.url">
						<img
							:src="`/genericUser/api/bannercontents/` +item.id +`/resource/cover/image`"
							:alt="item.title"
							:title="item.title"
							style="height: 480px;width:940px" 
						>
					</a>
				</div>
			</template>
			
			<a role="button" class="left carousel-control" @click="plusDivs(-1)">
				<span class="pointer-left" aria-hidden="true">&#10094;</span>
				<span class="sr-only">上一頁</span>
			</a>
			<a role="button" class="right carousel-control" @click="plusDivs(1)">
				<span class="pointer-right" aria-hidden="true">&#10095;</span>
				<span class="sr-only">下一頁</span>
			</a>

			<div class="textfornvda">
				<h3>輪播圖片說明</h3>
				<ul>
					<li v-for="(item, index) in bannercontentlist">
						<div v-html="markdown2html(item.content)"></div>
					</li>
				</ul>
			</div>
		</div>

		<div class="row introduction-area">
			<button type="button" class="btn btn-secondary btn-lg">校園版服務介紹</button>
			<button type="button" class="btn btn-secondary btn-lg">平台系統公告</button>
			<button type="button" class="btn btn-secondary btn-lg">協會簡介</button>
			<button type="button" class="btn btn-secondary btn-lg">著作權說明</button>
		</div>

		<div class="row" style="padding-top: 20px;">
			<div class="col-lg-4">
				<div class="panel panel-success">
					<div class="panel-heading">校園管理</div>
					<div class="panel-body">
						<ul class="navigation">
						    <li><a class="btn btn-link" 
								href="#"
							>
								校對進度查詢
							</a></li>

						    <li><a class="btn btn-link" 
								href="#"
							>
								志工時數查詢
							</a></li>
						</ul> 
					</div>
				</div>
			</div>
			<div class="col-lg-4">
				<div class="panel panel-success" itemscope="" itemtype="http://schema.org/Product">
					<div class="panel-heading" itemprop="name">服務使用者</div>
					<div class="panel-body" itemprop="description">
						<ul class="navigation">
						    <li><a class="btn btn-link" 
								href="#"
							>
								書籍快速下載
							</a></li>

						    <li><a class="btn btn-link" 
								href="#"
							>
								應用工具下載
							</a></li>
						</ul>
					</div>
				</div>
			</div>
			<div class="col-lg-4">
				<div class="panel panel-success" itemscope="" itemtype="http://schema.org/Product">
					<div class="panel-heading" itemprop="name">志工專區</div>
					<div class="panel-body" itemprop="description">
						<ul class="navigation">
						    <li><a class="btn btn-link" 
								href="#"
							>
								快速領書
							</a></li>

						    <li><a class="btn btn-link" 
								href="#"
							>
								校對規則說明
							</a></li>

							<li><a class="btn btn-link" 
								href="#"
							>
								服務時數說明
							</a></li>

							<li><a class="btn btn-link" 
								href="#"
							>
								帳號管理
							</a></li>

							<li><a class="btn btn-link" 
								href="#"
							>
								服務時數
							</a></li>
						</ul>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

	function Timer(fn, t) {
	    var timerObj = setInterval(fn, t);

	    this.stop = function() {
	        if (timerObj) {
	            clearInterval(timerObj);
	            timerObj = null;
	        }
	        return this;
	    }

	    // start timer using current settings (if it's not already running)
	    this.start = function() {
	        if (!timerObj) {
	            this.stop();
	            timerObj = setInterval(fn, t);
	        }
	        return this;
	    }

	    // start with new interval, stop current interval
	    this.reset = function(newT) {
	        t = newT;
	        return this.stop().start();
	    }
	}

	module.exports = {
		data: function() {
			return {
				bannercontentlist: null,
				announcementlist: null,
				slideIndex: 1,
				timer: null,
			}
		},
		computed: {
			showAnnouncements(){
				let target_announcements = [];
				if (this.announcementlist) {
					if(this.announcementlist.length < 3) {
						target_announcements = this.announcementlist;
					} else {
						target_announcements = this.announcementlist.slice(0, 2);
					}
				}
				return target_announcements.map(function(announcement) {
					let year, month, day;
					[year, month, day] = announcement.datetime.split('-');
					return {
						id: announcement.id,
						title: announcement.title,
						year,
						month,
						day,
					}
				});
			}
		},
		mounted(){
			Promise.all([
				genericUserAPI.bannerContentRest.filter({category: 'self'}),
				genericUserAPI.announcementRest.list(),
			])
			.then(res => {
				this.bannercontentlist = res[0].data;
				this.announcementlist = res[1].data;

				setTimeout(() => {
					this.showDivs(this.slideIndex);
				}, 100);

				this.timer = new Timer(() => {
					this.plusDivs(1);
				}, 4000);

			})

		},
		methods: {
			markdown2html(text){
				const converter = new showdown.Converter();
				const html = converter.makeHtml(text);
				return html;
			},
			plusDivs(n) {
			  	this.showDivs(
			  		this.slideIndex += n
			  	);
			  	this.timer.reset(4000);
			},
			showDivs(n) {
				const slides = document.getElementsByClassName("slides");
				if (n > slides.length) {
					this.slideIndex = 1
				}
				if (n < 1) {
					this.slideIndex = slides.length
				}
				for (let i = 0; i < slides.length; i++) {
					slides[i].style.display = "none";  
				}

				if (slides.length > 0) {
					slides[ this.slideIndex - 1 ].style.display = "block";
				}
			}
		},
	}
</script>

<style>
.carousel-inner > .item > img,
.carousel-inner > .item > a > img {
  margin: auto;
}

.homeCarousel {
	position: relative;
	width: 100%;
	overflow: hidden;
}

@keyframes opac{
	from{opacity:0} 
	to{opacity:1}
}

.slides {
	display:none; 
	animation: opac 0.8s;
}

.slides img {
	margin: auto;
	display: block;
    max-width: 100%;
}

.pointer-left, .pointer-right {
	position: absolute;
    top: 50%;
    z-index: 5;
    display: inline-block;
    font-size: 1.2em;
}

.pointer-right {
	right: 50%;
    margin-right: -10px;
}

.pointer-left {
	left: 50%;
    margin-left: -10px;
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
