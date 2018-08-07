{% include 'comp/drf.vue' %}
{% include 'dev/form.vue' %}

<template id="book_download">
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

	Vue.options.delimiters = ['{|{', '}|}'];

	Vue.component('book_download', {
		template: '#book_download',
		props: ['pk',],
		data: function(){
			return {
				fileformat: 'epub',
				password: '',
				model_info: {
					'fileformat': {
						'label': '類型',
						'type': 'select',
						'choices': [
							{
								'display_name': '電子書(epub)',
								'value': 'epub',
							},
							{
								'display_name': '純文字(txt)',
								'value': 'txt',
							},
						],
					},
					password: {
						'label': '密碼',
						'type': 'password',
					},
				},
			}
		},
		created: function () {
			let self = this
		},
		mounted: function () {
			this.refresh()
		},
		methods: {
			instance_set: function (event) {
				this.pk = event
				this.refresh()
			},
			refresh: function () {
				this.fileformat = 'epub'
				this.password = ''
			},
			object_get: function () {
				let self = this
				let url = '/ebookSystem/api/libraryrecords/' +self.pk +'/action/download/'
				let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
				//let csrf = $('input[name=csrfmiddlewaretoken]').val();
				post(url, {'fileformat': this.fileformat, 'password': this.password, 'csrfmiddlewaretoken': csrf}, 'post')
			},
		},
	})

</script>