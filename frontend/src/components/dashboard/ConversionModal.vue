<script setup>
import { computed, ref } from 'vue'
import { Archive, Ban, Download, Plus, X } from '@lucide/vue'
import UiButton from '@/components/ui/UiButton.vue'
import UiSelect from '@/components/ui/UiSelect.vue'
import { formatSize } from '@/utils/files'
import TerminalDialog from './TerminalDialog.vue'

const props = defineProps({
  tool: { type: Object, default: null },
  state: { type: Object, default: null },
  dragging: { type: Boolean, default: false },
})
const emit = defineEmits([
  'close',
  'add-files',
  'remove',
  'convert',
  'cancel',
  'download-all',
  'set-option',
])

const inputRef = ref(null)

const open = computed(() => Boolean(props.tool && props.state))
const doneCount = computed(
  () => props.state?.entries.filter(({ status }) => status === 'done').length ?? 0,
)
const pendingCount = computed(() => (props.state?.entries.length ?? 0) - doneCount.value)
const status = computed(() => {
  if (props.state?.running) return 'RUNNING'
  return pendingCount.value === 0 ? 'DONE' : 'READY'
})
const convertLabel = computed(() => {
  if (props.state?.running) return 'Convertendo…'
  if (pendingCount.value === 0) return 'Conversão concluída'
  return `Converter para ${props.tool.name}`
})

function onInput(event) {
  emit('add-files', Array.from(event.target.files ?? []))
  event.target.value = ''
}

function progressLabel(entry) {
  return entry.progress < 1
    ? `enviando ${Math.round(entry.progress * 100)}%`
    : 'processando no servidor…'
}
</script>

<template>
  <TerminalDialog
    :model-value="open"
    :title="tool ? `zenconvert / converter.${tool.target}` : ''"
    :status="status"
    :persistent="Boolean(state?.running)"
    :dragging="dragging"
    @update:model-value="emit('close')"
  >
    <template v-if="open">
      <p class="conversion-modal__meta">
        <span class="conversion-modal__key">aceita</span>
        <span class="conversion-modal__operator">=</span>
        <span>{{ tool.formats }}</span>
      </p>

      <ul class="conversion-modal__files" :aria-label="`Arquivos para converter em ${tool.name}`">
        <li v-for="(entry, index) in state.entries" :key="entry.key">
          <span class="conversion-modal__file-icon" aria-hidden="true">
            <component :is="tool.icon" :size="15" />
          </span>
          <span class="conversion-modal__file-copy">
            <span class="conversion-modal__file-name">{{ entry.file.name }}</span>
            <span class="conversion-modal__file-size">
              {{ formatSize(entry.file.size) }}
              <template v-if="entry.status === 'converting'">
                · {{ progressLabel(entry) }}</template
              >
              <template v-else-if="entry.status === 'done'"> · convertido</template>
            </span>
            <progress
              v-if="entry.status === 'converting'"
              class="conversion-modal__progress"
              max="1"
              :value="entry.progress < 1 ? entry.progress : undefined"
              :aria-label="`Progresso de ${entry.file.name}`"
            ></progress>
            <span v-if="entry.error" class="conversion-modal__file-error" role="alert">
              {{ entry.error }}
            </span>
          </span>
          <a
            v-if="entry.result"
            class="conversion-modal__icon-action conversion-modal__download"
            :href="entry.result.url"
            :download="entry.result.filename"
            :aria-label="`Baixar ${entry.result.filename}`"
          >
            <Download :size="16" aria-hidden="true" />
          </a>
          <button
            class="conversion-modal__icon-action conversion-modal__remove"
            type="button"
            :disabled="entry.status === 'converting'"
            :aria-label="`Remover ${entry.file.name}`"
            @click="emit('remove', index)"
          >
            <X :size="16" aria-hidden="true" />
          </button>
        </li>
      </ul>

      <p v-if="state.message" class="conversion-modal__message" role="alert">
        {{ state.message }}
      </p>

      <div class="conversion-modal__footer">
        <UiSelect
          v-if="tool.option"
          :model-value="state.options[tool.option.param]"
          @update:model-value="emit('set-option', $event)"
          :label="tool.option.label"
          :disabled="state.running"
        >
          <option v-for="choice in tool.option.choices" :key="choice.value" :value="choice.value">
            {{ choice.label }}
          </option>
        </UiSelect>

        <div class="conversion-modal__buttons">
          <input
            ref="inputRef"
            class="conversion-modal__input"
            type="file"
            multiple
            tabindex="-1"
            :accept="tool.accept"
            aria-hidden="true"
            @change="onInput"
          />
          <UiButton variant="secondary" :disabled="state.running" @click="inputRef.click()">
            <Plus :size="16" aria-hidden="true" /> Adicionar
          </UiButton>
          <UiButton
            v-if="doneCount >= 2"
            variant="secondary"
            :loading="state.zipping"
            :disabled="state.running"
            @click="emit('download-all')"
          >
            <Archive :size="16" aria-hidden="true" /> Baixar tudo (ZIP)
          </UiButton>
          <UiButton v-if="state.running" variant="secondary" @click="emit('cancel')">
            <Ban :size="16" aria-hidden="true" /> Cancelar
          </UiButton>
          <UiButton
            :loading="state.running"
            :disabled="pendingCount === 0"
            @click="emit('convert')"
          >
            {{ convertLabel }}
          </UiButton>
        </div>
      </div>
    </template>
  </TerminalDialog>
</template>

<style scoped>
.conversion-modal__meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin: 0;
  color: var(--color-green-300);
  font-size: var(--text-xs);
}

.conversion-modal__key {
  color: var(--color-blue-300);
}

.conversion-modal__operator {
  color: var(--color-gray-400);
}

.conversion-modal__files {
  display: grid;
  gap: var(--space-2);
  margin: 0;
  padding: 0;
  overflow-y: auto;
  list-style: none;
}

.conversion-modal__files li {
  display: flex;
  min-width: 0;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-raised);
}

.conversion-modal__file-icon {
  display: grid;
  width: 2rem;
  height: 2rem;
  flex: 0 0 auto;
  place-items: center;
  color: var(--color-green-300);
}

.conversion-modal__file-copy {
  display: grid;
  min-width: 0;
  flex: 1;
  gap: 0.25rem;
}

.conversion-modal__file-name {
  overflow: hidden;
  color: var(--color-text-secondary);
  font-size: var(--text-xs);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conversion-modal__file-size {
  color: var(--color-text-muted);
  font-size: 0.625rem;
}

.conversion-modal__file-error {
  color: var(--color-danger);
  font-size: var(--text-xs);
  overflow-wrap: anywhere;
}

.conversion-modal__progress {
  width: 100%;
  height: 0.25rem;
  overflow: hidden;
  border: 0;
  border-radius: var(--radius-sm);
  background: var(--color-gray-700);
  accent-color: var(--color-green-400);
}

.conversion-modal__progress::-webkit-progress-bar {
  background: var(--color-gray-700);
}

.conversion-modal__progress::-webkit-progress-value {
  background: var(--color-green-400);
  transition: width var(--duration-fast) var(--ease-standard);
}

.conversion-modal__progress::-moz-progress-bar {
  background: var(--color-green-400);
}

.conversion-modal__icon-action {
  display: grid;
  width: 2.5rem;
  height: 2.5rem;
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

.conversion-modal__remove:hover:not(:disabled) {
  background: var(--color-danger-surface);
  color: var(--color-danger);
}

.conversion-modal__remove:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

.conversion-modal__download {
  color: var(--color-green-300);
}

.conversion-modal__download:hover {
  background: var(--color-green-900);
  color: var(--color-green-200);
}

.conversion-modal__message {
  margin: 0;
  color: var(--color-warning);
  font-size: var(--text-xs);
}

.conversion-modal__footer {
  display: grid;
  gap: var(--space-3);
}

.conversion-modal__buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: var(--space-2);
}

.conversion-modal__input {
  display: none;
}
</style>
