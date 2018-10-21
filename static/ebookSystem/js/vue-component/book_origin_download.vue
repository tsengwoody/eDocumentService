<template>
	<div class="form-horizontal">
		<form-drf 
			:model_info="model_info.fileformat"
			:field="'fileformat'"
			v-model="fileformat"
		></form-drf>

		<form-drf 
			:model_info="model_info.password"
			:field="'password'"
			v-model="password"
		></form-drf>
	</div>
</template>
<script>

function post(path, params, method) {
	method = method || "post"; // Set method to post by default if not specified.

	// The rest of this code assumes you are not using a library.
	// It can be made less wordy if you use one.
	var form = document.createElement("form");
	form.setAttribute("method", method);
	form.setAttribute("action", path);

	for(var key in params) {
		if(params.hasOwnProperty(key)) {
			var hiddenField = document.createElement("input");
			hiddenField.setAttribute("type", "hidden");
			hiddenField.setAttribute("name", key);
			hiddenField.setAttribute("value", params[key]);

			form.appendChild(hiddenField);
		}
	}

	document.body.appendChild(form);
	form.submit();
}

	module.exports = {
		props: ['pk',],
		components: {
			'form-drf': httpVueLoader('/static/ebookSystem/js/vue-component/form.vue'),
		},
		data: function(){
			return {
				fileformat: 'epub',
				password: '',
				model_info: {
					fileformat: {
						label: '類型',
						type: 'select',
						choices: [
							{
								display_name: '電子書(epub)',
								value: 'epub',
							},
							{
								display_name: '純文字(txt)',
								value: 'txt',
							},
						],
					},
					password: {
						label: '密碼',
						type: 'password',
					},
				},
			}
		},
		created: function () {
			let self = this;
		},
		mounted: function () {
			this.refresh();
		},
		methods: {
			instance_set: function (event) {
				this.pk = event;
				this.refresh();
			},
			refresh: function () {
				this.fileformat = 'epub';
				this.password = '';
			},
			object_get: function () {
				let self = this;

				let authenticate_url = '/genericUser/api/users/action/authenticate/';
				rest_aj_send('post', authenticate_url, {'username': user.username, 'password': this.password,})
				.done(function(data) {
					let url = '/ebookSystem/api/books/' +self.pk +'/action/download/';
					let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
					post(url, {fileformat: self.fileformat, password: self.password, csrfmiddlewaretoken: csrf}, 'post')
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', '失敗使用者驗證')
				})

			},
		},
	};

</script>