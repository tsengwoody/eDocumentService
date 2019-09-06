<template>
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
					v-if="!disabilitycard_temp.is_active"
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

	module.exports = {
		props: ['bus',],
		components: {
			'drf-model': components['drf'],
		},
		data(){
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
			url(){
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
		},
		mounted(){

			genericUserAPI.userRest.list()
			.then(res => {
				_.each(res.data, (v) => {
					this.user_list.push({
						'display_name': v.username,
						'value': v.id,
					})
				})
			})

			genericUserAPI.disabilityCardRest.options()
			.then(res => {
				this.model_info = _.clone(res.data.actions.POST);
				this.model_info.owner.choices = this.user_list
				this.model_info.identity_card_number.label = '身份證字號'
				this.model_info.owner.label = '擁有者'
				this.model_info.owner.label = '擁有者'
				this.model_info.name.label = '姓名'
				this.model_info.address.label = '地址'
				this.model_info.category.label = '類別'
				this.model_info.identification_date.label = '鑑定日期'
				this.model_info.renew_date.label = '重新鑑定日期'
				this.model_info.level.label = '程度'
			})

		},
		methods: {
			instance_set(event){
				this.pk = event
				if(!this.pk){
					this.mode = 'create'
					_.each(this.disabilitycard, (v, k) => {
						this.disabilitycard[k] = ''
					})
					_.each(this.disabilitycard_temp, (v, k) => {
						this.disabilitycard_temp[k] = ''
					})
				}
				else {
					this.refresh()
				}
			},
			refresh(){
				this.mode = 'read'

				genericUserAPI.disabilityCardRest.read(this.pk)
				.then(res => {
					_.each(this.disabilitycard, (v,k) => {
						this.disabilitycard[k] = res.data[k]
						this.disabilitycard_temp[k] = res.data[k]
					})
					this.img_base64_front = null
					this.img_base64_back = null
				})
				.catch(res => {
					this.mode = 'create'
					alertmessage('error', o2j(res.response.data));
				})
			},
			active(status){
				this.disabilitycard.is_active = this.disabilitycard_temp.is_active = status
				genericUserAPI.disabilityCardRest.partialupdate(this.pk, {'is_active' :status})
				.then(res => {
					if(status){ alertmessage('success', '成功啟用手冊') }
					else if(!status){ alertmessage('success', '成功停用手冊') }
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			create(){
				this.disabilitycard_temp.is_active = 'false'
				genericUserAPI.disabilityCardRest.create(this.disabilitycard_temp)
				.then(res => {
					alertmessage('success', '成功新建手冊')
					this.pk = res.data.identity_card_number
					this.upload(this.pk)
					this.refresh()
					this.bus.$emit('instance-refresh', 'refresh')
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			update(){
				this.disabilitycard = _.clone(this.disabilitycard_temp)
				genericUserAPI.disabilityCardRest.update(this.pk, this.disabilitycard)
				.then(res => {
					alertmessage('success', '成功修改手冊資料')
					this.mode_change('read')
					this.upload(this.pk)
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			cancel(){
				this.disabilitycard_temp = _.clone(this.disabilitycard)
				this.mode_change('read');
				this.img_base64_front = '';
				this.img_base64_back = '';
			},
			mode_change(mode){
				this.mode = mode
			},
			ch_img(me, kind){
				let self = this;

				readfile(me)
				.done((bs) => {
					let v = bin2base64(bs2barr(bs));
					if(kind==='front') this.img_base64_front = v;
					else this.img_base64_back = v;
				})
			},
			upload(pk){
				let resource_url = '/genericUser/api/disabilitycards/' +pk +'/resource/source/'

				let fileFront = document.getElementById('id_front');
				let aj_front = null
				fileFrontObject = fileFront.files[0]
				if(fileFrontObject){
					aj_front = rest_aj_upload(resource_url +'front/', {'object': fileFrontObject})
				}

				let fileBack = document.getElementById('id_back');
				let aj_back = null
				fileBackObject = fileBack.files[0]
				if(fileBackObject){
					aj_back = rest_aj_upload(resource_url +'back/', {'object': fileBackObject})
				}

				if(aj_front && aj_back){
					$.when(aj_front, aj_back)
					.done((front_data, back_data) => {
						alertmessage('success', '成功上傳手冊')
					})
					.fail((data) => {
						alertmessage('error', '失敗上傳手冊')
					})
				}
				else if(aj_front){
					aj_front
					.done((data) => {
						alertmessage('success', '成功上傳手冊正面')
					})
					.fail((data) => {
						alertmessage('error', '失敗上傳手冊正面')
					})
				}
				else if(aj_back){
					aj_back
					.done((data) => {
						alertmessage('success', '成功上傳手冊反面')
					})
					.fail((data) => {
						alertmessage('error', '失敗上傳手冊反面')
					})
				}
			},
		},
	}

</script>