import { onBeforeUnmount, reactive } from 'vue'
import { convertFile } from '@/services/conversionApi'
import { downloadZip, getExtension } from '@/utils/files'

function createState(tool) {
  return {
    entries: [],
    running: false,
    zipping: false,
    message: '',
    options: tool.option ? { [tool.option.param]: tool.option.defaultValue } : {},
  }
}

function releaseResult(entry) {
  if (entry.result) URL.revokeObjectURL(entry.result.url)
}

/**
 * Estado e ações de conversão por ferramenta.
 * Cada entrada: { key, file, status: idle | converting | done | error, progress, error, result }.
 */
export function useConversions(tools, { onConverted } = {}) {
  const state = reactive(Object.fromEntries(tools.map((tool) => [tool.id, createState(tool)])))
  const controllers = new Map()

  function addFiles(tool, files) {
    const current = state[tool.id]
    const accepted = files.filter((file) => tool.extensions.includes(getExtension(file.name)))
    const rejected = files.length - accepted.length

    for (const file of accepted) {
      const key = `${file.name}-${file.size}-${file.lastModified}`
      if (!current.entries.some((entry) => entry.key === key)) {
        current.entries.push({ key, file, status: 'idle', progress: 0, error: '', result: null })
      }
    }

    current.message =
      rejected > 0 ? `${rejected} arquivo(s) ignorado(s). Formatos aceitos: ${tool.formats}.` : ''
    return { accepted: accepted.length, rejected }
  }

  function removeFile(toolId, index) {
    const [removed] = state[toolId].entries.splice(index, 1)
    releaseResult(removed)
    state[toolId].message = ''
  }

  function pendingCount(toolId) {
    return state[toolId].entries.filter(({ status }) => status !== 'done').length
  }

  function doneEntries(toolId) {
    return state[toolId].entries.filter(({ status }) => status === 'done')
  }

  async function convertAll(tool) {
    const current = state[tool.id]
    if (current.running) return
    const controller = new AbortController()
    controllers.set(tool.id, controller)
    current.running = true
    current.message = ''

    try {
      for (const entry of current.entries.filter(({ status }) => status !== 'done')) {
        if (controller.signal.aborted) break
        entry.status = 'converting'
        entry.progress = 0
        entry.error = ''
        try {
          const { blob, filename } = await convertFile({
            target: tool.target,
            file: entry.file,
            params: { ...current.options },
            signal: controller.signal,
            onUploadProgress: (progress) => {
              entry.progress = progress
            },
          })
          entry.result = { url: URL.createObjectURL(blob), filename, blob }
          entry.status = 'done'
          onConverted?.({ entry, tool })
        } catch (error) {
          if (error.cancelled) {
            entry.status = 'idle'
            current.message = 'Conversão cancelada. Os arquivos restantes não foram enviados.'
            break
          }
          entry.status = 'error'
          entry.error = error.message
        }
      }
    } finally {
      current.running = false
      controllers.delete(tool.id)
    }
  }

  function cancel(tool) {
    controllers.get(tool.id)?.abort()
  }

  async function downloadAll(tool) {
    const current = state[tool.id]
    const items = doneEntries(tool.id).map(({ result }) => result)
    if (current.zipping || items.length < 2) return
    current.zipping = true
    current.message = ''
    try {
      await downloadZip(items, `zenconvert-${tool.id}.zip`)
    } catch {
      current.message = 'Não foi possível gerar o ZIP. Baixe os arquivos individualmente.'
    } finally {
      current.zipping = false
    }
  }

  onBeforeUnmount(() => {
    controllers.forEach((controller) => controller.abort())
    Object.values(state).forEach(({ entries }) => entries.forEach(releaseResult))
  })

  return { state, addFiles, removeFile, pendingCount, doneEntries, convertAll, cancel, downloadAll }
}
