# UI components

The shared UI primitives live in `src/components/ui` and are exported from
`src/components/ui/index.js`. They use the semantic CSS variables in
`src/assets/styles/main.css`; import that stylesheet once from the app entry point.
The visual catalog and interactive examples are available at the `/` route
(`src/views/DesignSystem.vue`).
Icons use `@lucide/vue` as lightweight Vue components. Import only the icons needed
by a view, set decorative icons to `aria-hidden="true"`, and give every icon-only
control an accessible name on its button.

## Conventions

- Components are prefixed with `Ui` and use native HTML controls where possible.
- Use `v-model` with `UiInput`, `UiTextarea`, `UiSelect`, `UiCheckbox`, `UiRadioGroup`,
  `UiSwitch`, and `UiPagination`.
- Form controls expose their own label and connect descriptions and errors to the control.
  Use `UiFormField` for custom slotted controls and apply its `descriptionId` and `errorId`
  slot props to the control's `aria-describedby`.
- Buttons are `type="button"` by default. Choose a visual `variant` and `size`; use
  `loading` for an in-progress action and provide an accessible `label` for icon-only buttons.
- `UiAlert` is for feedback that belongs in the page flow. Use `error` for assertive,
  important errors; other variants use a polite status announcement. Set `announce` to
  `false` only for static visual examples that must not be announced as real events.
- `UiEmptyState` and `UiErrorState` provide distinct empty and failure messages. Put
  any real retry or create action in their `action` slot.
- `UiSkeleton` is decorative and hidden from assistive technology. Pair it with an
  appropriate loading status when the wait itself needs to be announced.
- `UiSpinner` announces a loading status by default. Use `decorative` only when it is a
  static visual specimen rather than an operation currently in progress.
- `UiBreadcrumbs` receives `{ label, href? }` items. The last item is always rendered
  as the current page rather than a link.
- Motion uses `--duration-fast` (120 ms), `--duration-normal` (180 ms), and
  `--ease-standard`. Keep state transitions short, favor opacity and small transforms,
  and preserve visible focus. The global reduced-motion rule disables smooth scrolling
  and reduces animation and transition durations.
- `UiAlert` dismissal and form feedback use short enter/leave transitions. Loading
  indicators describe only actual loading states; do not show a spinner or progress
  indicator for an operation that is not running.

## Example

```vue
<script setup>
import { ref } from 'vue'
import { UiAlert, UiButton, UiInput } from '@/components/ui'

const filename = ref('')
</script>

<template>
  <form>
    <UiInput
      v-model="filename"
      label="Nome do arquivo"
      description="Escolha um nome fácil de reconhecer."
      autocomplete="off"
    />
    <UiAlert v-if="filename.length > 80" variant="warning" title="Nome longo">
      O nome pode ser difícil de ler em telas pequenas.
    </UiAlert>
    <UiButton type="submit">Continuar</UiButton>
  </form>
</template>
```

No product-specific dialogs, menus, tabs, notifications, or application shell are
included yet: add those when a real screen needs their interaction and lifecycle.
