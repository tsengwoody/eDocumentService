<template>
	<div class="form-group">
		<label class="control-label col-sm-2">起訖時間</label>

		<div class="col-sm-3">
			<el-date-picker
				v-model="begin"
				value-format="yyyy-MM-dd"   
				placeholder="yyyy-MM-dd"
				size=small
				style="width: 100%;"
			></el-date-picker>
		</div>
		
		<div class="col-sm-3">
			<el-date-picker
				v-model="end"
				value-format="yyyy-MM-dd"   
				placeholder="yyyy-MM-dd"
				size=small
				style="width: 100%;"
			></el-date-picker>
		</div>
	</div>
</template>

<script>
module.exports = {
	props: {
		value: {
			begin: '',
			end: '',
		},
	},
	components: {
	},
	data() {
		return {
			begin: '',
			end: '',
		};
	},
	mounted() {
	},
	methods: {
		out(){
			this.$emit('input', {
				begin: this.begin,
				end: this.end,
			})
		},
	},
};
</script>

<style>

</style>
