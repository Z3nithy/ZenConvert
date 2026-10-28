# ZenConvert API

API em **FastAPI** que converte arquivos entre formatos (Word, Excel, PDF, JSON, Imagem, CSV, YAML, XML e Texto). Não há banco de dados nem autenticação: os arquivos são processados em memória.

## Configuração

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Variáveis opcionais em `.env`:

```env
MAX_UPLOAD_MB=25
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Executando

```bash
uvicorn main:app --reload
```

- `http://127.0.0.1:8000/docs`: Swagger
- `http://127.0.0.1:8000/redoc`: ReDoc

## API de conversões

Endpoints sem estado e sem autenticação. Enviam-se os arquivos por `multipart/form-data` no campo `arquivo`; a resposta é o arquivo convertido (download). Limite de upload configurável por `MAX_UPLOAD_MB` (padrão 25) e origens CORS por `CORS_ORIGINS` (padrão: Vite em `localhost:5173`).

| Endpoint | Origens aceitas | Saída |
|---|---|---|
| `GET /api/conversoes` | — | Lista as conversões e o limite de upload |
| `POST /api/conversoes/word` | pdf, csv, tsv, xlsx, xls, json, yaml, xml, txt, md, html, pptx, imagens | `.docx` |
| `POST /api/conversoes/excel` | csv, tsv, json, yaml, xml, xls, docx (primeira tabela) | `.xlsx` |
| `POST /api/conversoes/pdf` | docx, doc*, pptx*, ppt*, csv, tsv, xlsx, xls, json, yaml, xml, txt, md, html, imagens | `.pdf` |
| `POST /api/conversoes/json` | csv, tsv, xlsx, xls, yaml, xml, docx (primeira tabela) | `.json` |
| `POST /api/conversoes/imagem?formato=png\|jpg\|webp` | pdf, imagens | imagem (ou `.zip` se o PDF tiver várias páginas, máx. 50) |
| `POST /api/conversoes/csv` | xlsx, xls, json, yaml, xml, docx (primeira tabela) | `.csv` |
| `POST /api/conversoes/yaml` | csv, tsv, xlsx, xls, json, xml, docx (primeira tabela) | `.yaml` |
| `POST /api/conversoes/xml` | csv, tsv, xlsx, xls, json, yaml, docx (primeira tabela) | `.xml` |
| `POST /api/conversoes/texto?formato=txt\|md\|html` | docx, pdf, pptx, html, md, txt | `.txt`, `.md` ou `.html` |

\* `doc`/`docx`/`ppt`/`pptx` → PDF exige o LibreOffice (`soffice`) no servidor; sem ele a API responde `503`. PDF → Word usa `pdf2docx` (fidelidade depende do layout do PDF).

Limitações: o PDF gerado a partir de texto/dados usa a fonte Helvetica (caracteres fora do Latin-1 não são renderizados); Markdown e HTML são convertidos apenas em títulos e parágrafos; PDF → texto exige texto selecionável (sem OCR, máx. 200 páginas). YAML com âncoras/aliases e XML com DTD/entidades são rejeitados por segurança.

Erros usam `{"detail": "..."}` com `400` (vazio), `413` (acima do limite), `415` (formato não aceito) e `422` (conteúdo inválido).
