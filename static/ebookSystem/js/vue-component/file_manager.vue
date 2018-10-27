<template>
	<div>
		<template>
			<table-div
				:header="file_manager_header"
				:datas="resource_file_datas"
			>
				<template slot="action" slot-scope="props">
					<button
						v-if="button_permission(user, 'read')"
						class="btn btn-default"
						@click="window.location.replace(url +props.item.name +'/')"
					>下載</button>
					<button
						v-if="button_permission(user, 'update')"
						class="btn btn-default"
						@click="
							resource_name=props.item.name;
							$refs.fu.change_mode('update');
							openDialog('fum', this);
						"
					>更新</button>
					<button
						v-if="button_permission(user, 'delete')"
						class="btn btn-default"
						@click="
							resource_name=props.item.name;
							$refs.fu.change_mode('delete');
							openDialog('fum', this);
						"
					>刪除</button>
				</template>
			</table-div>
			<button
				v-if="button_permission(user, 'create')"
				class="btn btn-default"
				@click="
					resource_name='';
					$refs.fu.change_mode('create');
					openDialog('fum', this);
				"
			>新建</button>
		</template>
		<template>
			<file_upload
				ref="fu"
				:url="url"
				:resource_name="resource_name"
				@change="get_resource_file_datas()"
			>
			</file_upload>
		</template>
	</div>
</template>
<script>

	module.exports = {
		props: ['url', 'permission',],
		components: {
			'table-div': httpVueLoader('/static/ebookSystem/js/vue-component/table-div.vue'),
			'file_upload': httpVueLoader('/static/ebookSystem/js/vue-component/file_upload.vue'),
		},
		data: function(){
			return {
				file_manager_header: {
					'order': '序號',
					'name': '檔案名稱',
					'size': '檔案大小',
					'mtime': '修改日期',
					'action': '動作',
				},
				resource_file_datas: [],
				resource_name: '',
			}
		},
		computed: {
		},
		mounted: function () {
			this.get_resource_file_datas()
		},
		methods: {
			button_permission: function(u, crud){
				p = this.permission
				if(u.is_editor&&p[crud].is_editor){ return true }
				else if(u.is_guest&&p[crud].is_guest){ return true }
				else if(u.is_manager&&p[crud].is_manager){ return true }
				else if(p[crud].is_all){ return true }
				else {return false}
			},
			get_resource_file_datas: function(resource_name){
				let self = this

				self.resource_file_datas = []
				rest_aj_send('get', self.url, {})
				.done(function(data) {
					index = 0
					_.each(data['data'], function(v){
						self.resource_file_datas.push({
							'order': index,
							'name': v.name,
							'size': v.size,
							'mtime': v.mtime.slice(0,10),
							'action': v,
						})
						index = index +1
					})
				})
				.fail(function(xhr, result, statusText){
					console.log(xhr)
				})
			},
		},
	}

</script>