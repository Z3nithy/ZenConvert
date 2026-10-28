<script setup>
import {
  ArrowDown,
  ArrowRight,
  ArrowUpRight,
  Check,
  FileImage,
  MoreHorizontal,
  Plus,
  Terminal,
} from '@lucide/vue'
import { onBeforeUnmount, ref } from 'vue'
import {
  UiAlert,
  UiBadge,
  UiBreadcrumbs,
  UiButton,
  UiCard,
  UiCheckbox,
  UiEmptyState,
  UiErrorState,
  UiFormField,
  UiIconButton,
  UiInput,
  UiPagination,
  UiRadioGroup,
  UiSelect,
  UiSkeleton,
  UiSpinner,
  UiSwitch,
  UiTextarea,
} from '@/components/ui'
import ThemeToggle from '@/components/dashboard/ThemeToggle.vue'

const navigation = [
  { label: 'Visão geral', href: '#overview', index: '00' },
  { label: 'Cores', href: '#colors', index: '01' },
  { label: 'Tipografia', href: '#typography', index: '02' },
  { label: 'Ações', href: '#actions', index: '03' },
  { label: 'Formulários', href: '#forms', index: '04' },
  { label: 'Superfícies', href: '#surfaces', index: '05' },
  { label: 'Feedback', href: '#feedback', index: '06' },
  { label: 'Estados e navegação', href: '#states', index: '07' },
  { label: 'Motion', href: '#motion', index: '08' },
]

const colorGroups = [
  {
    name: 'Verde — acento',
    colors: [
      { token: 'green-950', value: '#0C1710' },
      { token: 'green-800', value: '#183825' },
      { token: 'green-600', value: '#2F7546' },
      { token: 'green-400', value: '#69D887' },
      { token: 'green-200', value: '#C7F7D1' },
    ],
  },
  {
    name: 'Neutros — estrutura',
    colors: [
      { token: 'black', value: '#080D0A' },
      { token: 'gray-900', value: '#18221B' },
      { token: 'gray-700', value: '#35433A' },
      { token: 'gray-400', value: '#91A197' },
      { token: 'white', value: '#F0F7F1' },
    ],
  },
  {
    name: 'Estados — semântica',
    colors: [
      { token: 'success', value: '#9AF0AD' },
      { token: 'warning', value: '#FFD27B' },
      { token: 'danger', value: '#FF8585' },
      { token: 'info', value: '#8BC4FF' },
    ],
  },
]

const radioOptions = [
  { value: 'balanced', label: 'Equilibrado', description: 'Boa leitura com tamanho compacto.' },
  { value: 'precise', label: 'Precisão máxima', description: 'Prioriza a saída mais detalhada.' },
]

const filename = ref('')
const filenameError = ref('')
const formFeedback = ref('')
const stateFeedback = ref('')
const outputFormat = ref('webp')
const quality = ref('balanced')
const keepMetadata = ref(true)
const automaticMode = ref(false)
const page = ref(3)
const copyFeedback = ref('')
let copyFeedbackTimer

function validateFilename() {
  filenameError.value = ''
  formFeedback.value = ''

  if (!filename.value.trim()) {
    filenameError.value = 'Informe um nome para continuar.'
    return
  }

  formFeedback.value = `O nome “${filename.value.trim()}” está pronto para uso no exemplo.`
}

function showStateFeedback(message) {
  stateFeedback.value = message
}

async function copyToken(value) {
  try {
    await navigator.clipboard.writeText(value)
    copyFeedback.value = `Cor ${value} copiada.`
  } catch {
    copyFeedback.value = 'Não foi possível copiar. Selecione o valor e copie manualmente.'
  }

  window.clearTimeout(copyFeedbackTimer)
  copyFeedbackTimer = window.setTimeout(() => {
    copyFeedback.value = ''
  }, 2800)
}

onBeforeUnmount(() => {
  window.clearTimeout(copyFeedbackTimer)
})
</script>

<template>
  <div class="ds-shell">
    <a class="ds-skip-link" href="#main-content">Pular para o conteúdo</a>

    <aside class="ds-sidebar" aria-label="Navegação do design system">
      <a class="ds-wordmark" href="#overview" aria-label="ZenConvert — início do design system">
        <span class="ds-wordmark__symbol" aria-hidden="true">
          <Terminal :size="18" :stroke-width="1.75" />
        </span>
        <span>Zen<span class="ds-wordmark__accent">Convert</span></span>
      </a>

      <div class="ds-sidebar__caption">SISTEMA DE INTERFACE</div>
      <nav class="ds-navigation" aria-label="Seções">
        <a
          v-for="item in navigation"
          :key="item.href"
          class="ds-navigation__link"
          :href="item.href"
        >
          <span class="ds-navigation__index">{{ item.index }}</span>
          <span>{{ item.label }}</span>
        </a>
      </nav>

      <div class="ds-sidebar__footer">
        <span class="ds-status-dot" aria-hidden="true"></span>
        <span>Interface system <span class="ds-mono">v1.0</span></span>
      </div>
    </aside>

    <div class="ds-main-column">
      <header class="ds-topbar">
        <div class="ds-topbar__breadcrumb">
          <span class="ds-mono">zenconvert</span>
          <span aria-hidden="true">/</span>
          <span>design-system</span>
        </div>
        <a class="ds-topbar__link" href="#components">
          Explorar componentes <ArrowDown :size="14" :stroke-width="1.75" aria-hidden="true" />
        </a>
        <ThemeToggle />
      </header>

      <main id="main-content" class="ds-content" tabindex="-1">
        <section id="overview" class="ds-hero" aria-labelledby="page-title">
          <div class="ds-hero__copy">
            <p class="ds-eyebrow">
              <span class="ds-eyebrow__mark">01</span> DESIGN SYSTEM / FOUNDATION
            </p>
            <h1 id="page-title">Uma interface<br />feita para <span>fluir.</span></h1>
            <p class="ds-hero__description">
              A linguagem visual do ZenConvert: precisa, acessível e sem ruído. Tokens e componentes
              prontos para transformar tarefas complexas em experiências simples.
            </p>
            <div class="ds-hero__meta">
              <UiBadge variant="success">Sistema ativo</UiBadge>
              <span class="ds-mono">Vue 3 <span aria-hidden="true">·</span> UI kit 1.0</span>
            </div>
          </div>

          <div class="ds-terminal" aria-label="Resumo técnico do sistema">
            <div class="ds-terminal__bar">
              <div class="ds-terminal__lights" aria-hidden="true">
                <span></span><span></span><span></span>
              </div>
              <span class="ds-mono">system.config</span>
              <span class="ds-terminal__live"><span class="ds-status-dot"></span> ONLINE</span>
            </div>
            <div class="ds-terminal__body">
              <p><span class="ds-terminal__prompt">›</span> interface.status</p>
              <p>
                <span class="ds-terminal__key">theme</span><span>=</span
                ><span class="ds-terminal__value">"deep-green"</span>
              </p>
              <p>
                <span class="ds-terminal__key">contrast</span><span>=</span
                ><span class="ds-terminal__value">"accessible"</span>
              </p>
              <p>
                <span class="ds-terminal__key">motion</span><span>=</span
                ><span class="ds-terminal__value">"reduced-aware"</span>
              </p>
              <p>
                <span class="ds-terminal__key">components</span><span>=</span
                ><span class="ds-terminal__number">18</span>
              </p>
              <p class="ds-terminal__ready">
                <Check
                  class="ds-terminal__prompt"
                  :size="14"
                  :stroke-width="2"
                  aria-hidden="true"
                />
                ready_for_humans<span class="ds-cursor" aria-hidden="true"></span>
              </p>
            </div>
          </div>
        </section>

        <div class="ds-section-heading">
          <div>
            <p class="ds-eyebrow">01 — FUNDAMENTOS</p>
            <h2>As peças do sistema</h2>
          </div>
          <p>Uma base visual consistente para cada detalhe da experiência.</p>
        </div>

        <section id="colors" class="ds-section" aria-labelledby="colors-title">
          <div class="ds-section__heading">
            <div>
              <p class="ds-section__index">FOUNDATION / 01</p>
              <h3 id="colors-title">Cor com propósito</h3>
            </div>
            <p class="ds-section__note">Selecione uma amostra para copiar seu valor hexadecimal.</p>
          </div>

          <div class="ds-color-groups">
            <div v-for="group in colorGroups" :key="group.name" class="ds-color-group">
              <h4>{{ group.name }}</h4>
              <div class="ds-swatches">
                <button
                  v-for="color in group.colors"
                  :key="color.token"
                  class="ds-swatch"
                  type="button"
                  :aria-label="`Copiar ${color.token}, ${color.value}`"
                  @click="copyToken(color.value)"
                >
                  <span class="ds-swatch__color" :style="{ backgroundColor: color.value }"></span>
                  <span class="ds-swatch__meta">
                    <span class="ds-mono">{{ color.token }}</span>
                    <span class="ds-swatch__value">{{ color.value }}</span>
                  </span>
                </button>
              </div>
            </div>
          </div>
          <div class="ds-live-message" role="status" aria-live="polite">
            <Transition name="ds-feedback">
              <span v-if="copyFeedback" :key="copyFeedback">{{ copyFeedback }}</span>
            </Transition>
          </div>
        </section>

        <section id="typography" class="ds-section" aria-labelledby="typography-title">
          <div class="ds-section__heading">
            <div>
              <p class="ds-section__index">FOUNDATION / 02</p>
              <h3 id="typography-title">Tipografia de interface</h3>
            </div>
            <p class="ds-section__note">
              Sans-serif para leitura. Monoespaçada para contexto técnico.
            </p>
          </div>

          <div class="ds-type-specimens">
            <div class="ds-type-specimen">
              <span class="ds-type-specimen__label">DISPLAY / 36</span>
              <p class="ds-type-display">Conversão simplificada.</p>
              <code>font-size: var(--text-3xl)</code>
            </div>
            <div class="ds-type-specimen">
              <span class="ds-type-specimen__label">HEADING / 22</span>
              <p class="ds-type-heading">Clareza em cada etapa</p>
              <code>font-size: var(--text-xl)</code>
            </div>
            <div class="ds-type-specimen ds-type-specimen--body">
              <span class="ds-type-specimen__label">BODY / 16</span>
              <p>Uma interface legível mantém o foco no que realmente importa: seu trabalho.</p>
              <code>line-height: var(--line-height-normal)</code>
            </div>
            <div class="ds-type-specimen ds-type-specimen--mono">
              <span class="ds-type-specimen__label">MONO / 14</span>
              <p>format: image/webp <span aria-hidden="true">→</span> quality: 82%</p>
              <code>font-family: var(--font-mono)</code>
            </div>
          </div>
        </section>

        <div id="components" class="ds-section-divider">
          <p class="ds-eyebrow">02 — COMPONENTES</p>
          <h2>Consistência em cada interação</h2>
          <p>Peças reutilizáveis, com estados acessíveis e comportamento previsível.</p>
        </div>

        <section id="actions" class="ds-section" aria-labelledby="actions-title">
          <div class="ds-section__heading">
            <div>
              <p class="ds-section__index">COMPONENTS / 01</p>
              <h3 id="actions-title">Ações e hierarquia</h3>
            </div>
            <p class="ds-section__note">
              Uma ação principal por contexto; alternativas com menos peso visual.
            </p>
          </div>

          <div class="ds-panel">
            <div class="ds-showcase-row">
              <span class="ds-showcase-label">Variantes</span>
              <div class="ds-control-row">
                <UiButton @click="showStateFeedback('Ação primária de demonstração acionada.')">
                  Primária <ArrowUpRight :size="16" :stroke-width="1.75" aria-hidden="true" />
                </UiButton>
                <UiButton
                  variant="secondary"
                  @click="showStateFeedback('Ação secundária de demonstração acionada.')"
                >
                  Secundária
                </UiButton>
                <UiButton
                  variant="ghost"
                  @click="showStateFeedback('Ação neutra de demonstração acionada.')"
                >
                  Neutra
                </UiButton>
                <UiButton
                  variant="danger"
                  @click="
                    showStateFeedback(
                      'Ação destrutiva de demonstração acionada; nenhum dado foi alterado.',
                    )
                  "
                >
                  Destrutiva
                </UiButton>
              </div>
            </div>
            <div class="ds-showcase-row">
              <span class="ds-showcase-label">Tamanhos e estados</span>
              <div class="ds-control-row">
                <UiButton
                  size="sm"
                  variant="secondary"
                  @click="showStateFeedback('Botão compacto de demonstração acionado.')"
                >
                  Compacta
                </UiButton>
                <UiButton
                  size="md"
                  @click="showStateFeedback('Botão padrão de demonstração acionado.')"
                >
                  Padrão
                </UiButton>
                <UiButton
                  size="lg"
                  @click="showStateFeedback('Botão em tamanho de destaque acionado.')"
                >
                  Destaque
                </UiButton>
                <span aria-hidden="true">
                  <UiButton loading disabled>Loading / amostra</UiButton>
                </span>
                <UiButton disabled variant="secondary">Desabilitada</UiButton>
                <UiIconButton
                  label="Exibir opções de demonstração"
                  title="Exibir opções de demonstração"
                  @click="showStateFeedback('Botão de ícone acionado.')"
                >
                  <MoreHorizontal :size="18" :stroke-width="1.75" aria-hidden="true" />
                </UiIconButton>
              </div>
            </div>
          </div>
        </section>

        <section id="forms" class="ds-section" aria-labelledby="forms-title">
          <div class="ds-section__heading">
            <div>
              <p class="ds-section__index">COMPONENTS / 02</p>
              <h3 id="forms-title">Controles de formulário</h3>
            </div>
            <p class="ds-section__note">
              Labels persistentes, validação associada e estados fáceis de reconhecer.
            </p>
          </div>

          <div class="ds-form-grid">
            <UiCard title="Campos de texto" description="Exemplo local — nenhum dado é enviado.">
              <form class="ds-form-stack" novalidate @submit.prevent="validateFilename">
                <UiInput
                  v-model="filename"
                  label="Nome do arquivo"
                  placeholder="ex.: projeto-final"
                  description="Use um nome curto, sem extensão."
                  :error="filenameError"
                  autocomplete="off"
                />
                <UiTextarea
                  label="Observações"
                  placeholder="Adicione uma nota opcional..."
                  :rows="3"
                />
                <UiSelect v-model="outputFormat" label="Formato de saída">
                  <option value="webp">WebP — leve para web</option>
                  <option value="png">PNG — sem perdas</option>
                  <option value="jpeg">JPEG — compatível</option>
                </UiSelect>
                <div class="ds-form-actions">
                  <UiButton type="submit">
                    Validar exemplo
                    <ArrowRight :size="16" :stroke-width="1.75" aria-hidden="true" />
                  </UiButton>
                </div>
              </form>
              <UiAlert
                v-if="formFeedback"
                class="ds-demo-alert"
                variant="success"
                title="Tudo certo"
                dismissible
                @dismiss="formFeedback = ''"
              >
                {{ formFeedback }}
              </UiAlert>
            </UiCard>

            <UiCard
              title="Preferências"
              description="Controles nativos, com apresentação consistente."
            >
              <div class="ds-form-stack ds-preferences">
                <UiRadioGroup
                  v-model="quality"
                  legend="Perfil de qualidade"
                  :options="radioOptions"
                />
                <div class="ds-preferences__divider"></div>
                <UiCheckbox
                  v-model="keepMetadata"
                  label="Preservar metadados"
                  description="Mantém informações do arquivo original."
                />
                <UiSwitch v-model="automaticMode" label="Ajuste automático" />
                <UiFormField
                  label="Identificador técnico"
                  for-id="sample-identifier"
                  description="Exemplo de campo personalizado com associação de descrição."
                  v-slot="{ descriptionId }"
                >
                  <input
                    id="sample-identifier"
                    class="ui-field__control"
                    type="text"
                    value="zc-001"
                    :aria-describedby="descriptionId"
                    readonly
                  />
                </UiFormField>
                <p class="ds-preference-output ds-mono" aria-live="polite">
                  {{ outputFormat }} / {{ quality }} / metadados {{ keepMetadata ? 'on' : 'off' }} /
                  auto {{ automaticMode ? 'on' : 'off' }}
                </p>
              </div>
            </UiCard>
          </div>
        </section>

        <section id="surfaces" class="ds-section" aria-labelledby="surfaces-title">
          <div class="ds-section__heading">
            <div>
              <p class="ds-section__index">COMPONENTS / 03</p>
              <h3 id="surfaces-title">Superfícies e contexto</h3>
            </div>
            <p class="ds-section__note">
              Agrupe informações relacionadas sem competir com o conteúdo.
            </p>
          </div>

          <div class="ds-surface-grid">
            <UiCard
              title="Arquivo demonstrativo"
              description="Dados ilustrativos do componente; nenhum arquivo real está conectado."
            >
              <div class="ds-file-row">
                <div class="ds-file-icon" aria-hidden="true">
                  <FileImage :size="20" :stroke-width="1.6" />
                </div>
                <div class="ds-file-copy">
                  <strong>exemplo-imagem.png</strong>
                  <span>Exemplo: 4,8 MB <span aria-hidden="true">→</span> 1,2 MB</span>
                </div>
                <UiBadge variant="success">−75%</UiBadge>
              </div>
              <template #footer>
                <UiButton
                  variant="secondary"
                  size="sm"
                  @click="showStateFeedback('Resumo demonstrativo do arquivo selecionado.')"
                >
                  Ver resumo
                </UiButton>
                <UiButton
                  size="sm"
                  @click="
                    showStateFeedback(
                      'Ação de download ilustrativa; nenhum arquivo de backend está conectado.',
                    )
                  "
                >
                  Testar ação <ArrowDown :size="15" :stroke-width="1.75" aria-hidden="true" />
                </UiButton>
              </template>
            </UiCard>

            <div class="ds-badge-card">
              <span class="ds-showcase-label">Badges / estado</span>
              <div class="ds-badge-list">
                <UiBadge>Em fila</UiBadge>
                <UiBadge variant="success"
                  ><span class="ds-status-dot" aria-hidden="true"></span> Concluído</UiBadge
                >
                <UiBadge variant="warning">Atenção</UiBadge>
                <UiBadge variant="danger">Falhou</UiBadge>
              </div>
              <p class="ds-muted-copy">O texto mantém o significado sem depender apenas da cor.</p>
            </div>
          </div>
        </section>

        <section id="feedback" class="ds-section" aria-labelledby="feedback-title">
          <div class="ds-section__heading">
            <div>
              <p class="ds-section__index">COMPONENTS / 04</p>
              <h3 id="feedback-title">Feedback e mensagens</h3>
            </div>
            <p class="ds-section__note">
              Mensagens próximas à ação, com semântica apropriada para leitores de tela.
            </p>
          </div>

          <div class="ds-feedback-stack">
            <UiAlert :announce="false" variant="success" title="Exemplo visual · sucesso">
              Seu arquivo está pronto para baixar.
            </UiAlert>
            <UiAlert :announce="false" variant="warning" title="Exemplo visual · atenção">
              Arquivos acima de 20 MB podem levar mais tempo para processar.
            </UiAlert>
            <UiAlert :announce="false" variant="error" title="Exemplo visual · erro" dismissible>
              Escolha um arquivo PNG, JPEG ou WebP para continuar.
            </UiAlert>
          </div>
        </section>

        <section id="states" class="ds-section" aria-labelledby="states-title">
          <div class="ds-section__heading">
            <div>
              <p class="ds-section__index">COMPONENTS / 05</p>
              <h3 id="states-title">Estados, carregamento e navegação</h3>
            </div>
            <p class="ds-section__note">
              Orientação clara enquanto o conteúdo carrega, está vazio ou precisa de atenção.
            </p>
          </div>

          <div class="ds-state-grid">
            <UiCard title="Carregando">
              <div class="ds-loading-row">
                <UiSpinner size="sm" decorative />
                <UiSpinner decorative />
                <UiSpinner size="lg" decorative />
              </div>
              <div class="ds-skeleton-stack" aria-label="Prévia de conteúdo carregando">
                <UiSkeleton height="0.75rem" width="38%" />
                <UiSkeleton height="1rem" width="92%" />
                <UiSkeleton height="1rem" width="72%" />
              </div>
            </UiCard>

            <UiCard title="Conteúdo sem resultados">
              <UiEmptyState
                title="Sua fila está vazia"
                description="Adicione um arquivo para começar uma nova conversão."
                :announce="false"
              >
                <template #icon>
                  <span class="ds-empty-icon" aria-hidden="true">
                    <Plus :size="22" :stroke-width="1.75" />
                  </span>
                </template>
                <template #action>
                  <UiButton
                    @click="
                      showStateFeedback('A seleção de arquivos depende da integração do produto.')
                    "
                  >
                    Adicionar arquivo
                  </UiButton>
                </template>
              </UiEmptyState>
            </UiCard>

            <UiCard title="Falha recuperável">
              <UiErrorState
                title="Não foi possível carregar"
                description="Verifique a conexão e tente novamente. Este exemplo não chama um serviço."
                :announce="false"
              >
                <template #action>
                  <UiButton
                    variant="secondary"
                    @click="
                      showStateFeedback(
                        'Ação de demonstração acionada; não há serviço conectado para repetir a solicitação.',
                      )
                    "
                  >
                    Tentar novamente
                  </UiButton>
                </template>
              </UiErrorState>
            </UiCard>

            <UiCard
              title="Navegação estrutural"
              description="Indica a localização atual na hierarquia."
            >
              <UiBreadcrumbs
                :items="[
                  { label: 'Arquivos', href: '#overview' },
                  { label: 'Conversões', href: '#surfaces' },
                  { label: 'Detalhes' },
                ]"
              />
              <div class="ds-pagination-example">
                <span class="ds-showcase-label">Paginação · {{ page }} de 12</span>
                <UiPagination v-model="page" :page-count="12" />
              </div>
            </UiCard>
          </div>
          <div class="ds-status-region" role="status" aria-live="polite">
            <Transition name="ds-feedback" mode="out-in">
              <p v-if="stateFeedback" :key="stateFeedback" class="ds-interaction-note">
                {{ stateFeedback }}
              </p>
            </Transition>
          </div>
        </section>

        <section id="motion" class="ds-section" aria-labelledby="motion-title">
          <div class="ds-section__heading">
            <div>
              <p class="ds-section__index">FOUNDATION / 03</p>
              <h3 id="motion-title">Movimento com intenção</h3>
            </div>
            <p class="ds-section__note">
              Transições curtas reforçam a resposta sem atrasar a ação.
            </p>
          </div>

          <div class="ds-motion-grid">
            <UiCard
              title="Escala de movimento"
              description="Valores compartilhados pelos componentes."
            >
              <div class="ds-motion-tokens">
                <div>
                  <span class="ds-motion-sample ds-motion-sample--fast" aria-hidden="true"></span>
                  <span class="ds-motion-tokens__value ds-mono">120 ms</span>
                  <span class="ds-motion-tokens__label">resposta rápida</span>
                </div>
                <div>
                  <span class="ds-motion-sample ds-motion-sample--normal" aria-hidden="true"></span>
                  <span class="ds-motion-tokens__value ds-mono">180 ms</span>
                  <span class="ds-motion-tokens__label">mudança de estado</span>
                </div>
                <div>
                  <span
                    class="ds-motion-sample ds-motion-sample--distance"
                    aria-hidden="true"
                  ></span>
                  <span class="ds-motion-tokens__value ds-mono">4 px</span>
                  <span class="ds-motion-tokens__label">deslocamento máximo</span>
                </div>
              </div>
            </UiCard>

            <UiCard title="Acessibilidade primeiro">
              <p class="ds-motion-copy">
                Hover, pressão, foco e feedback usam os tokens do sistema. Com
                <code>prefers-reduced-motion</code>, transições e animações são reduzidas e a
                rolagem suave é desativada.
              </p>
              <p class="ds-motion-copy ds-motion-copy--muted">
                Menus, diálogos e drawers ainda não fazem parte do produto; suas animações devem ser
                definidas junto às interações reais, não simuladas nesta página.
              </p>
            </UiCard>
          </div>
        </section>

        <footer class="ds-footer">
          <span>ZENCONVERT <span aria-hidden="true">/</span> INTERFACE SYSTEM</span>
          <span class="ds-mono">feito para fluir<span class="ds-footer__dot">.</span></span>
        </footer>
      </main>
    </div>
  </div>
</template>

<style scoped>
.ds-shell {
  --ds-sidebar-width: 15.5rem;

  min-height: 100vh;
  background:
    radial-gradient(
      ellipse at 86% 0%,
      color-mix(in srgb, var(--color-accent) 9%, transparent),
      transparent 31rem
    ),
    var(--color-surface-canvas);
}

.ds-skip-link {
  position: fixed;
  z-index: 100;
  top: var(--space-3);
  left: var(--space-3);
  padding: var(--space-3) var(--space-4);
  transform: translateY(-160%);
  border-radius: var(--radius-md);
  background: var(--color-accent);
  color: var(--color-text-inverse);
  font-weight: var(--font-weight-semibold);
}

.ds-skip-link:focus {
  transform: translateY(0);
}

.ds-sidebar {
  position: fixed;
  z-index: var(--layer-sticky);
  top: 0;
  bottom: 0;
  left: 0;
  display: flex;
  width: var(--ds-sidebar-width);
  flex-direction: column;
  padding: var(--space-6) var(--space-4) var(--space-4);
  border-right: 1px solid var(--color-border);
  background: color-mix(in srgb, var(--color-surface-canvas) 92%, transparent);
  backdrop-filter: blur(16px);
}

.ds-wordmark {
  display: inline-flex;
  align-items: center;
  gap: var(--space-3);
  width: fit-content;
  color: var(--color-text-primary);
  font-size: var(--text-md);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--tracking-tight);
  text-decoration: none;
}

.ds-wordmark__symbol {
  display: grid;
  width: 2rem;
  height: 2rem;
  place-items: center;
  border: 1px solid var(--color-green-700);
  border-radius: var(--radius-sm);
  background: var(--color-green-900);
  color: var(--color-green-300);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  letter-spacing: -0.08em;
}

.ds-wordmark__accent {
  color: var(--color-green-300);
}

.ds-sidebar__caption {
  margin: var(--space-10) 0 var(--space-3) var(--space-2);
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  font-size: 0.625rem;
  letter-spacing: 0.12em;
}

.ds-navigation {
  display: grid;
  gap: var(--space-1);
}

.ds-navigation__link {
  display: flex;
  min-height: 2.5rem;
  align-items: center;
  gap: var(--space-3);
  padding: 0 var(--space-2);
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  color: var(--color-text-muted);
  font-size: var(--text-sm);
  text-decoration: none;
  transition:
    background var(--duration-fast) var(--ease-standard),
    border-color var(--duration-fast) var(--ease-standard),
    color var(--duration-fast) var(--ease-standard);
}

.ds-navigation__link:hover {
  border-color: var(--color-border);
  background: var(--color-surface-raised);
  color: var(--color-text-primary);
}

.ds-navigation__index {
  width: 1.5rem;
  color: var(--color-gray-500);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
}

.ds-sidebar__footer {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-top: auto;
  padding: var(--space-4) var(--space-2) 0;
  border-top: 1px solid var(--color-border);
  color: var(--color-text-muted);
  font-size: var(--text-xs);
}

.ds-status-dot {
  display: inline-block;
  width: 0.4375rem;
  height: 0.4375rem;
  flex: 0 0 auto;
  border-radius: 50%;
  background: var(--color-green-400);
  box-shadow: 0 0 10px color-mix(in srgb, var(--color-success) 38%, transparent);
}

.ds-main-column {
  min-width: 0;
  margin-left: var(--ds-sidebar-width);
}

.ds-topbar {
  position: sticky;
  z-index: var(--layer-sticky);
  top: 0;
  display: flex;
  min-height: 3.75rem;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  padding: 0 clamp(var(--space-5), 5vw, var(--space-12));
  border-bottom: 1px solid color-mix(in srgb, var(--color-border) 70%, transparent);
  background: color-mix(in srgb, var(--color-surface-canvas) 82%, transparent);
  backdrop-filter: blur(16px);
}

.ds-topbar__breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--color-text-muted);
  font-size: var(--text-xs);
}

.ds-topbar__link {
  color: var(--color-green-300);
  font-size: var(--text-xs);
  font-weight: var(--font-weight-medium);
  text-decoration: none;
}

.ds-topbar__link:hover {
  color: var(--color-white);
}

.ds-content {
  width: min(100%, calc(var(--content-width) + 2 * clamp(var(--space-5), 5vw, var(--space-12))));
  margin-inline: auto;
  padding: 0 clamp(var(--space-5), 5vw, var(--space-12));
}

.ds-hero {
  display: grid;
  min-height: 27rem;
  grid-template-columns: minmax(0, 1.1fr) minmax(19rem, 0.9fr);
  align-items: center;
  gap: clamp(var(--space-8), 6vw, var(--space-12));
  padding-block: clamp(var(--space-10), 8vw, 6.5rem);
  border-bottom: 1px solid var(--color-border);
}

.ds-eyebrow,
.ds-section__index {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin: 0;
  color: var(--color-green-300);
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  letter-spacing: 0.1em;
}

.ds-eyebrow__mark {
  display: grid;
  width: 1.5rem;
  height: 1.5rem;
  place-items: center;
  border: 1px solid var(--color-green-700);
  border-radius: var(--radius-sm);
  background: var(--color-green-900);
  font-size: 0.625rem;
}

.ds-hero h1 {
  margin: var(--space-5) 0 var(--space-4);
  font-size: clamp(2.75rem, 5.3vw, 4.5rem);
  font-weight: var(--font-weight-semibold);
  letter-spacing: -0.065em;
  line-height: 0.99;
}

.ds-hero h1 span {
  color: var(--color-green-300);
}

.ds-hero__description {
  max-width: 35rem;
  margin: 0;
  color: var(--color-text-secondary);
  font-size: var(--text-md);
  line-height: var(--line-height-relaxed);
}

.ds-hero__meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-4);
  margin-top: var(--space-6);
  color: var(--color-text-muted);
  font-size: var(--text-xs);
}

.ds-mono {
  font-family: var(--font-mono);
}

.ds-terminal {
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface-raised);
  box-shadow: var(--shadow-raised);
}

.ds-terminal__bar {
  display: flex;
  min-height: 2.75rem;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  padding: 0 var(--space-4);
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-muted);
  font-size: var(--text-xs);
}

.ds-terminal__lights {
  display: flex;
  gap: 0.375rem;
}

.ds-terminal__lights span {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: var(--color-gray-700);
}

.ds-terminal__lights span:first-child {
  background: var(--color-green-500);
}

.ds-terminal__live {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--color-green-300);
  font-family: var(--font-mono);
  font-size: 0.625rem;
}

.ds-terminal__body {
  display: grid;
  gap: var(--space-3);
  padding: var(--space-5);
  color: var(--color-gray-300);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
}

.ds-terminal__body p {
  display: flex;
  gap: var(--space-2);
  margin: 0;
}

.ds-terminal__prompt,
.ds-terminal__ready {
  color: var(--color-green-300);
}

.ds-terminal__key {
  color: var(--color-blue-300);
}

.ds-terminal__value {
  color: var(--color-amber-300);
}

.ds-terminal__number {
  color: var(--color-green-300);
}

.ds-terminal__ready {
  margin-top: var(--space-2) !important;
}

.ds-cursor {
  display: inline-block;
  width: 0.4rem;
  height: 0.8rem;
  align-self: center;
  margin-left: var(--space-1);
  background: var(--color-green-400);
  animation: ds-blink 1s steps(2, start) infinite;
}

@keyframes ds-blink {
  to {
    visibility: hidden;
  }
}

.ds-section-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: var(--space-6);
  padding: var(--space-12) 0 var(--space-4);
}

.ds-section-heading h2,
.ds-section-divider h2 {
  margin: var(--space-2) 0 0;
  font-size: var(--text-2xl);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--tracking-tight);
}

.ds-section-heading > p,
.ds-section-divider > p:last-child {
  max-width: 23rem;
  margin: 0;
  color: var(--color-text-muted);
  font-size: var(--text-sm);
}

.ds-section {
  scroll-margin-top: 5rem;
  padding-block: var(--space-8);
  border-top: 1px solid var(--color-border);
}

.ds-section__heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: var(--space-5);
  margin-bottom: var(--space-5);
}

.ds-section__index {
  color: var(--color-text-muted);
  font-size: 0.625rem;
}

.ds-section__heading h3 {
  margin: var(--space-2) 0 0;
  font-size: var(--text-xl);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--tracking-tight);
}

.ds-section__note {
  max-width: 25rem;
  margin: 0;
  color: var(--color-text-muted);
  font-size: var(--text-xs);
  text-align: right;
}

.ds-color-groups {
  display: grid;
  gap: var(--space-5);
}

.ds-color-group {
  padding: var(--space-4);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface-raised);
}

.ds-color-group h4 {
  margin: 0 0 var(--space-3);
  color: var(--color-text-secondary);
  font-size: var(--text-xs);
  font-weight: var(--font-weight-medium);
}

.ds-swatches {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: var(--space-2);
}

.ds-swatch {
  display: grid;
  min-width: 0;
  gap: var(--space-2);
  padding: 0;
  border: 0;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--color-text-primary);
  cursor: pointer;
  text-align: left;
}

.ds-swatch__color {
  min-height: 3.25rem;
  border: 1px solid color-mix(in srgb, var(--color-text-primary) 13%, transparent);
  border-radius: var(--radius-sm);
  transition:
    transform var(--duration-fast) var(--ease-standard),
    border-color var(--duration-fast) var(--ease-standard);
}

.ds-swatch:hover .ds-swatch__color {
  transform: translateY(-2px);
  border-color: var(--color-gray-300);
}

.ds-swatch__meta {
  display: grid;
  gap: 0.125rem;
  padding-inline: 0.125rem;
}

.ds-swatch__meta .ds-mono,
.ds-swatch__value {
  overflow: hidden;
  font-size: 0.625rem;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ds-swatch__meta .ds-mono {
  color: var(--color-text-secondary);
}

.ds-swatch__value {
  color: var(--color-text-muted);
  font-family: var(--font-mono);
}

.ds-live-message {
  min-height: 1.25rem;
  margin: var(--space-2) 0 0;
  color: var(--color-success);
  font-size: var(--text-xs);
}

.ds-feedback-enter-active,
.ds-feedback-leave-active {
  transition:
    opacity var(--duration-normal) var(--ease-standard),
    transform var(--duration-normal) var(--ease-standard);
}

.ds-feedback-enter-from,
.ds-feedback-leave-to {
  transform: translateY(var(--space-1));
  opacity: 0;
}

.ds-live-message .ds-feedback-enter-from,
.ds-live-message .ds-feedback-leave-to {
  transform: translateY(2px);
}

.ds-type-specimens {
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface-raised);
}

.ds-type-specimen {
  display: grid;
  grid-template-columns: 8rem minmax(0, 1fr) minmax(10rem, 0.65fr);
  align-items: center;
  gap: var(--space-4);
  min-height: 5.5rem;
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
}

.ds-type-specimen:last-child {
  border-bottom: 0;
}

.ds-type-specimen__label,
.ds-type-specimen code {
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  font-size: 0.625rem;
}

.ds-type-specimen p {
  margin: 0;
  color: var(--color-text-primary);
}

.ds-type-specimen code {
  overflow-wrap: anywhere;
  text-align: right;
}

.ds-type-display {
  font-size: var(--text-2xl);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--tracking-tight);
  line-height: var(--line-height-tight);
}

.ds-type-heading {
  font-size: var(--text-lg);
  font-weight: var(--font-weight-medium);
}

.ds-type-specimen--body p {
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
}

.ds-type-specimen--mono p {
  color: var(--color-green-300);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
}

.ds-section-divider {
  scroll-margin-top: 5rem;
  padding: var(--space-10) 0 var(--space-6);
  border-top: 1px solid var(--color-border);
}

.ds-section-divider > p:last-child {
  margin-top: var(--space-2);
}

.ds-panel {
  display: grid;
  gap: var(--space-6);
  padding: var(--space-5);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface-raised);
}

.ds-showcase-row {
  display: grid;
  gap: var(--space-3);
}

.ds-showcase-label {
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  font-size: 0.625rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.ds-control-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-3);
}

.ds-form-grid,
.ds-surface-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: start;
  gap: var(--space-4);
}

.ds-form-stack {
  display: grid;
  gap: var(--space-4);
}

.ds-form-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: var(--space-1);
}

.ds-demo-alert {
  margin-top: var(--space-4);
}

.ds-preferences {
  padding-top: var(--space-1);
}

.ds-preferences__divider {
  height: 1px;
  background: var(--color-border);
}

.ds-preference-output {
  overflow-wrap: anywhere;
  margin: 0;
  padding: var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-muted);
  color: var(--color-green-300);
  font-size: 0.6875rem;
}

.ds-file-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-muted);
}

.ds-file-icon {
  display: grid;
  width: 2.5rem;
  height: 2.5rem;
  flex: 0 0 auto;
  place-items: center;
  border: 1px solid var(--color-green-700);
  border-radius: var(--radius-sm);
  background: var(--color-green-900);
  color: var(--color-green-300);
  font-family: var(--font-mono);
  font-size: 0.5625rem;
}

.ds-file-copy {
  display: grid;
  min-width: 0;
  flex: 1;
  gap: 0.125rem;
}

.ds-file-copy strong {
  overflow: hidden;
  font-size: var(--text-xs);
  font-weight: var(--font-weight-medium);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ds-file-copy span,
.ds-muted-copy {
  color: var(--color-text-muted);
  font-size: var(--text-xs);
}

.ds-badge-card {
  display: grid;
  min-height: 100%;
  align-content: center;
  gap: var(--space-4);
  padding: var(--space-5);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface-raised);
}

.ds-badge-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.ds-muted-copy {
  margin: 0;
}

.ds-feedback-stack {
  display: grid;
  gap: var(--space-3);
}

.ds-state-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
}

.ds-loading-row {
  display: flex;
  min-height: 2.5rem;
  align-items: center;
  gap: var(--space-5);
}

.ds-skeleton-stack {
  display: grid;
  gap: var(--space-2);
  margin-top: var(--space-4);
}

.ds-empty-icon {
  display: grid;
  width: 2.75rem;
  height: 2.75rem;
  place-items: center;
  border: 1px solid var(--color-green-700);
  border-radius: var(--radius-lg);
  background: var(--color-green-900);
  color: var(--color-green-300);
  font-size: var(--text-xl);
}

.ds-pagination-example {
  display: grid;
  gap: var(--space-3);
  margin-top: var(--space-6);
}

.ds-interaction-note {
  margin: var(--space-4) 0 0;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-green-700);
  border-radius: var(--radius-md);
  background: var(--color-success-surface);
  color: var(--color-success);
  font-size: var(--text-sm);
}

.ds-status-region {
  min-height: 4rem;
}

.ds-motion-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
}

.ds-motion-tokens {
  display: grid;
  gap: var(--space-4);
}

.ds-motion-tokens > div {
  display: grid;
  grid-template-columns: 2rem minmax(5rem, auto) minmax(0, 1fr);
  align-items: center;
  gap: var(--space-3);
}

.ds-motion-sample {
  width: 1.5rem;
  height: 1.5rem;
  border: 1px solid var(--color-green-700);
  border-radius: var(--radius-sm);
  background: var(--color-green-900);
}

.ds-motion-sample--fast {
  transition: transform var(--duration-fast) var(--ease-standard);
}

.ds-motion-sample--normal {
  transition: transform var(--duration-normal) var(--ease-standard);
}

.ds-motion-tokens > div:hover .ds-motion-sample--fast,
.ds-motion-tokens > div:hover .ds-motion-sample--normal {
  transform: translateX(var(--space-2));
  background: var(--color-green-700);
}

.ds-motion-sample--distance {
  transition: transform var(--duration-normal) var(--ease-standard);
}

.ds-motion-tokens > div:hover .ds-motion-sample--distance {
  transform: translateX(var(--space-1));
  background: var(--color-green-700);
}

.ds-motion-tokens__value {
  color: var(--color-green-300);
  font-size: var(--text-xs);
}

.ds-motion-tokens__label {
  color: var(--color-text-secondary);
  font-size: var(--text-xs);
}

.ds-motion-copy {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
}

.ds-motion-copy + .ds-motion-copy {
  margin-top: var(--space-3);
}

.ds-motion-copy code {
  padding: 0.1em 0.35em;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface-muted);
  color: var(--color-green-300);
  font-family: var(--font-mono);
  font-size: 0.85em;
}

.ds-motion-copy--muted {
  color: var(--color-text-muted);
  font-size: var(--text-xs);
}

.ds-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  margin-top: var(--space-8);
  padding: var(--space-5) 0 var(--space-8);
  border-top: 1px solid var(--color-border);
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  font-size: 0.625rem;
  letter-spacing: 0.06em;
}

.ds-footer__dot {
  color: var(--color-green-300);
}

@media (prefers-reduced-motion: reduce) {
  .ds-cursor {
    animation: none;
  }
}

@media (max-width: 68rem) {
  .ds-sidebar {
    width: 13.5rem;
  }

  .ds-main-column {
    margin-left: 13.5rem;
  }

  .ds-hero {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--space-6);
  }

  .ds-terminal {
    max-width: 38rem;
  }

  .ds-type-specimen {
    grid-template-columns: 6rem minmax(0, 1fr);
  }

  .ds-type-specimen code {
    grid-column: 2;
    text-align: left;
  }
}

@media (max-width: 48rem) {
  .ds-sidebar {
    position: sticky;
    z-index: calc(var(--layer-sticky) + 1);
    top: 0;
    bottom: auto;
    width: 100%;
    height: auto;
    padding: var(--space-3) var(--space-4) 0;
    border-right: 0;
    border-bottom: 1px solid var(--color-border);
    background: color-mix(in srgb, var(--color-surface-canvas) 96%, transparent);
  }

  .ds-wordmark {
    min-height: 2.5rem;
  }

  .ds-sidebar__caption,
  .ds-sidebar__footer {
    display: none;
  }

  .ds-navigation {
    display: flex;
    overflow-x: auto;
    gap: var(--space-1);
    margin: var(--space-2) calc(-1 * var(--space-1)) 0;
    padding: 0 var(--space-1) var(--space-2);
    scrollbar-width: thin;
    scrollbar-color: var(--color-gray-700) transparent;
  }

  .ds-navigation::-webkit-scrollbar {
    height: 0.25rem;
  }

  .ds-navigation::-webkit-scrollbar-track {
    background: transparent;
  }

  .ds-navigation::-webkit-scrollbar-thumb {
    border-radius: var(--radius-pill);
    background: var(--color-gray-700);
  }

  .ds-navigation__link {
    min-height: 2.25rem;
    flex: 0 0 auto;
    gap: var(--space-2);
    padding-inline: var(--space-2);
    font-size: var(--text-xs);
  }

  .ds-navigation__index {
    width: auto;
    font-size: 0.625rem;
  }

  .ds-main-column {
    margin-left: 0;
  }

  .ds-topbar {
    position: static;
    min-height: 3.25rem;
    padding-inline: var(--space-5);
  }

  .ds-content {
    padding-inline: var(--space-5);
  }

  .ds-hero {
    min-height: auto;
    padding-block: var(--space-10);
  }

  .ds-hero h1 {
    font-size: clamp(2.6rem, 11vw, 4rem);
  }

  .ds-section-heading,
  .ds-section__heading {
    align-items: flex-start;
    flex-direction: column;
  }

  .ds-section-heading {
    padding-top: var(--space-8);
  }

  .ds-section-heading > p,
  .ds-section__note {
    max-width: 34rem;
    text-align: left;
  }

  .ds-form-grid,
  .ds-surface-grid,
  .ds-state-grid,
  .ds-motion-grid {
    grid-template-columns: minmax(0, 1fr);
  }
}

@media (max-width: 36rem) {
  .ds-topbar__link {
    font-size: 0;
  }

  .ds-topbar__link span {
    font-size: var(--text-md);
  }

  .ds-swatches {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .ds-type-specimen {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--space-2);
    padding: var(--space-4);
  }

  .ds-type-specimen code {
    grid-column: auto;
  }

  .ds-type-display {
    font-size: var(--text-xl);
  }

  .ds-panel {
    padding: var(--space-4);
  }

  .ds-control-row {
    gap: var(--space-2);
  }

  .ds-footer {
    align-items: flex-start;
    flex-direction: column;
    gap: var(--space-2);
  }
}
</style>
