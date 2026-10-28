<script setup>
import { X } from '@lucide/vue'
import { ref, watch } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'info',
    validator: (value) => ['info', 'success', 'warning', 'error'].includes(value),
  },
  title: {
    type: String,
    default: '',
  },
  dismissible: {
    type: Boolean,
    default: false,
  },
  announce: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['dismiss'])
const visible = ref(true)

watch(
  () => props.variant,
  () => {
    visible.value = true
  },
)

function dismiss() {
  visible.value = false
  emit('dismiss')
}
</script>

<template>
  <Transition name="ui-feedback">
    <div
      v-if="visible"
      class="ui-alert"
      :class="`ui-alert--${variant}`"
      :role="announce ? (variant === 'error' ? 'alert' : 'status') : undefined"
      :aria-live="announce ? undefined : 'off'"
    >
      <div class="ui-alert__content">
        <strong v-if="title" class="ui-alert__title">{{ title }}</strong>
        <p class="ui-alert__message"><slot /></p>
      </div>
      <button
        v-if="dismissible"
        class="ui-alert__close"
        type="button"
        aria-label="Fechar aviso"
        @click="dismiss"
      >
        <X :size="18" :stroke-width="1.75" aria-hidden="true" />
      </button>
    </div>
  </Transition>
</template>
