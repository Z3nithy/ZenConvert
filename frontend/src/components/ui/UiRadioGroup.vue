<script setup>
import { computed, useId } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  name: {
    type: String,
    default: '',
  },
  legend: {
    type: String,
    required: true,
  },
  options: {
    type: Array,
    required: true,
    validator: (items) =>
      items.every(
        (item) =>
          item &&
          Object.prototype.hasOwnProperty.call(item, 'value') &&
          typeof item.label === 'string' &&
          (item.disabled === undefined || typeof item.disabled === 'boolean'),
      ),
  },
  error: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])
const generatedId = useId()
const groupName = computed(() => props.name || `ui-radio-${generatedId}`)
</script>

<template>
  <fieldset
    class="ui-radio-group"
    :aria-invalid="error ? 'true' : undefined"
    :aria-describedby="error ? `${groupName}-error` : undefined"
  >
    <legend class="ui-radio-group__legend">{{ legend }}</legend>
    <div class="ui-radio-group__options">
      <label v-for="option in options" :key="String(option.value)" class="ui-check">
        <input
          class="ui-check__input"
          type="radio"
          :name="groupName"
          :value="option.value"
          :checked="modelValue === option.value"
          :disabled="option.disabled"
          :aria-invalid="error ? 'true' : undefined"
          @change="emit('update:modelValue', option.value)"
        />
        <span class="ui-check__copy">
          <span class="ui-check__label">{{ option.label }}</span>
          <span v-if="option.description" class="ui-check__description">
            {{ option.description }}
          </span>
        </span>
      </label>
    </div>
    <p v-if="error" :id="`${groupName}-error`" class="ui-field__message--error" role="alert">
      {{ error }}
    </p>
  </fieldset>
</template>
