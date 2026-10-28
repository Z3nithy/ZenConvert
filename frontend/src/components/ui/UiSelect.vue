<script setup>
import { computed, useId } from 'vue'

defineOptions({ inheritAttrs: false })

const props = defineProps({
  modelValue: {
    type: [String, Number],
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
  description: {
    type: String,
    default: '',
  },
  error: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])
const generatedId = useId()
const selectId = computed(() => props.id || `ui-select-${generatedId}`)
const descriptionId = computed(() =>
  props.description ? `${selectId.value}-description` : undefined,
)
const errorId = computed(() => (props.error ? `${selectId.value}-error` : undefined))
const describedBy = computed(
  () => [descriptionId.value, errorId.value].filter(Boolean).join(' ') || undefined,
)

function updateValue(event) {
  const value = event.target.value
  const parsedValue = typeof props.modelValue === 'number' && value !== '' ? Number(value) : value
  emit('update:modelValue', parsedValue)
}
</script>

<template>
  <div class="ui-field">
    <label class="ui-field__label" :for="selectId">{{ label }}</label>
    <select
      v-bind="$attrs"
      :id="selectId"
      class="ui-field__control"
      :value="modelValue"
      :aria-invalid="error ? 'true' : undefined"
      :aria-describedby="describedBy"
      @change="updateValue"
    >
      <slot />
    </select>
    <p v-if="description" :id="descriptionId" class="ui-field__description">{{ description }}</p>
    <Transition name="ui-feedback">
      <p v-if="error" :id="errorId" class="ui-field__message--error" role="alert">
        {{ error }}
      </p>
    </Transition>
  </div>
</template>
