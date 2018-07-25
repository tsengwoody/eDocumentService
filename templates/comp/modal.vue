<template id="modal-template">
	<div class="modal fade" :id="id_modal" role="dialog" aria-modal="true">
		<div class="modal-dialog modal-lg" role="document">
			<div class="modal-content alert-info" style="background-color: #f5f5f5;">
				<div class="modal-header">
					<button onclick="closeDialog(this)" class="close" data-dismiss="modal" aria-label="Close"><span>&times;</span></button>
					<slot name="header">
						<h4 class="modal-title">Modal title</h4>
					</slot>
				</div>
				<div class="modal-body">
					<slot name="body">
						<p>default body</p>
					</slot>
				</div>
				<div class="modal-footer">
					<slot name="footer">
						<button onclick="closeDialog(this)" class="btn btn-default" data-dismiss="modal">關閉</button>
						<button class="btn btn-primary">儲存</button>
					</slot>
				</div>
			</div>
		</div>
	</div>		
</template>

<script>
	Vue.options.delimiters = ['{|{', '}|}'];
	Vue.component('modal', {
		template: '#modal-template',
		props: {
			id_modal: String,	// define type
		},
	});
</script>