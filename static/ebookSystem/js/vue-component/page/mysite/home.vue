
<template>
	<div>
<!-- 		<div id="id_bannercontent_list">
			<div id="myCarousel" class="carousel slide" data-ride="carousel">
				<ol class="carousel-indicators">
					<template v-for="(item, index) in bannercontentlist">
						<li data-target="#myCarousel"
							v-if="index==0"
							v-bind:data-slide-to="index"
							class="active"
						></li>
						<li data-target="#myCarousel"
							v-if="index!=0"
							v-bind:data-slide-to="index"
						></li>
					</template>
				</ol>

				<div class="carousel-inner" role="listbox">
					<template v-for="(item, index) in bannercontentlist">
						<div class="item active" v-if="index==0">
							<img
								:src="`/genericUser/api/bannercontents/` +item.id +`/resource/cover/image`"
								:alt="item.title"
								:title="item.title"
								style="height: 480px;width:940px" 
							>
						</div>
						<div class="item" v-if="index!=0">
							<img
								:src="`/genericUser/api/bannercontents/` +item.id +`/resource/cover/image`"
								:alt="item.title"
								:title="item.title"
								style="height: 480px;width:940px" 
							>
						</div>
					</template>
				</div>

				<a class="left carousel-control" href="#myCarousel" role="button" data-slide="prev" aria-label="上一頁">
					<span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
					<span class="sr-only">Previous</span>
				</a>
				<a class="right carousel-control" href="#myCarousel" role="button" data-slide="next" aria-label="下一頁">
					<span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
					<span class="sr-only">Next</span>
				</a>
			</div>

			<div class="textfornvda">
				<h4>首頁圖片說明</h4>
				<ul>
					<li v-for="(item, index) in bannercontentlist">
						<div v-html="markdown2html(item.content)"></div>
					</li>
				</ul>
			</div>
		</div> -->

		<div class="homeCarousel">
			<template v-for="(item, index) in bannercontentlist">
				<div class="slides active" v-if="index==0">
					<img
						:src="`/genericUser/api/bannercontents/` +item.id +`/resource/cover/image`"
						:alt="item.title"
						:title="item.title"
						style="height: 480px;width:940px" 
					>
				</div>
				<div class="slides" v-if="index!=0">
					<img
						:src="`/genericUser/api/bannercontents/` +item.id +`/resource/cover/image`"
						:alt="item.title"
						:title="item.title"
						style="height: 480px;width:940px" 
					>
				</div>
			</template>
			

			<a role="button" class="left carousel-control" @click="plusDivs(-1)">
				<span class="pointer-left">&#10094;</span>
			</a>
  			<a role="button" class="right carousel-control" @click="plusDivs(1)">
  				<span class="pointer-right">&#10095;</span>
  			</a>

  			<div class="textfornvda">
				<h4>首頁圖片說明</h4>
				<ul>
					<li v-for="(item, index) in bannercontentlist">
						<div v-html="markdown2html(item.content)"></div>
					</li>
				</ul>
			</div>
		</div>

		<div class="row" style="padding-top: 20px;">
			<div class="col-lg-4">
				<div class="panel panel-success">
					<div class="panel-heading">最新消息 {|{ slideIndex }|}</div>
					<div class="panel-body">
						<template v-for="announcement in showAnnouncements">
							<p style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
								<a class="btn btn-link" role="button" 
									:href="'/routing/genericUser/announcement/' + announcement.id"
								>
									{|{ announcement.year }|}年{|{ announcement.month }|}月{|{ announcement.day }|}日 {|{ announcement.title }|}
								</a>
							</p>
						</template>
						<div class="pull-right">
							<p><a class="btn btn-default center" href="/routing/genericUser/announcement_list/" role="button">公告列表 »</a></p>
						</div>
					</div>
				</div>
			</div>
			<div class="col-lg-4">
				<div class="panel panel-success" itemscope="" itemtype="http://schema.org/Product">
					<div class="panel-heading" itemprop="name">雲端千眼-使用流程</div>
					<div class="panel-body" itemprop="description">
						<p>一、以段落為基準，每段即為一行，辨識軟體基本以這種方式輸出，如有遺漏再請將分多行的文字但為一段之內容合併成一行。二、每行前不需空格。三、英文文句標點使用半形符號。四、中文文句標點使用全形符號，但遇到英文、數字使用半形符號。</p>
						<div class="pull-right">
							<p><a class="btn btn-default center" role="button" href="/genericUser/generics/user_guide/" itemprop="url" >閱讀更多 »</a></p>
						</div>
					</div>
				</div>
			</div>
			<div class="col-lg-4">
				<div class="panel panel-success" itemscope="" itemtype="http://schema.org/Product">
					<div class="panel-heading" itemprop="name">招募志工</div>
					<div class="panel-body" itemprop="description">
						<p>「eDocumentService雲端千眼平台」招募大量志工於線上進行重製書籍服務，不如一般志工型態需固定排班或前往特定地點，只要您有時間、有網路，無論何時何地皆能進行志工服務，讓您的愛不再受到限制！</p>
						<div class="pull-right">
							<p><a class="btn btn-default center" href="/genericUser/generics/recruit/" role="button" itemprop="url">閱讀更多 »</a></p>
						</div>
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
		mounted: function() {
			document.title = '首頁';

			const self = this;
			let client = new $.RestClient('/genericUser/api/');
			client.add('bannercontents');
			client.add('announcements');

			$.when(
				client.bannercontents.read(), 
				client.announcements.read()
			).done(function(res1, res2) {
				self.bannercontentlist = res1[0];
				self.announcementlist = res2[0];
				
				setTimeout(() => {
					self.showDivs(self.slideIndex);
				}, 100);

				self.timer = new Timer(function() {
				    self.plusDivs(1);
				}, 4000);
			})
		},
		computed: {
			showAnnouncements: function() {
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
		methods: {
			markdown2html: function (text) {
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

.slides > img {
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


</style>
