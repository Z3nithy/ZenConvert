<script setup>
import { computed, ref } from 'vue'
import { Check, CloudUpload, Upload } from '@lucide/vue'
import ConversionModal from '@/components/dashboard/ConversionModal.vue'
import DestinationPicker from '@/components/dashboard/DestinationPicker.vue'
import HistoryPanel from '@/components/dashboard/HistoryPanel.vue'
import TerminalBar from '@/components/dashboard/TerminalBar.vue'
import ThemeToggle from '@/components/dashboard/ThemeToggle.vue'
import { useConversionHistory } from '@/composables/useConversionHistory'
import { useConversions } from '@/composables/useConversions'
import { useFileDrop } from '@/composables/useFileDrop'
import { tools } from '@/config/conversionTools'
import { detectDestinations } from '@/utils/files'

const history = useConversionHistory()
const conversions = useConversions(tools, {
  onConverted: ({ entry, tool }) =>
    history.add({
      name: entry.file.name,
      output: entry.result.filename,
      tool: tool.name,
      size: entry.file.size,
    }),
})
const { state } = conversions

const activeToolId = ref(null)
const activeTool = computed(() => tools.find(({ id }) => id === activeToolId.value) ?? null)
const selection = ref(null)

const totalFiles = computed(() =>
  Object.values(state).reduce((total, { entries }) => total + entries.length, 0),
)

function addToTool(tool, files) {
  const { accepted } = conversions.addFiles(tool, files)
  if (accepted) activeToolId.value = tool.id
}

function routeFiles(files) {
  if (!files.length) return
  const { supported, unsupported, destinations } = detectDestinations(files, tools)
  if (destinations.length === 1 && !unsupported.length) {
    addToTool(destinations[0], supported)
    return
  }
  selection.value = {
    files: supported,
    unsupported: unsupported.map(({ name }) => name),
    destinations,
  }
}

function selectDestination(tool) {
  const files = selection.value?.files ?? []
  selection.value = null
  addToTool(tool, files)
}

function onCardInput(tool, event) {
  addToTool(tool, Array.from(event.target.files ?? []))
  event.target.value = ''
}

function onIntakeInput(event) {
  routeFiles(Array.from(event.target.files ?? []))
  event.target.value = ''
}

function removeFile(index) {
  conversions.removeFile(activeToolId.value, index)
  if (!state[activeToolId.value].entries.length) activeToolId.value = null
}

const { isDragging, dropTarget } = useFileDrop((files, targetId) => {
  if (activeTool.value) {
    addToTool(activeTool.value, files)
    return
  }
  const target = tools.find(({ id }) => id === targetId)
  if (target) addToTool(target, files)
  else routeFiles(files)
})

const dropHint = computed(() => {
  if (!isDragging.value || activeTool.value || selection.value) return ''
  const target = tools.find(({ id }) => id === dropTarget.value)
  return target ? `Solte para converter em ${target.name}` : 'Solte para escolher o destino'
})
</script>

<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <a class="dashboard-brand" href="/" aria-label="ZenConvert — início">
        <span class="dashboard-brand__mark" aria-hidden="true">
          <span>&gt;</span><span class="dashboard-brand__cursor">_</span>
        </span>
        <span class="dashboard-brand__name">Zen<span>Convert</span></span>
      </a>

      <div class="dashboard-header__right">
        <ThemeToggle />
        <span class="dashboard-header__status">
          <span class="dashboard-status-dot" aria-hidden="true"></span>
          SISTEMA ONLINE
        </span>
      </div>
    </header>

    <main class="dashboard-main">
      <section class="dashboard-hero" aria-labelledby="dashboard-title">
        <div class="dashboard-hero__copy">
          <p class="dashboard-eyebrow">
            <span class="dashboard-eyebrow__prompt" aria-hidden="true">&gt;</span>
            SEU ESPAÇO DE ARQUIVOS
          </p>
          <h1 id="dashboard-title">Seus arquivos.<br />Seu <span>fluxo.</span></h1>
          <p class="dashboard-hero__description">
            Escolha o formato de destino, envie ou arraste seus arquivos e baixe o resultado
            convertido.
          </p>
        </div>

        <div class="dashboard-terminal" aria-label="Status do painel ZenConvert">
          <TerminalBar title="zenconvert / workspace" status="READY" />
          <div class="dashboard-terminal__body">
            <p><span class="dashboard-terminal__muted">workspace.files</span></p>
            <p>
              <span class="dashboard-terminal__key">selected</span>
              <span class="dashboard-terminal__operator">=</span>
              <strong>{{ totalFiles }}</strong>
              <span class="dashboard-terminal__muted">file{{ totalFiles === 1 ? '' : 's' }}</span>
            </p>
            <p class="dashboard-terminal__ready">
              <Check :size="14" aria-hidden="true" />
              ready_to_start<span class="dashboard-terminal__caret" aria-hidden="true"></span>
            </p>
          </div>
        </div>
      </section>

      <section class="dashboard-tools" aria-labelledby="tools-title">
        <div class="dashboard-section-heading">
          <div>
            <p class="dashboard-section-heading__eyebrow">01 / FERRAMENTAS</p>
            <h2 id="tools-title">Com o que vamos trabalhar?</h2>
          </div>
          <p>Selecione o formato de destino da conversão.</p>
        </div>

        <label class="dashboard-intake" :class="{ 'dashboard-intake--active': isDragging }">
          <input
            class="dashboard-visually-hidden"
            type="file"
            multiple
            aria-label="Enviar arquivos e escolher o destino depois"
            @change="onIntakeInput"
          />
          <span class="dashboard-intake__icon" aria-hidden="true">
            <CloudUpload :size="22" :stroke-width="1.7" />
          </span>
          <span class="dashboard-intake__copy">
            <span class="dashboard-intake__title">Não sabe o destino? Envie primeiro.</span>
            <span class="dashboard-intake__text">
              Detectamos o formato dos arquivos e sugerimos as conversões possíveis. Você também
              pode arrastar arquivos para qualquer lugar da tela.
            </span>
          </span>
          <span class="dashboard-intake__action">Escolher arquivos</span>
        </label>

        <div class="dashboard-grid">
          <article v-for="tool in tools" :key="tool.id" class="dashboard-tool">
            <label
              class="dashboard-tool__picker"
              :class="[
                `dashboard-tool__picker--${tool.tone}`,
                {
                  'dashboard-tool__picker--selected': state[tool.id].entries.length > 0,
                  'dashboard-tool__picker--drop': dropTarget === tool.id,
                },
              ]"
              :for="`file-${tool.id}`"
              :data-drop-target="tool.id"
            >
              <input
                :id="`file-${tool.id}`"
                class="dashboard-visually-hidden"
                type="file"
                :accept="tool.accept"
                multiple
                :disabled="state[tool.id].running"
                :aria-label="`Selecionar arquivos para converter em ${tool.name}`"
                :aria-describedby="
                  state[tool.id].message ? `file-${tool.id}-error` : `file-${tool.id}-formats`
                "
                @change="onCardInput(tool, $event)"
              />
              <span class="dashboard-tool__icon" aria-hidden="true">
                <component :is="tool.icon" :size="23" :stroke-width="1.7" />
              </span>
              <span class="dashboard-tool__arrow" aria-hidden="true">
                <Upload :size="16" :stroke-width="1.75" />
              </span>
              <span class="dashboard-tool__name">{{ tool.name }}</span>
              <span class="dashboard-tool__description">{{ tool.description }}</span>
              <span :id="`file-${tool.id}-formats`" class="dashboard-tool__formats">
                {{ tool.formats }}
              </span>
              <span class="dashboard-tool__action">
                {{ state[tool.id].entries.length ? 'Adicionar arquivos' : 'Selecionar arquivos' }}
              </span>
            </label>

            <Transition name="dashboard-feedback">
              <p
                v-if="state[tool.id].message && activeToolId !== tool.id"
                :id="`file-${tool.id}-error`"
                class="dashboard-tool__error"
                role="alert"
              >
                {{ state[tool.id].message }}
              </p>
            </Transition>

            <button
              v-if="state[tool.id].entries.length"
              class="dashboard-tool__review"
              type="button"
              @click="activeToolId = tool.id"
            >
              Ver {{ state[tool.id].entries.length }} arquivo{{
                state[tool.id].entries.length === 1 ? '' : 's'
              }}
              <span
                v-if="conversions.pendingCount(tool.id) === 0"
                class="dashboard-tool__review-done"
              >
                · convertido{{ state[tool.id].entries.length === 1 ? '' : 's' }}
              </span>
            </button>
          </article>
        </div>

        <p class="dashboard-selection-status" role="status" aria-live="polite">
          {{
            totalFiles
              ? `${totalFiles} arquivo${totalFiles === 1 ? '' : 's'} neste painel.`
              : 'Escolha um card, adicione arquivos e converta para o formato desejado.'
          }}
        </p>
      </section>

      <HistoryPanel
        :items="history.items.value"
        :persistent="history.persistent.value"
        @clear="history.clear"
      />

      <footer class="dashboard-footer">
        <span><span class="dashboard-footer__prompt">&gt;_</span> ZENCONVERT</span>
        <span>SEU ESPAÇO DE ARQUIVOS</span>
      </footer>
    </main>

    <ConversionModal
      :tool="activeTool"
      :state="activeTool ? state[activeTool.id] : null"
      :dragging="isDragging"
      @close="activeToolId = null"
      @add-files="addToTool(activeTool, $event)"
      @remove="removeFile"
      @set-option="state[activeTool.id].options[activeTool.option.param] = $event"
      @convert="conversions.convertAll(activeTool)"
      @cancel="conversions.cancel(activeTool)"
      @download-all="conversions.downloadAll(activeTool)"
    />

    <DestinationPicker
      :selection="selection"
      @close="selection = null"
      @select="selectDestination"
    />

    <Transition name="dashboard-feedback">
      <div v-if="dropHint" class="dashboard-drop-hint" role="status">
        <CloudUpload :size="18" aria-hidden="true" /> {{ dropHint }}
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.dashboard {
  --dashboard-content-width: 76rem;

  min-height: 100vh;
  background:
    radial-gradient(
      ellipse at 82% 4%,
      color-mix(in srgb, var(--color-accent) 9%, transparent),
      transparent 29rem
    ),
    var(--color-surface-canvas);
}

.dashboard-visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  clip-path: inset(50%);
  white-space: nowrap;
}

.dashboard-header {
  position: sticky;
  z-index: var(--layer-sticky);
  top: 0;
  display: flex;
  min-height: 4.25rem;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  padding-inline: max(var(--space-5), calc((100vw - var(--dashboard-content-width)) / 2));
  border-bottom: 1px solid color-mix(in srgb, var(--color-border) 72%, transparent);
  background: color-mix(in srgb, var(--color-surface-canvas) 90%, transparent);
  backdrop-filter: blur(16px);
}

.dashboard-brand,
.dashboard-header__right,
.dashboard-header__status {
  display: inline-flex;
  align-items: center;
}

.dashboard-brand {
  gap: var(--space-3);
  color: var(--color-text-primary);
  text-decoration: none;
}

.dashboard-brand__mark {
  display: grid;
  width: 2rem;
  height: 2rem;
  place-content: center;
  border: 1px solid var(--color-green-700);
  border-radius: var(--radius-sm);
  background: var(--color-green-900);
  color: var(--color-green-300);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: var(--font-weight-semibold);
}

.dashboard-brand__cursor {
  animation: dashboard-cursor 1.2s steps(2, start) infinite;
}

@keyframes dashboard-cursor {
  to {
    visibility: hidden;
  }
}

.dashboard-brand__name {
  font-size: var(--text-md);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--tracking-tight);
}

.dashboard-brand__name span {
  color: var(--color-green-300);
}

.dashboard-header__right {
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: var(--space-5);
}

.dashboard-header__status {
  gap: var(--space-2);
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  font-size: 0.625rem;
  letter-spacing: 0.06em;
}

.dashboard-status-dot {
  width: 0.4375rem;
  height: 0.4375rem;
  flex: 0 0 auto;
  border-radius: 50%;
  background: var(--color-green-400);
  box-shadow: 0 0 10px rgb(105 216 135 / 38%);
}

.dashboard-main {
  width: min(100%, calc(var(--dashboard-content-width) + 2 * var(--space-8)));
  margin-inline: auto;
  padding: 0 var(--space-8);
}

.dashboard-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(17rem, 0.8fr);
  align-items: center;
  gap: clamp(var(--space-8), 7vw, var(--space-12));
  padding-block: clamp(var(--space-10), 8vw, 6rem);
  border-bottom: 1px solid var(--color-border);
}

.dashboard-eyebrow,
.dashboard-section-heading__eyebrow {
  margin: 0;
  color: var(--color-green-300);
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  letter-spacing: 0.1em;
}

.dashboard-eyebrow__prompt {
  margin-right: var(--space-2);
  color: var(--color-green-400);
}

.dashboard-hero h1 {
  margin: var(--space-5) 0 var(--space-4);
  font-size: clamp(2.75rem, 6vw, 4.5rem);
  font-weight: var(--font-weight-semibold);
  letter-spacing: -0.065em;
  line-height: 0.99;
}

.dashboard-hero h1 span {
  color: var(--color-green-300);
}

.dashboard-hero__description {
  max-width: 34rem;
  margin: 0;
  color: var(--color-text-secondary);
  font-size: var(--text-md);
  line-height: var(--line-height-relaxed);
}

.dashboard-terminal {
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface-raised);
  box-shadow: var(--shadow-raised);
}

.dashboard-terminal__body {
  display: grid;
  gap: var(--space-3);
  padding: var(--space-5);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
}

.dashboard-terminal__body p {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin: 0;
}

.dashboard-terminal__muted {
  color: var(--color-text-muted);
}

.dashboard-terminal__key {
  color: var(--color-blue-300);
}

.dashboard-terminal__operator {
  color: var(--color-gray-400);
}

.dashboard-terminal__body strong,
.dashboard-terminal__ready {
  color: var(--color-green-300);
}

.dashboard-terminal__ready {
  align-items: center;
  gap: var(--space-2) !important;
  margin-top: var(--space-2) !important;
}

.dashboard-terminal__caret {
  width: 0.4rem;
  height: 0.8rem;
  background: var(--color-green-400);
  animation: dashboard-cursor 1.2s steps(2, start) infinite;
}

.dashboard-tools {
  padding-block: var(--space-10);
}

.dashboard-section-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: var(--space-5);
  margin-bottom: var(--space-5);
}

.dashboard-section-heading h2 {
  margin: var(--space-2) 0 0;
  font-size: var(--text-2xl);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--tracking-tight);
}

.dashboard-section-heading > p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: var(--text-sm);
}

.dashboard-intake {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
  padding: var(--space-4) var(--space-5);
  border: 1px dashed var(--color-gray-500);
  border-radius: var(--radius-lg);
  background: var(--color-surface-raised);
  cursor: pointer;
  transition:
    border-color var(--duration-fast) var(--ease-standard),
    background var(--duration-fast) var(--ease-standard),
    box-shadow var(--duration-fast) var(--ease-standard);
}

.dashboard-intake:hover,
.dashboard-intake--active {
  border-color: var(--color-green-500);
  background: var(--color-surface-interactive);
}

.dashboard-intake:focus-within {
  border-color: var(--color-border-focus);
  box-shadow: var(--focus-ring);
}

.dashboard-intake__icon {
  display: grid;
  width: 2.75rem;
  height: 2.75rem;
  flex: 0 0 auto;
  place-items: center;
  border: 1px solid var(--color-green-700);
  border-radius: var(--radius-md);
  background: var(--color-green-900);
  color: var(--color-green-300);
}

.dashboard-intake__copy {
  display: grid;
  min-width: 0;
  flex: 1;
  gap: var(--space-1);
}

.dashboard-intake__title {
  font-weight: var(--font-weight-semibold);
}

.dashboard-intake__text {
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
}

.dashboard-intake__action {
  flex: 0 0 auto;
  padding: var(--space-2) var(--space-4);
  border: 1px solid var(--color-green-700);
  border-radius: var(--radius-md);
  color: var(--color-green-200);
  font-size: var(--text-xs);
  font-weight: var(--font-weight-medium);
  white-space: nowrap;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-4);
}

.dashboard-tool {
  min-width: 0;
}

.dashboard-tool__picker {
  position: relative;
  display: grid;
  min-height: 13.25rem;
  grid-template-columns: 1fr auto;
  align-content: start;
  align-items: center;
  gap: var(--space-2) var(--space-3);
  padding: var(--space-5);
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface-raised);
  cursor: pointer;
  transition:
    transform var(--duration-fast) var(--ease-standard),
    border-color var(--duration-fast) var(--ease-standard),
    background var(--duration-fast) var(--ease-standard),
    box-shadow var(--duration-fast) var(--ease-standard);
}

.dashboard-tool__picker:hover {
  transform: translateY(-2px);
  border-color: var(--color-gray-500);
  background: var(--color-surface-interactive);
}

.dashboard-tool__picker:focus-within {
  border-color: var(--color-border-focus);
  box-shadow: var(--focus-ring);
}

.dashboard-tool__picker--selected {
  border-color: var(--color-green-600);
}

.dashboard-tool__picker--drop {
  transform: translateY(-2px);
  border-color: var(--color-green-400);
  background: var(--color-surface-interactive);
  box-shadow: 0 0 0 2px var(--color-green-500);
}

.dashboard-tool__icon {
  display: grid;
  width: 3rem;
  height: 3rem;
  grid-column: 1;
  place-items: center;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-overlay);
  color: var(--color-text-primary);
  transition:
    transform var(--duration-fast) var(--ease-standard),
    border-color var(--duration-fast) var(--ease-standard),
    color var(--duration-fast) var(--ease-standard);
}

.dashboard-tool__picker:hover .dashboard-tool__icon {
  transform: scale(1.04);
}

.dashboard-tool__picker--blue .dashboard-tool__icon {
  border-color: rgb(139 196 255 / 28%);
  color: var(--color-blue-300);
}

.dashboard-tool__picker--green .dashboard-tool__icon {
  border-color: rgb(105 216 135 / 28%);
  color: var(--color-green-300);
}

.dashboard-tool__picker--red .dashboard-tool__icon {
  border-color: rgb(255 133 133 / 28%);
  color: var(--color-danger);
}

.dashboard-tool__picker--amber .dashboard-tool__icon {
  border-color: rgb(255 210 123 / 28%);
  color: var(--color-warning);
}

.dashboard-tool__picker--violet .dashboard-tool__icon {
  border-color: rgb(196 167 255 / 28%);
  color: #c4a7ff;
}

.dashboard-tool__picker--cyan .dashboard-tool__icon {
  border-color: rgb(139 219 255 / 28%);
  color: #8bdbff;
}

.dashboard-tool__picker--orange .dashboard-tool__icon {
  border-color: rgb(255 176 120 / 28%);
  color: #ffb078;
}

.dashboard-tool__picker--pink .dashboard-tool__icon {
  border-color: rgb(255 163 214 / 28%);
  color: #ffa3d6;
}

.dashboard-tool__picker--lime .dashboard-tool__icon {
  border-color: rgb(204 237 112 / 28%);
  color: #cced70;
}

.dashboard-tool__arrow {
  display: grid;
  width: 2.25rem;
  height: 2.25rem;
  grid-column: 2;
  grid-row: 1;
  place-items: center;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-muted);
  transition:
    color var(--duration-fast) var(--ease-standard),
    background var(--duration-fast) var(--ease-standard),
    border-color var(--duration-fast) var(--ease-standard);
}

.dashboard-tool__picker:hover .dashboard-tool__arrow {
  border-color: var(--color-green-700);
  background: var(--color-green-900);
  color: var(--color-green-300);
}

.dashboard-tool__name,
.dashboard-tool__description,
.dashboard-tool__formats,
.dashboard-tool__action {
  grid-column: 1 / -1;
}

.dashboard-tool__name {
  margin-top: var(--space-2);
  font-size: var(--text-lg);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-tight);
}

.dashboard-tool__description {
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
}

.dashboard-tool__formats {
  margin-top: var(--space-1);
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  font-size: 0.625rem;
  letter-spacing: 0.06em;
}

.dashboard-tool__action {
  display: flex;
  min-height: 2.5rem;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  margin-top: var(--space-2);
  padding-inline: var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: var(--text-xs);
  font-weight: var(--font-weight-medium);
  transition:
    border-color var(--duration-fast) var(--ease-standard),
    background var(--duration-fast) var(--ease-standard),
    color var(--duration-fast) var(--ease-standard);
}

.dashboard-tool__picker:hover .dashboard-tool__action,
.dashboard-tool__picker--selected .dashboard-tool__action,
.dashboard-tool__picker--drop .dashboard-tool__action {
  border-color: var(--color-green-700);
  background: var(--color-green-900);
  color: var(--color-green-200);
}

.dashboard-tool__review {
  display: inline-flex;
  min-height: 2.5rem;
  align-items: center;
  margin-top: var(--space-2);
  padding: 0 var(--space-2);
  border: 0;
  background: transparent;
  color: var(--color-green-300);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  cursor: pointer;
}

.dashboard-tool__review:hover {
  color: var(--color-green-200);
  text-decoration: underline;
}

.dashboard-tool__review-done {
  margin-left: var(--space-1);
  color: var(--color-text-muted);
}

.dashboard-tool__error {
  margin: var(--space-2) 0 0;
  color: var(--color-danger);
  font-size: var(--text-xs);
}

.dashboard-feedback-enter-active,
.dashboard-feedback-leave-active {
  transition:
    opacity var(--duration-normal) var(--ease-standard),
    transform var(--duration-normal) var(--ease-standard);
}

.dashboard-feedback-enter-from,
.dashboard-feedback-leave-to {
  transform: translateY(var(--space-1));
  opacity: 0;
}

.dashboard-drop-hint {
  position: fixed;
  z-index: var(--layer-toast, 60);
  bottom: var(--space-6);
  left: 50%;
  display: inline-flex;
  max-width: calc(100vw - var(--space-6));
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-5);
  transform: translateX(-50%);
  border: 1px solid var(--color-green-500);
  border-radius: var(--radius-lg);
  background: var(--color-green-900);
  color: var(--color-green-200);
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  box-shadow: var(--shadow-raised);
  pointer-events: none;
}

.dashboard-drop-hint.dashboard-feedback-enter-from,
.dashboard-drop-hint.dashboard-feedback-leave-to {
  transform: translate(-50%, var(--space-1));
}

.dashboard-selection-status {
  min-height: 1.5rem;
  margin: var(--space-5) 0 0;
  color: var(--color-text-muted);
  font-size: var(--text-xs);
  text-align: center;
}

.dashboard-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  padding: var(--space-5) 0 var(--space-8);
  border-top: 1px solid var(--color-border);
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  font-size: 0.625rem;
  letter-spacing: 0.08em;
}

.dashboard-footer__prompt {
  margin-right: var(--space-2);
  color: var(--color-green-300);
}

@media (max-width: 64rem) {
  .dashboard-hero {
    grid-template-columns: minmax(0, 1fr) minmax(15rem, 0.8fr);
  }

  .dashboard-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 48rem) {
  .dashboard-header {
    min-height: 3.75rem;
    padding-inline: var(--space-5);
  }

  .dashboard-main {
    padding-inline: var(--space-5);
  }

  .dashboard-hero {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--space-6);
    padding-block: var(--space-10);
  }

  .dashboard-terminal {
    max-width: 34rem;
  }

  .dashboard-intake {
    flex-wrap: wrap;
  }

  .dashboard-intake__copy {
    flex-basis: calc(100% - 4.5rem);
  }
}

@media (max-width: 36rem) {
  .dashboard-header__right {
    gap: var(--space-2);
  }

  .dashboard-header__status {
    font-size: 0;
  }

  .dashboard-header__status .dashboard-status-dot {
    width: 0.5rem;
    height: 0.5rem;
  }

  .dashboard-main {
    padding-inline: var(--space-4);
  }

  .dashboard-section-heading {
    align-items: flex-start;
    flex-direction: column;
    gap: var(--space-2);
  }

  .dashboard-section-heading h2 {
    font-size: var(--text-xl);
  }

  .dashboard-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .dashboard-tool__picker {
    min-height: 12.5rem;
  }

  .dashboard-intake__action {
    width: 100%;
    text-align: center;
  }

  .dashboard-footer {
    align-items: flex-start;
    flex-direction: column;
    gap: var(--space-2);
  }
}

@media (prefers-reduced-motion: reduce) {
  .dashboard-brand__cursor,
  .dashboard-terminal__caret {
    animation: none;
  }
}
</style>
