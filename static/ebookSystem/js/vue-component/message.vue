<template>
	<div class="modal fade" id="message" ref="message" role="dialog" aria-modal="true" @keydown.esc="close">
		<div :class="[ 'modal-dialog']" role="document">
			<div class="modal-content alert-info" style="background-color: #f5f5f5;">
				<div class="modal-header">
					<button @click="close" class="close" data-dismiss="modal" aria-label="Close"><span>&times;</span></button>
					<h4 class="modal-title">系統訊息</h4>
				</div>
				<div class="modal-body">
					{{ message }}
				</div>
				<div class="modal-footer">
					<button @click="ok" class="btn btn-default" data-dismiss="modal">確定</button>
				</div>
			</div>
		</div>
	</div>		
</template>

<script>

module.exports = {
	data(){
		return {
			isShow: false,
			promise: null,
			message: '',
		}
	},
	watch: {
		isShow(){
			if(!this.isShow){
				closeDialog(this.$refs['message'])
			}
			else {
				openDialog('message', 'app')
			}
		},
	},
	created() {
		this.$root.$message = this;
	},
	mounted(){
	},
	methods: {
		open({message, }){
			this.message = message;
			this.isShow = true;
			this.promise = new Promise((resolve, reject) => {
				this.$on('cancel', () => {
					console.log('Cancel!');
					reject();
				});
				this.$on('ok', () => {
					console.log('Ok!');
					resolve();
				});
			} );
			return this.promise;
		},
		close() {
			this.isShow = false;
			this.$emit('ok');
		},
		cancel(){
			this.isShow = false;
			this.$emit('cancel');
		},
		ok(){
			this.isShow = false;
			this.$emit('ok');
		},
	}
};
</script>