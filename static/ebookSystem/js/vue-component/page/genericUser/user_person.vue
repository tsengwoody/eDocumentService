<template>
	<div id="user_person">
		<h3>個人資料</h3>
		<div class="form-horizontal">
			<template v-for="(value, key) in filter_data">
				<div class="form-group" v-if="key==='email'">
					<label class="control-label col-sm-2" :for="key"><font style="color:red">*</font><span>{|{ data_header[key] }|}</span></label>
					<div class="col-sm-4">
						<div class="input-group">
							<div class="likebtn">{|{ value }|}</div>
							<span class="input-group-btn">
								<button class="btn btn-success" disabled v-if="auth_email">已驗證</button>
								<button class="btn btn-warning" v-else
										@click="user_getOTP(userID, 'email')"
								>未驗證</button>
							</span>
						</div>
					</div>
				</div>
				<div class="form-group" v-else-if="key==='phone'">
					<label class="control-label col-sm-2" :for="key"><font style="color:red">*</font><span>{|{ data_header[key] }|}</span></label>
					<div class="col-sm-4">
						<div class="input-group">
							
							<div class="likebtn">{|{ value }|}</div>
							<span class="input-group-btn">
								<button class="btn btn-success" disabled v-if="auth_phone">已驗證</button>
								<button class="btn btn-warning" v-else
										@click="user_getOTP(userID, 'phone')"
								>未驗證</button>
							</span>
						</div>
					</div>
				</div>
				<div class="form-group" v-else>
					<label class="control-label col-sm-2" :for="key"><font style="color:red">*</font><span>{|{ data_header[key] }|}</span></label>
					<div class="col-sm-4">
						<div class="likebtn" :id="key">{|{ value }|}</div>
					</div>
				</div>
			</template>
			<div class="form-group">
				<label class="control-label col-sm-2"></label>
				<div class="col-sm-7">
					<button class="btn btn-primary" @click="usermodel(userID)">變更使用者資訊</button>
					<button
						class="btn btn-primary"
						@click="openDialog('spm', this);"
					>修改密碼</button>
						<button class="btn btn-primary"
						v-if="user.is_guest"
						@click="dm_bus.$emit('instance-set', user.disabilitycard_set[0]); openDialog('dm', this);"
					>
						<div v-if="user.disabilitycard_set[0]">手冊查閱編修</div>
						<div v-else>手冊新建登錄</div>
					</button>
					<button
						class="btn btn-primary"
						@click="
							$refs['fs'].open('user_person');
						"
					>字體設定</button>
				</div>
			</div>
		</div>
		<modal :id_modal="'spm'">
			<template slot="header">
				<h4 class="modal-title">修改密碼</h4>
			</template>   
			<template slot="body">
				<div class="form-horizontal">
					<set_password ref="spm"></set_password>
				</div>
			</template>
			<template slot="footer">
				<button class="btn btn-default"
					@click="change_password"
				>送出</button>
			</template>
		</modal>
		<modal :id_modal="'dm'">
			<template slot="header">
				<h4 class="modal-title">身心障礙手冊登錄</h4>
			</template>
			<template slot="body">
				<disabilitycard
					:bus="dm_bus"
				>
				</disabilitycard>
			</template>
			<template slot="footer">
				<button onclick="closeDialog(this)" class="btn btn-default" data-dismiss="modal">關閉</button>
			</template>
		</modal>
		<modal :id_modal="'fs'" :ref="'fs'">
			<template slot="header">
				<h4 class="modal-title">字體大小設定</h4>
			</template>
			<template slot="body">
				<div class="font-size-area" style="padding:20px 20px;">
					<span style="font-size: 1.2em;">設定文字大小:</span>
					<button class="font-size-default" @click="defautlFontSize">預設</button>
					<button class="font-size-up" @click="upFontSize">放大</button>
					<button class="font-size-down" @click="downFontSize">縮小</button>
					<span class="font-size-ratio">{|{ fontSizeRatio }|}</span>
				</div>
			</template>
		</modal>
	</div>
</template>
<script>

	const defautlFontSize = "htmlFontSize90";
	const percentage = [
		"htmlFontSize70",
	  	"htmlFontSize75",
		"htmlFontSize80",
		"htmlFontSize85",
		"htmlFontSize90",
		"htmlFontSize95",
		"htmlFontSize100",
		"htmlFontSize105",
		"htmlFontSize110"
	];

	module.exports = {
		components: {
			'disabilitycard': components['disabilitycard'],
			'modal': components['modal'],
			'set_password': components['set_password'],
		},
		data: function(){
			return {
				dm_bus: new Vue(),
				user: user,
				userID: user.id,
				filter_data: {
					username: user.username,
					first_name: user.first_name,
					last_name: user.last_name,
					email: user.email,
					phone: user.phone,
					birthday: user.birthday,
					education: user.education,
					is_book: user.is_book,
					org: user.org,
				},
				data_header: {
					username: '使用者名稱',
					first_name: '姓氏',
					last_name: '名字',
					email: '電子信箱',
					phone: '聯絡電話',
					birthday: '生日',
					education: '教育程度',
					is_book: '訂閱訊息',
					org: '所屬單位',
				},
				auth_email: user.auth_email,
				auth_phone: user.auth_phone,
				newRatio: '',
				percentageIndex: 0,
			}
		},
		mounted: function() {
			document.title = '個人資料';
			const self = this;
			const client = new $.RestClient('/genericUser/api/');
			client.add('organizations');
			
			client.organizations.read()
			.done(function (org_data) {
				_.each(org_data,function(v,k){
					if(self.filter_data['org'] == v['id']) {
						self.filter_data['org'] = v['name'];
					}
				})
			})

			const fontClass = document.querySelector('body').className;
			self.newRatio = fontClass;
			self.percentageIndex = percentage.indexOf(fontClass);
		},
		methods: {
			change_password: function() {
				this.$refs.spm.set_password(user.id);
				closeDialog(this.$refs.spm);
			},
			upFontSize() {
				if (this.percentageIndex < percentage.length -1) {
					this.percentageIndex += 1;
					this.updateFontSize();
				}
			},
			downFontSize() {
				if (this.percentageIndex > 0) {
					this.percentageIndex -= 1;
					this.updateFontSize();
				}
			},
			defautlFontSize() {
				this.percentageIndex = percentage.indexOf(defautlFontSize);
				this.updateFontSize();
			},
			updateFontSize() {
				this.newRatio =  percentage[ this.percentageIndex ];
				document.querySelector('body').className = this.newRatio;
				localStorage.setItem('fontSize', this.newRatio);
			}
		},
		computed: {
			fontSizeRatio() {
				console.log(typeof this.newRatio);
				return this.newRatio.substr(12) - 90;
			}
		}
	}
</script>

<style>
.font-size-area > .font-size-default,
.font-size-area > .font-size-up,
.font-size-area > .font-size-down {
	color: darkgray;
	font-size: 1.2em;
	margin-left: 0.3em;
	padding: 0.1em 0.5em;
	border: 1px solid lightgray;
	border-radius: 0.3em;

	background-color: white;
}

.font-size-area > .font-size-default:hover,
.font-size-area > .font-size-up:hover,
.font-size-area > .font-size-down:hover {
	color: white;
	background-color: darkgray;
}

.font-size-ratio {
	display: inline-block; 
	width: 2.5em; 
	text-align: center; 
	font-size: 3em; 
	border-radius: 0.2em; 
	border: 2px solid lightgray; 
	margin-left: 1em;
}
</style>