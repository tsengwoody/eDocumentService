<template>
	<div class="form-horizontal">
		<div class="form-group">
			<label class="control-label col-sm-4">搜尋</label>
			<div class="col-sm-4">
				<input type="text" class="form-control" v-model="filter_word">
			</div>
			<div class="col-sm-2">
				<button class="btn btn-primary" @click="filter_user">確認</button>
			</div>
		</div>

		<div class="form-group">
			<label class="control-label col-sm-4">選擇使用者</label>
			<div class="col-sm-4">
				<select class="form-control" v-model="assign_user">
					<option value="">---</option>
					<template v-if="!iser(users)" v-for="(user, index) in users">
						<option
							:value="user.username"
						>
							{|{ user.username }|}
						</option>
					</template>
				</select>
			</div>
			<div class="col-sm-4">
				<input class="form-control" v-model="assign_user"/>
			</div>
		</div>
		<div class="form-group">
			<label class="control-label col-sm-4">預定完成時間</label>
			<div class="col-sm-4">
				<el-date-picker 
					v-model="deadline"
					type="date"
					value-format="yyyy-MM-dd"   
					placeholder="yyyy-MM-dd"
				></el-date-picker>
			</div>
		</div>
	</div>
</template>

<script>

	module.exports = {
		props: ['isbn_part'],
		data(){
			return {
				// assign data
				assign_user: '',
				deadline: '',	
				users: [],		 // present users
				orig_users: [],  // save api source users
				filter_word: '',
			}
		},
		methods: {
			instance_set(pk){
				this.isbn_part = pk;
			},
			save_assign(){
				ebookSystemAPI.ebookAction.assign(this.isbn_part, {
					username: this.assign_user,
					deadline: this.deadline,
				})
				.then(res => {
					alertmessage('success', res.data['detail'])
					.done(() => {
						location.reload()
					})
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})

			},
			filter_user(){
				let vo = this;
				vo.filter_word = vo.filter_word.trim();
				let filtered_users = vo.orig_users.filter(function(item, index, array){
					return item['username'].indexOf(vo.filter_word) !== -1 ;
				})
				vo.users = filtered_users;
			}
		},

		created () {
			let vo = this;
			rest_aj_send('get', '/genericUser/api/users/', {})
			.done(function(data) {
				_.each(data.data, function(v, k){
					vo.users.push({
						id: v['id'],
						username: v['username']
					})
					
				})
			})

			vo.orig_users = vo.users;

			let d = new Date();
			// deadline default 今天+3天
			vo.deadline = d.getFullYear()+'-'+(d.getMonth() + 1)+'-'+(d.getDate()+3); 
		},
		mounted () {
			//this.bus.$on('submit', this.save_assign)
		}
	};

</script>