# ZenConvert

O **ZenConvert** é uma aplicação web para converter arquivos entre formatos comuns sem precisar instalar um programa para cada tipo de arquivo. Escolha um formato de destino, envie um ou mais arquivos e baixe o resultado convertido.

O projeto tem duas partes: uma interface feita com Vue 3 e uma API em Python/FastAPI que recebe os arquivos e realiza as conversões.

## O que dá para fazer

- Converter arquivos para Word, Excel, PDF, JSON, imagem, CSV, YAML, XML ou texto.
- Escolher o destino depois de enviar um arquivo: o ZenConvert identifica a extensão e sugere destinos compatíveis.
- Arrastar arquivos para um card de destino ou para a página.
- Enviar vários arquivos para a mesma conversão, acompanhar o envio e cancelar a operação.
- Baixar os resultados um por um ou, quando houver mais de um, juntos em um arquivo ZIP.
- Consultar as últimas conversões. O histórico fica neste navegador e guarda nomes, formatos, tamanhos e datas — não guarda os arquivos convertidos.
- Alternar entre o tema escuro verde e o tema claro azul e branco. A preferência fica salva neste navegador.

## Formatos disponíveis

Os formatos de origem aceitos dependem do destino. A extensão do arquivo é usada para identificar o formato; arquivos incompatíveis são recusados pela API.

| Destino | Formatos de origem aceitos |
| --- | --- |
| **Word (`.docx`)** | PDF, CSV, TSV, XLSX, XLS, JSON, YAML, XML, TXT, Markdown (`.md`), HTML, PPTX e imagens PNG, JPG/JPEG, WEBP, GIF ou AVIF |
| **Excel (`.xlsx`)** | CSV, TSV, XLS, JSON, YAML, XML e DOCX |
| **PDF (`.pdf`)** | DOC/DOCX, PPT/PPTX, CSV, TSV, XLSX, XLS, JSON, YAML, XML, TXT, Markdown, HTML e imagens PNG, JPG/JPEG, WEBP, GIF ou AVIF |
| **JSON (`.json`)** | CSV, TSV, XLSX, XLS, YAML, XML e DOCX |
| **Imagem** | PDF e imagens PNG, JPG/JPEG, WEBP, GIF ou AVIF. Escolha PNG, JPG ou WEBP como saída. |
| **CSV (`.csv`)** | XLSX, XLS, JSON, YAML, XML e DOCX |
| **YAML (`.yaml`)** | CSV, TSV, XLSX, XLS, JSON, XML e DOCX |
| **XML (`.xml`)** | CSV, TSV, XLSX, XLS, JSON, YAML e DOCX |
| **Texto** | DOCX, PDF, PPTX, HTML, Markdown e TXT. Escolha TXT, Markdown ou HTML como saída. |

O seletor de destino no painel apresenta somente conversões compatíveis com os arquivos enviados. A lista definitiva de formatos aceitos está na API e pode ser consultada em `GET /api/conversoes`.

## Como funciona

1. Escolha um card (por exemplo, **PDF**) ou use o envio universal para escolher o destino depois.
2. Selecione ou arraste os arquivos. O painel mostra as opções disponíveis quando o destino é detectado automaticamente.
3. Para imagem e texto, escolha também o formato de saída.
4. Inicie a conversão, acompanhe o progresso do envio e baixe os arquivos gerados.

O progresso mostrado durante o envio corresponde aos bytes enviados. Depois que o envio termina, a interface informa que a API está processando o arquivo; não há uma porcentagem estimada do processamento no servidor.

## Requisitos

- **Node.js** compatível com a versão declarada em `frontend/package.json` e npm.
- **Python 3.10 ou superior** para o backend.
- **LibreOffice** no servidor para converter DOC/DOCX ou PPT/PPTX em PDF.

PDF para Word usa `pdf2docx`; a fidelidade depende da estrutura e do layout do PDF. PDF para texto precisa de texto selecionável: não há OCR para imagens escaneadas.

## Rodar localmente

Abra dois terminais na pasta do projeto.

### 1. Iniciar a API

No Windows, PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

No macOS ou Linux:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

A API fica em `http://127.0.0.1:8000`. A documentação interativa fica em `http://127.0.0.1:8000/docs`.

### 2. Iniciar o site

```bash
cd frontend
npm install
npm run dev
```

Abra o endereço mostrado pelo Vite (normalmente `http://localhost:5173`). Durante o desenvolvimento, o Vite encaminha as chamadas `/api` para a API local na porta `8000`.

### Gerar a versão de produção do site

```bash
cd frontend
npm run build
```

Os arquivos prontos para publicação são criados em `frontend/dist`. Para testar a versão gerada localmente, use `npm run preview`.

## Configuração

### API

O backend carrega variáveis opcionais de um arquivo `.env` dentro da pasta `backend`:

```env
MAX_UPLOAD_MB=25
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

- `MAX_UPLOAD_MB`: tamanho máximo de cada arquivo enviado, em megabytes. O padrão é `25`.
- `CORS_ORIGINS`: lista de endereços do site separados por vírgula. Em produção, configure o domínio real do frontend.

Não publique arquivos `.env` nem credenciais no repositório.

### Frontend

Opcionalmente, defina `VITE_API_URL` no ambiente de build do frontend com o endereço-base da API, por exemplo:

```env
VITE_API_URL=https://api.exemplo.com
```

Use somente o endereço-base, sem acrescentar `/api`. Se essa variável não estiver definida, a aplicação usa o mesmo domínio da página; em desenvolvimento, o proxy do Vite encaminha a chamada para `localhost:8000`.

## API

As conversões usam `multipart/form-data`, com o arquivo no campo `arquivo`. O resultado é enviado como download.

| Método e caminho | Finalidade |
| --- | --- |
| `GET /api/conversoes` | Lista os destinos, as extensões de origem aceitas e o limite de upload. |
| `POST /api/conversoes/word` | Gera um documento Word (`.docx`). |
| `POST /api/conversoes/excel` | Gera uma planilha Excel (`.xlsx`). |
| `POST /api/conversoes/pdf` | Gera um PDF. |
| `POST /api/conversoes/json` | Gera um arquivo JSON. |
| `POST /api/conversoes/imagem?formato=png\|jpg\|webp` | Converte para imagem. O parâmetro `formato` é opcional e, sem ele, a saída é PNG. |
| `POST /api/conversoes/csv` | Gera um CSV. |
| `POST /api/conversoes/yaml` | Gera um YAML. |
| `POST /api/conversoes/xml` | Gera um XML. |
| `POST /api/conversoes/texto?formato=txt\|md\|html` | Gera texto. O parâmetro `formato` é opcional e, sem ele, a saída é TXT. |

Os erros da API incluem uma mensagem no campo `detail`. Entre os códigos possíveis estão `400` (arquivo vazio), `413` (arquivo acima do limite), `415` (extensão não aceita), `422` (conteúdo inválido) e `503` (serviço externo necessário indisponível).

## Privacidade e limites

- A API não tem conta de usuário, autenticação ou armazenamento de arquivos para download posterior.
- O histórico de conversões fica no `localStorage` do navegador e contém apenas metadados. Limpar os dados do navegador também remove esse histórico.
- Cada arquivo é limitado a 25 MB por padrão. O limite pode ser ajustado com `MAX_UPLOAD_MB`; limites de memória e tempo da hospedagem também se aplicam.
- A conversão de DOC/DOCX ou PPT/PPTX para PDF depende do LibreOffice instalado junto à API.
- PDF para texto funciona apenas com texto selecionável e tem limite de 200 páginas.
- Conversões de HTML e Markdown para texto preservam uma estrutura simples de títulos e parágrafos; não são conversores de layout completo.
- O PDF gerado a partir de texto ou dados usa Helvetica; caracteres fora do conjunto Latin-1 podem não ser exibidos corretamente.
- YAML que use âncoras ou aliases e XML que contenha DTD ou entidades externas são rejeitados.
- Como a API não exige autenticação, não a exponha publicamente sem considerar proteção contra abuso, limites de requisição, monitoramento e políticas de privacidade adequadas.

## Estrutura do projeto

```text
ZenConvert/
├── backend/
│   ├── core/                 # Configurações da API
│   ├── enums/                # Formatos de saída
│   ├── routes/               # Endpoints HTTP
│   ├── schemas/              # Modelos de resposta
│   └── services/conversores/ # Leitura e conversão de arquivos
└── frontend/
    ├── src/components/       # Componentes de interface
    ├── src/composables/      # Estado e lógica reutilizável do Vue
    ├── src/config/           # Cards e formatos de conversão
    ├── src/services/         # Comunicação HTTP com a API
    ├── src/views/            # Painel e página do Design System
    └── src/assets/styles/    # Tokens e estilos globais
```

## Tecnologias

- **Frontend:** Vue 3, Vite, Vue Router, Tailwind CSS, Axios e Lucide.
- **Backend:** Python, FastAPI e Uvicorn.
- **Conversões:** bibliotecas Python para documentos Word, planilhas, PDF, imagens, JSON, CSV, YAML, XML e apresentações.
