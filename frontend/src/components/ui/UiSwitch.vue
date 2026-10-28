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
  disabled: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue'])
const generatedId = useId()
const inputId = computed(() => props.id || `ui-switch-${generatedId}`)
</script>

<template>
  <label class="ui-switch" :for="inputId">
    <input
      v-bind="$attrs"
      :id="inputId"
      class="ui-switch__input"
      type="checkbox"
      role="switch"
      :checked="modelValue"
      :disabled="disabled"
      @change="emit('update:modelValue', $event.target.checked)"
    />
    <span class="ui-switch__track" aria-hidden="true">
      <span class="ui-switch__thumb"></span>
    </span>
    <span class="ui-switch__label">{{ label }}</span>
  </label>
</template>
