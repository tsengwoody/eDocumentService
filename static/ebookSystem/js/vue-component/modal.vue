<template>
	<div class="modal fade" :id="id_modal" :ref="id_modal +'_instance'" role="dialog" aria-modal="true">
		<div :class="[ 'modal-dialog', modalSize ]" role="document">
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
					</slot>
				</div>
			</div>
		</div>
	</div>		
</template>

<script>
	module.exports = {
		props: {
			id_modal: String,	// define type
			size: {
				type: String,
				default: 'large',
			},
		},
		data() {
			return {
				// modalSize: 'modal-lg'

				modalSizeMap: {
					large: 'modal-lg',
					normal: '',
					small: 'modal-sm',
				},
				modalSize: 'modal-lg',
			}
		},
		mounted() {
			this.modalSize = this.modalSizeMap[this.size];
		},
		methods: {
			open: function(focusAfterClosed){
				openDialog(this.id_modal, focusAfterClosed)
			},
			close: function(){
				closeDialog(this.$refs[this.id_modal +'_instance'])
			},
		},
	}
</script>