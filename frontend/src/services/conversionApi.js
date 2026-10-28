import axios from 'axios'

const http = axios.create({
  baseURL: (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, ''),
  responseType: 'blob',
})

export class ConversionError extends Error {
  constructor(message, { cancelled = false } = {}) {
    super(message)
    this.name = 'ConversionError'
    this.cancelled = cancelled
  }
}

function filenameFromHeader(header, fallback) {
  const encoded = /filename\*=UTF-8''([^;]+)/i.exec(header ?? '')
  if (!encoded) return fallback
  try {
    return decodeURIComponent(encoded[1])
  } catch {
    return fallback
  }
}

// Com responseType 'blob', o corpo de erro também chega como Blob.
async function readError(error) {
  try {
    const body = JSON.parse(await error.response.data.text())
    if (typeof body.detail === 'string') return body.detail
    if (Array.isArray(body.detail)) return 'Parâmetros de conversão inválidos.'
  } catch {
    // resposta sem JSON: usa a mensagem genérica abaixo
  }
  return 'Não foi possível converter o arquivo.'
}

/**
 * @param {object} options
 * @param {string} options.target destino da conversão (ex.: 'word')
 * @param {File} options.file
 * @param {Record<string, string>} [options.params]
 * @param {AbortSignal} [options.signal]
 * @param {(progress: number) => void} [options.onUploadProgress] fração de 0 a 1
 */
export async function convertFile({ target, file, params = {}, signal, onUploadProgress }) {
  const body = new FormData()
  body.append('arquivo', file)

  try {
    const response = await http.post(`/api/conversoes/${target}`, body, {
      params,
      signal,
      onUploadProgress: (event) => {
        if (event.progress !== undefined) onUploadProgress?.(event.progress)
      },
    })
    const fallbackName = `${file.name.replace(/\.[^.]+$/, '')}-convertido`
    return {
      blob: response.data,
      filename: filenameFromHeader(response.headers['content-disposition'], fallbackName),
    }
  } catch (error) {
    if (axios.isCancel(error))
      throw new ConversionError('Conversão cancelada.', { cancelled: true })
    if (error.response) throw new ConversionError(await readError(error))
    throw new ConversionError('Não foi possível conectar ao servidor. Tente novamente.')
  }
}
