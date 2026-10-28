<script setup>
defineOptions({ inheritAttrs: false })

defineProps({
  label: {
    type: String,
    required: true,
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md'].includes(value),
  },
  type: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'submit', 'reset'].includes(value),
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <button
    v-bind="$attrs"
    class="ui-icon-button"
    :class="{ 'ui-icon-button--sm': size === 'sm' }"
    :type="type"
    :aria-label="label"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>
