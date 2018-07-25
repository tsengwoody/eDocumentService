{% include 'comp/drf.vue' %}
<template id="disabilitycard">
<div id="disabilitycard_register" class="container">
	<div class="row">
		<div class="col-sm-4 col-md-4">
			<img v-if="img_base64_front"
				:src="'data:image/jpeg;base64,' + img_base64_front"
				:base64="img_base64_front"
				alt="身心障礙手冊正面"
				class=img-thumbnail
			>
			<img v-else
				:src="url +'resource/source/front'"
				alt="身心障礙手冊正面"
				class=img-thumbnail
			>
			<input
				v-if="mode==='create' || mode==='update'"
				@change="ch_img($event.target,'front')"
				id="id_front"
				type="file"
			>
			<img v-if="img_base64_back"
				:src="'data:image/jpeg;base64,' + img_base64_back"
				:base64="img_base64_back"
				alt="身心障礙手冊反面"
				class=img-thumbnail
			>
			<img v-else
				:src="url +'resource/source/back'"
				alt="身心障礙手冊反面"
				class=img-thumbnail
			>
			<input
				v-if="mode==='create' || mode==='update'"
				@change="ch_img($event.target,'back')"
				type="file"
				id="id_back"
			>
		</div>

		<div class="col-sm-6 col-md-6">
			<div class="form-horizontal" v-if="mode==='read' || mode==='update'">
				<div class="form-group">
					<label for="id_status" class="col-sm-3">狀態</label>
					<div class="col-sm-9">
						<p v-if="disabilitycard.is_active">啟用</p>
						<p v-if="!disabilitycard.is_active">停用</p>
					</div>
				</div>
			</div>

			<div v-if="!iser(model_info)" class="form-horizontal">
				<drf-model
						v-if="mode==='read' || mode==='update'"
						:keys="'identity_card_number'"
						:model_info="model_info.identity_card_number"
					mode="read"
					v-model="disabilitycard_temp.identity_card_number"
				></drf-model>
				<drf-model
						v-if="mode==='create'"
						:keys="'identity_card_number'"
						:model_info="model_info.identity_card_number"
					mode="write"
					v-model="disabilitycard_temp.identity_card_number"
				></drf-model>

				<drf-model
					v-for="item in ['owner', 'name', 'address', 'category', 'level', 'identification_date', 'renew_date',]"
					v-if="mode==='read'"
					:keys="item"
					:model_info="model_info[item]"
					mode="read"
					v-model="disabilitycard_temp[item]"
				></drf-model>
				<drf-model
					v-for="item in ['owner', 'name', 'address', 'category', 'level', 'identification_date', 'renew_date',]"
					v-if="mode==='create' || mode==='update'"
					:keys="item"
					:model_info="model_info[item]"
					mode="write"
					v-model="disabilitycard_temp[item]"
				></drf-model>
			</div>

			<div
				v-if="mode==='create'"
			>
				<button
					@click="create()"
					class="btn btn-default" 
				>新建</button>
			</div>

			<div
				v-if="mode==='update'"
			>
				<button
					@click="cancel()"
					class="btn btn-default" 
				>取消</button>
				<button
					@click="update()"
					class="btn btn-default" 
				>更新</button>
			</div>

			<div
				v-if="mode==='read'"
			>
				<button
					@click="mode_change('update')"
					class="btn btn-default" 
				>編輯</button>
				<template v-if="user.is_manager">
					<button
						v-if="!disabilitycard.is_active"
						@click="active(true)"
						class="btn btn-default" 
					>啟用</button>
					<button
						v-if="disabilitycard.is_active"
						@click="active(false)"
						class="btn btn-default" 
					>停用</button>
				</template>
			</div>

		</div>
	</div>
</div>
</template>
<script>
	let convertTitle = {
		"owner": "擁有者",
		"identity_card_number": "身分證字號",
		"name": "姓名",
		"address": "地址",
		"identification_date": "鑑定日期",
		"renew_date": "有效日期",
		"level": "程度",
		"category": "類別",
	};

	Vue.options.delimiters = ['{|{', '}|}'];

	Vue.component('disabilitycard', {
		template: '#disabilitycard',
		props: ['bus',],
		data: function(){
			return {
				mode: 'read',
				pk: '',
				disabilitycard: {
					"identity_card_number": "",
					"name": "",
					"address": "",
					"identification_date": "",
					"renew_date": "",
					"level": "",
					"category": "",
					"owner": "",
					is_active: '',
				},
				model_info: {},
				disabilitycard_temp: {
					"identity_card_number": "",
					"name": "",
					"address": "",
					"identification_date": "",
					"renew_date": "",
					"level": "",
					"category": "",
					"owner": "",
					is_active: '',
				},
				img_base64_front: '',
				img_base64_back: '',
				user_list: [],
			}
		},
		computed: {
			url: function(){
				if(this.pk===-1){
					return '/genericUser/api/disabilitycards/'
				}
				else {
					return '/genericUser/api/disabilitycards/' +this.pk +'/'
				}
			},
		},
		created: function () {
			this.bus.$on('instance-set', this.instance_set)
			let self = this
			self.client = new $.RestClient('/genericUser/api/')
			self.client.add('users');
			self.client.add('disabilitycards');
			self.client.addVerb('disabilitycardsoption', 'OPTIONS', {
				url: 'disabilitycards',
			});

			self.client.users.read()
			.done(function(data) {
				_.each(data, function(v){
					self.user_list.push({
						'display_name': v.username,
						'value': v.id,
					})
				})
			})

		},
		mounted: function () {
			let self = this

			self.client.disabilitycardsoption()
			.done(function(data) {
				self.model_info = _.clone(data.actions.POST)
				self.model_info.owner.choices = self.user_list
			})
		},
		methods: {
			instance_set: function (event) {
				console.log(event)
				this.pk = event

				if(iser(this.pk)){
					this.mode = 'create'
					this.disabilitycard = {}
					this.disabilitycard_temp = _.clone(this.disabilitycard)
				}
				else {
					this.refresh()
				}
			},
			refresh: function () {
				this.mode = 'read'
				let self = this
					self.client.disabilitycards.read(self.pk)
					.done(function(data) {
						_.each(self.disabilitycard, function(v,k){
							self.disabilitycard[k] = data[k]
							//self.disabilitycard_temp[k] = data[k]
						})
						self.disabilitycard_temp = _.clone(self.disabilitycard)
					})
					.fail(function(xhr, result, statusText){
						self.mode = 'create'
					})

			},
			active: function (status) {
				let self = this
				self.disabilitycard.is_active = self.disabilitycard_temp.is_active = status
				//rest_aj_send('put', self.url, self.disabilitycard)
				self.client.disabilitycards.update(self.pk, self.disabilitycard)
				.done(function(data) {
					if(status){ alertmessage('success', '成功啟用手冊') }
					else if(!status){ alertmessage('success', '成功停用手冊') }
				})
				.fail(function(data){
				    alertmessage('error', data['message']);
				})

			},
			create: function () {
				let self = this

				self.client.disabilitycards.create(self.disabilitycard_temp)
				.done(function(data) {
					alertmessage('success', '成功新建手冊')
					self.pk = data.identity_card_number
					self.refresh()
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})

			},
			cancel: function () {
				let self = this
				self.disabilitycard_temp = _.clone(self.disabilitycard)
				self.mode_change('read');
				self.img_base64_front = '';
				self.img_base64_back = '';
			},
			update: function () {
				let self = this

				self.disabilitycard = _.clone(self.disabilitycard_temp)
				self.client.disabilitycards.update(self.pk, self.disabilitycard)
				.done(function(data) {
					alertmessage('success', '成功修改手冊資料')
					self.mode_change('read')
					self.upload(self.pk)
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})

			},
			mode_change: function (mode) {
				this.mode = mode
			},
			ch_img: function(me, kind){
				let self = this;

				readfile(me)
				.done(function (bs) {
					let v = bin2base64(bs2barr(bs));
					if(kind==='front') self.img_base64_front = v;
					else self.img_base64_back = v;
					// cv_img_set(kind, v)
				})
			},
			upload: function(pk){
				let self = this
				let resource_url = '/genericUser/api/disabilitycards/' +pk +'/resource/source/'

				let fileFront = document.getElementById('id_front');
				let aj_front = null
				fileFrontObject = fileFront.files[0]
				if(!iser(fileFrontObject)){
					aj_front = rest_aj_upload(resource_url +'front/', {'object': fileFrontObject})
				}

				let fileBack = document.getElementById('id_back');
				let aj_back = null
				fileBackObject = fileBack.files[0]
				if(!iser(fileBackObject)){
					aj_back = rest_aj_upload(resource_url +'back/', {'object': fileBackObject})
				}

				if(!iser(aj_front) && !iser(aj_back)){
					$.when(aj_front, aj_back)
					.done(function(front_data, back_data) {
						alertmessage('success', '成功上傳手冊')
					})
					.fail(function(data){
						alertmessage('error', '失敗上傳手冊')
					})
				}
				else if(!iser(aj_front)){
					aj_front
					.done(function(data) {
						alertmessage('success', '成功上傳手冊正面')
					})
					.fail(function(data){
						alertmessage('error', '失敗上傳手冊正面')
					})
				}
				else if(!iser(aj_back)){
					aj_back
					.done(function(data) {
						alertmessage('success', '成功上傳手冊反面')
					})
					.fail(function(data){
						alertmessage('error', '失敗上傳手冊反面')
					})
				}
			},
		},

	})

</script>