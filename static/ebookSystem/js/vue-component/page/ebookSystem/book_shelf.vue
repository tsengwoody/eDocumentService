
<template>
	<div id="book_shelf" class="container">
		<h2>借閱書櫃</h3>
		<ul class="nav nav-tabs">
			<li class="active"><a href="#book_shelf_checkout" name="book_shelf_tab_grp" data-toggle="tab" aria-expanded="true">正借閱書籍</a></li>
			<li><a href="#book_shelf_checkin" name="book_shelf_tab_grp" data-toggle="tab" aria-expanded="false">借閱歷史紀錄</a></li>
		</ul>
		<div class="tab-content" style="padding:20px 0px;">
			<div id="book_shelf_checkout" class="tab-pane active">
				<h3>正借閱書籍</h3>
				<table-div :datas="checkout_list" :header="checkout_header">
					<template slot="action" slot-scope="props">
						<a
							class="btn btn-default" role="button"
							:href="'/ebookSystem/library_view?ISBN=' +props.item.id"
							target="_blank" title="閱讀(另開新視窗)"
						>閱讀</a>
						<button
							class="btn btn-default"
							@click="$refs.db.instance_set(props.item.id); openDialog('db', this);"
						>下載</button>
						<button
							class="btn btn-default"
							@click="check_inout(props.item.id, 'check_in')"
						>歸還</button>
					</template>
				</table-div>
			</div>
			<div id="book_shelf_checkin" class="tab-pane">
				<h3>借閱歷史紀錄</h3>
				<table-div :datas="checkin_list" :header="checkin_header">
				</table-div>
			</div>
		</div>
		<modal :id_modal="'db'">
			<template slot="header">
				<h4 class="modal-title">取得書籍</h4>
			</template>
			<template slot="body">
				<book_download
					pk="0"
					ref="db"
				>
				</book_download>
			</template>

			<template slot="footer">
				<button class="btn btn-primary" @click=" $refs.db.object_get()">確定</button>
			</template>

		</modal>
	</div>
</template>

<script>

	module.exports = {
		components: {
			'book_download': components['book_download'],
			'modal': components['modal'],
			'table-div': components['table-div'],
		},
		data: function() {
			return {
				checkout_header: {
					bookname: '書名',
					check_out_time: '借出日期',
					check_in_time: '到期日期',
					action: '動作',
				},
				checkout_list: [],
				checkin_header: {
					bookname: '書名',
					check_out_time: '借出日期',
					check_in_time: '到期日期',
				},
				checkin_list: [],
			}
		},
		computed: {},
		mounted: function () {
			document.title = '借閱書櫃';
			
			let self = this;
			rest_aj_send('get', '/ebookSystem/api/libraryrecords/', {'owner_id': user.id, 'status': 'true'})
			.done(function(data) {
				let filter_data = [];
				_.each(data['data'], function(v){

					try {
						filter_data.push({
							bookname: v.object.book_info.bookname,
							check_out_time: v.check_out_time.slice(0,10),
							check_in_time: v.check_in_time.slice(0,10),
							action: v,
						})
					} catch (exception) {
						console.log(`${exception.name}: ${exception.message}`)
					}

				})
				self.checkout_list = filter_data
			})

			rest_aj_send('get', '/ebookSystem/api/libraryrecords/', {'owner_id': user.id, 'status': 'false'})
			.done(function(data) {
				let filter_data = [];
				_.each(data['data'], function(v){

					try {
						filter_data.push({
							bookname: v.object.book_info.bookname,
							check_out_time: v.check_out_time.slice(0,10),
							check_in_time: v.check_in_time.slice(0,10),
						})
					} catch (exception) {
						console.log(`${exception.name}: ${exception.message}`)
					}

				})
				self.checkin_list = filter_data;
			})
		},
		methods: {
			check_inout: function (pk, action) {
				let self = this;

				rest_aj_send('post', '/ebookSystem/api/libraryrecords/' +pk +'/action/check_inout/', {'action': action,})
				.done(function(data) {
					let message = ''
					if(action==='check_in'){
						message = '成功歸還書籍'
						alertmessage('success', message)
						.done(function() {
							window.location.reload();
						})
					}
					if(action==='check_out'){
						message = '成功借閱書籍';
						alertmessage('success', message)
					}
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.message)
				})

			},
		},
	}
</script>
