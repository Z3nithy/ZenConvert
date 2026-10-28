<script setup>
import { LoaderCircle } from '@lucide/vue'

defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value),
  },
  label: {
    type: String,
    default: 'Carregando',
  },
  decorative: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <LoaderCircle
    class="ui-spinner"
    :class="{ 'ui-spinner--sm': size === 'sm', 'ui-spinner--lg': size === 'lg' }"
    :role="decorative ? undefined : 'status'"
    :aria-label="decorative ? undefined : label"
    :aria-hidden="decorative ? 'true' : undefined"
  />
</template>
