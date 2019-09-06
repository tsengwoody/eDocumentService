<template>
	<div class="dateCtnr">
		<label :for="'begin' +id"><font-awesome-icon icon="hourglass-start" class="textAside" />開始日期</label>
		<input
			:id="'begin' +id"
			type="text"
			v-model="begin"
			@input="out"
		>
		<label :for="'end' +id"><font-awesome-icon icon="hourglass-end" class="textAside" />結束日期</label>
		<input
			:id="'end' +id"
			type="text"
			v-model="end"
			@input="out"
		>
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
			id: -Math.floor(Math.random() * 100000000).toString(),
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
	@import '../style/base.scss';

	.dateCtnr {
		display: grid;
		grid-template-columns: auto auto;
		justify-content: left;
		justify-items: center;
		grid-column-gap: $spaceS4;
		grid-row-gap: $spaceS2;
	}
</style>
