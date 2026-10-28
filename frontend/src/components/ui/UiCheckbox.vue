<script setup>
import { computed, useId } from 'vue'

defineOptions({ inheritAttrs: false })

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
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
const inputId = computed(() => props.id || `ui-checkbox-${generatedId}`)
const descriptionId = computed(() =>
  props.description ? `${inputId.value}-description` : undefined,
)
const errorId = computed(() => (props.error ? `${inputId.value}-error` : undefined))
const describedBy = computed(
  () => [descriptionId.value, errorId.value].filter(Boolean).join(' ') || undefined,
)
</script>

<template>
  <div>
    <label class="ui-check" :for="inputId">
      <input
        v-bind="$attrs"
        :id="inputId"
        class="ui-check__input"
        type="checkbox"
        :checked="modelValue"
        :aria-invalid="error ? 'true' : undefined"
        :aria-describedby="describedBy"
        @change="emit('update:modelValue', $event.target.checked)"
      />
      <span class="ui-check__copy">
        <span class="ui-check__label">{{ label }}</span>
        <span v-if="description" :id="descriptionId" class="ui-check__description">
          {{ description }}
        </span>
      </span>
    </label>
    <p v-if="error" :id="errorId" class="ui-field__message--error" role="alert">{{ error }}</p>
  </div>
</template>
