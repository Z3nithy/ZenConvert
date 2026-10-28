<script setup>
import { computed, useId } from 'vue'

defineOptions({ inheritAttrs: false })

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  id: {
    type: String,
    default: '',
  },
  label: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    default: 'text',
  },
  placeholder: {
    type: String,
    default: '',
  },
  description: {
    type: String,
    default: '',
  },
  error: {
    type: String,
    default: '',
  },
  success: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])
const generatedId = useId()
const inputId = computed(() => props.id || `ui-input-${generatedId}`)
const descriptionId = computed(() =>
  props.description ? `${inputId.value}-description` : undefined,
)
const errorId = computed(() => (props.error ? `${inputId.value}-error` : undefined))
const successId = computed(() => (props.success ? `${inputId.value}-success` : undefined))
const describedBy = computed(
  () =>
    [descriptionId.value, errorId.value || successId.value].filter(Boolean).join(' ') || undefined,
)
</script>

<template>
  <div class="ui-field">
    <label class="ui-field__label" :for="inputId">{{ label }}</label>
    <input
      v-bind="$attrs"
      :id="inputId"
      class="ui-field__control"
      :class="{ 'ui-field__control--success': success && !error }"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :aria-invalid="error ? 'true' : undefined"
      :aria-describedby="describedBy"
      @input="emit('update:modelValue', $event.target.value)"
    />
    <p v-if="description" :id="descriptionId" class="ui-field__description">{{ description }}</p>
    <Transition name="ui-feedback">
      <p v-if="error" :id="errorId" class="ui-field__message--error" role="alert">
        {{ error }}
      </p>
    </Transition>
    <Transition name="ui-feedback">
      <p v-if="!error && success" :id="successId" class="ui-field__message--success">
        {{ success }}
      </p>
    </Transition>
  </div>
</template>
