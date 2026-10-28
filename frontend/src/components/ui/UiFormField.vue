<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  forId: {
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

const descriptionId = computed(() => (props.description ? `${props.forId}-description` : undefined))
const errorId = computed(() => (props.error ? `${props.forId}-error` : undefined))
</script>

<template>
  <div class="ui-field ui-form-field">
    <label class="ui-form-field__label" :for="forId">{{ label }}</label>
    <slot :description-id="descriptionId" :error-id="errorId" />
    <p v-if="description" :id="`${forId}-description`" class="ui-form-field__description">
      {{ description }}
    </p>
    <p v-if="error" :id="`${forId}-error`" class="ui-form-field__message--error" role="alert">
      {{ error }}
    </p>
  </div>
</template>
