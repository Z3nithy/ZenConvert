<script setup>
import { onMounted, ref, useId, watch } from 'vue'
import { X } from '@lucide/vue'
import TerminalBar from './TerminalBar.vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  title: { type: String, required: true },
  status: { type: String, default: '' },
  // Impede fechar por Esc, clique no fundo ou botão (ex.: durante uma operação).
  persistent: { type: Boolean, default: false },
  dragging: { type: Boolean, default: false },
})
const emit = defineEmits(['update:modelValue'])

const dialogRef = ref(null)
const titleId = useId()

function sync(open) {
  const dialog = dialogRef.value
  if (!dialog) return
  if (open && !dialog.open) dialog.showModal()
  else if (!open && dialog.open) dialog.close()
}

watch(() => props.modelValue, sync, { flush: 'post' })
onMounted(() => sync(props.modelValue))

function requestClose() {
  if (!props.persistent) emit('update:modelValue', false)
}

function onCancel(event) {
  event.preventDefault()
  requestClose()
}

function onClick(event) {
  if (event.target === dialogRef.value) requestClose()
}
</script>

<template>
  <dialog
    ref="dialogRef"
    class="terminal-dialog"
    :class="{ 'terminal-dialog--dragging': dragging }"
    :aria-labelledby="titleId"
    @cancel="onCancel"
    @click="onClick"
  >
    <template v-if="modelValue">
      <TerminalBar :title="title" :status="status" title-tag="h2" :title-id="titleId">
        <button
          class="terminal-dialog__close"
          type="button"
          :disabled="persistent"
          aria-label="Fechar"
          @click="requestClose"
        >
          <X :size="16" aria-hidden="true" />
        </button>
      </TerminalBar>
      <div class="terminal-dialog__body">
        <slot />
      </div>
    </template>
  </dialog>
</template>

<style scoped>
.terminal-dialog {
  inset: 0;
  width: min(34rem, calc(100vw - var(--space-5)));
  max-height: calc(100dvh - var(--space-5));
  margin: auto;
  padding: 0;
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface-overlay);
  color: var(--color-text-primary);
  box-shadow: var(--shadow-raised);
  font-family: var(--font-mono);
  transition: border-color var(--duration-fast) var(--ease-standard);
}

.terminal-dialog[open] {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  animation: terminal-dialog-in var(--duration-normal) var(--ease-standard);
}

.terminal-dialog::backdrop {
  background: rgb(4 8 6 / 72%);
  backdrop-filter: blur(3px);
}

.terminal-dialog--dragging {
  border-color: var(--color-green-400);
  box-shadow:
    var(--shadow-raised),
    0 0 0 2px var(--color-green-500);
}

.terminal-dialog__body {
  display: grid;
  min-height: 0;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-5) var(--space-5);
  overflow-y: auto;
}

.terminal-dialog__close {
  display: grid;
  width: 2rem;
  height: 2rem;
  flex: 0 0 auto;
  place-items: center;
  border: 0;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  transition:
    background var(--duration-fast) var(--ease-standard),
    color var(--duration-fast) var(--ease-standard);
}

.terminal-dialog__close:hover:not(:disabled) {
  background: var(--color-danger-surface);
  color: var(--color-danger);
}

.terminal-dialog__close:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

@keyframes terminal-dialog-in {
  from {
    transform: translateY(var(--space-2));
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .terminal-dialog[open] {
    animation: none;
  }
}
</style>
