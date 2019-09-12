<template>
	<div class="form-group">
		<label class="control-label col-sm-2">起訖時間</label>

		<div class="col-sm-3">
		<label :for="'begin'"><font-awesome-icon icon="hourglass-start" class="textAside" />開始日期</label>
		<input
			:id="'begin'"
			type="text"
			v-model="begin"
			@input="out"
		>
		</div>
		<div class="col-sm-3">
		<label :for="'end'"><font-awesome-icon icon="hourglass-end" class="textAside" />結束日期</label>
		<input
			:id="'end'"
			type="text"
			v-model="end"
			@input="out"
		>
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
