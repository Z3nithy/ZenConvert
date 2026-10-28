<script setup>
import { computed } from 'vue'
import { ChevronRight } from '@lucide/vue'
import UiButton from '@/components/ui/UiButton.vue'
import TerminalDialog from './TerminalDialog.vue'

const props = defineProps({
  // { files, unsupported (nomes), destinations (ferramentas) } ou null quando fechado.
  selection: { type: Object, default: null },
})
const emit = defineEmits(['close', 'select'])

const open = computed(() => props.selection !== null)
const summary = computed(() => {
  const count = props.selection?.files.length ?? 0
  return `${count} arquivo${count === 1 ? '' : 's'} reconhecido${count === 1 ? '' : 's'}`
})
</script>

<template>
  <TerminalDialog
    :model-value="open"
    title="zenconvert / destino"
    status="SELECT"
    @update:model-value="emit('close')"
  >
    <template v-if="selection">
      <p class="destination-picker__meta">
        <span class="destination-picker__key">entrada</span>
        <span class="destination-picker__operator">=</span>
        <span>{{ summary }}</span>
      </p>

      <ul v-if="selection.files.length" class="destination-picker__names">
        <li v-for="file in selection.files" :key="file.name + file.size">{{ file.name }}</li>
      </ul>

      <p v-if="selection.unsupported.length" class="destination-picker__warning" role="alert">
        Ignorado{{ selection.unsupported.length === 1 ? '' : 's' }} (formato não suportado):
        {{ selection.unsupported.join(', ') }}.
      </p>

      <template v-if="selection.destinations.length">
        <p class="destination-picker__hint">Converter para:</p>
        <ul class="destination-picker__options">
          <li v-for="tool in selection.destinations" :key="tool.id">
            <button
              class="destination-picker__option"
              :class="`destination-picker__option--${tool.tone}`"
              type="button"
              @click="emit('select', tool)"
            >
              <span class="destination-picker__icon" aria-hidden="true">
                <component :is="tool.icon" :size="18" :stroke-width="1.7" />
              </span>
              <span class="destination-picker__copy">
                <span class="destination-picker__name">{{ tool.name }}</span>
                <span class="destination-picker__description">{{ tool.description }}</span>
              </span>
              <ChevronRight :size="16" aria-hidden="true" />
            </button>
          </li>
        </ul>
      </template>
      <p v-else class="destination-picker__warning" role="alert">
        {{
          selection.files.length
            ? 'Nenhum destino aceita todos esses arquivos juntos. Envie-os em grupos do mesmo tipo.'
            : 'Nenhum dos arquivos tem um formato suportado.'
        }}
      </p>

      <div class="destination-picker__footer">
        <UiButton variant="secondary" @click="emit('close')">Cancelar</UiButton>
      </div>
    </template>
  </TerminalDialog>
</template>

<style scoped>
.destination-picker__meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin: 0;
  color: var(--color-green-300);
  font-size: var(--text-xs);
}

.destination-picker__key {
  color: var(--color-blue-300);
}

.destination-picker__operator {
  color: var(--color-gray-400);
}

.destination-picker__names {
  max-height: 5.5rem;
  margin: 0;
  padding: 0;
  overflow-y: auto;
  color: var(--color-text-muted);
  font-size: 0.625rem;
  list-style: none;
}

.destination-picker__names li {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.destination-picker__hint {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: var(--text-xs);
}

.destination-picker__warning {
  margin: 0;
  color: var(--color-warning);
  font-size: var(--text-xs);
  overflow-wrap: anywhere;
}

.destination-picker__options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr));
  gap: var(--space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.destination-picker__option {
  display: flex;
  width: 100%;
  min-height: 3.5rem;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-raised);
  color: var(--color-text-muted);
  font: inherit;
  text-align: left;
  cursor: pointer;
  transition:
    border-color var(--duration-fast) var(--ease-standard),
    background var(--duration-fast) var(--ease-standard);
}

.destination-picker__option:hover {
  border-color: var(--color-green-600);
  background: var(--color-green-900);
}

.destination-picker__icon {
  display: grid;
  width: 2.25rem;
  height: 2.25rem;
  flex: 0 0 auto;
  place-items: center;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-overlay);
  color: var(--color-green-300);
}

.destination-picker__copy {
  display: grid;
  min-width: 0;
  flex: 1;
}

.destination-picker__name {
  color: var(--color-text-primary);
  font-size: var(--text-sm);
  font-weight: var(--font-weight-semibold);
}

.destination-picker__description {
  overflow: hidden;
  color: var(--color-text-muted);
  font-size: 0.625rem;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.destination-picker__footer {
  display: flex;
  justify-content: flex-end;
}
</style>
