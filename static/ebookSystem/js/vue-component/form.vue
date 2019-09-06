<template>
	<div class="form-group">
		<label :class="['control-label', labelClass, offsetClass]" :for="field"><span>{{ model_info.label }}</span></label>
		<div :class="[inputClass]">
			<input
				v-if="model_info.type === 'text' || model_info.type === 'email' || model_info.type === 'password'"
				class="form-control" 
				:type="model_info.type" 
				:id="field"
				:value="value"
				@input="$emit('input', $event.target.value)"
				:required="model_info.required"
			>

			<input
				v-if="model_info.type === 'checkbox'"
				:type="model_info.type" 
				:id="field"
				:value="value"
				@change="$emit('input', $event.target.checked)"
				:checked="value == true"
				style="height: 30px; line-height: 30px;"
				:required="model_info.required"
			>

			<el-date-picker v-if="model_info.type === 'date'"
				:id="field"
				:value="value"
				@input="$emit('input', $event)"
				value-format="yyyy-MM-dd"   
				placeholder="yyyy-MM-dd"
				size=small
				style="width: 100%;"
			></el-date-picker>

			<select v-if="model_info.type === 'select'"
				class="form-control"
				:id="field"
				:value="value"
				@input="$emit('input', $event.target.value)"
			>
				<option
					v-for="el in model_info.choices"
					:value="el.value"
				>
					{{ el.display_name }}
				</option>
			</select>

			<template
				v-if="model_info.type === 'radio'" 
				v-for="el in model_info.choices"
			>
				
				<label class="radio-inline">
				<input 
					type="radio" 
					:id="el.value"
					:value="el.value"
					@input="$emit('input', $event.target.value)"
					:checked="el.value == value"
				> 
					{{ el.display_name }}
				</label>
			</template>

			<textarea v-if="model_info.type === 'textarea'"
				class="form-control" 
				:id="field"
				:value="value"
				@input="$emit('input', $event.target.value)"
				rows="10"
			>
				
			</textarea>
		</div>
		<label v-if="!iser(model_info.remark)" class="control-label col-sm-4" :for="field" style="text-align:left;"><font style="color:red">{{ model_info.remark }}</font></label>
	</div>
</template>

<script>
	module.exports = {
		props: {
			model_info: Object,
			field: String,
			value: [String, Boolean],
			
			offsetClass: {
				type: String,
				default: '',
			},
			labelClass: {
				type: String,
				default: 'col-sm-2',
			},
			inputClass: {
				type: String,
				default: 'col-sm-3',
			},
		},
		methods: {

		},
		mounted() {
		}
	};

</script>