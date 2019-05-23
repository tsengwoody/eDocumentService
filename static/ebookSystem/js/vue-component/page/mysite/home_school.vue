<template>
	<div class="home_school">
		<div class="row">
		    <div class="row space-16">&nbsp;</div>
		    <div class="row">
		      <div class="col-sm-3">
		        <div class="thumbnail">
		          <div class="caption text-center" onclick="location.href='#'">
		            <div class="position-relative">
		              <img src="/genericUser/api/bannercontents/1/resource/cover/image" />
		            </div>
		            <h4 id="thumbnail-label"><a href="#" target="_blank">校園版服務介紹</a></h4>
		          </div>
		        </div>
		      </div>

		      <div class="col-sm-3">
		        <div class="thumbnail">
		          <div class="caption text-center" onclick="location.href='#'">
		            <div class="position-relative">
		              <img src="https://az818438.vo.msecnd.net/icons/slack.png" style="width:72px;height:72px;" />
		            </div>
		            <h4 id="thumbnail-label"><a href="#" target="_blank">平台系統公告</a></h4>
		          </div>
		        </div>
		      </div>

		      <div class="col-sm-3">
		        <div class="thumbnail">
		          <div class="caption text-center" onclick="location.href='#'">
		            <div class="position-relative">
		              <img src="https://az818438.vo.msecnd.net/icons/slack.png" style="width:72px;height:72px;" />
		            </div>
		            <h4 id="thumbnail-label"><a href="#" target="_blank">協會簡介</a></h4>
		          </div>
		        </div>
		      </div>

		      <div class="col-sm-3">
		        <div class="thumbnail">
		          <div class="caption text-center" onclick="location.href='#'">
		            <div class="position-relative">
		              <img src="https://az818438.vo.msecnd.net/icons/slack.png" style="width:72px;height:72px;" />
		            </div>
		            <h4 id="thumbnail-label"><a href="#" target="_blank">著作權說明</a></h4>
		          </div>
		        </div>
		      </div>
		    </div>
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
	module.exports = {
		data: function() {
			return {

			}
		},
		mounted: function() {
			document.title = '首頁';

		},
		methods: {

		},
	}
</script>

<style>
.thumbnail {
	box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
	transition: 0.3s;
	min-width: 40%;
	border-radius: 5px;
}

.thumbnail:hover {
	cursor: pointer;
	box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.5);
}

.thumbnail img {
	width: 100%;
}

ul.navigation {
  list-style: none; 
  padding: 0;
}
ul.navigation li {
  display: inline;
}
</style>
