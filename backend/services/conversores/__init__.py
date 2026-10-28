from . import (
    para_csv,
    para_excel,
    para_imagem,
    para_json,
    para_pdf,
    para_texto,
    para_word,
    para_xml,
    para_yaml,
)
from .erros import ConversaoError

ORIGENS_POR_DESTINO = {
    "word": sorted(para_word.ORIGENS),
    "excel": sorted(para_excel.ORIGENS),
    "pdf": sorted(para_pdf.ORIGENS),
    "json": sorted(para_json.ORIGENS),
    "imagem": sorted(para_imagem.ORIGENS),
    "csv": sorted(para_csv.ORIGENS),
    "yaml": sorted(para_yaml.ORIGENS),
    "xml": sorted(para_xml.ORIGENS),
    "texto": sorted(para_texto.ORIGENS),
}

__all__ = [
    "ConversaoError",
    "ORIGENS_POR_DESTINO",
    "para_csv",
    "para_excel",
    "para_imagem",
    "para_json",
    "para_pdf",
    "para_texto",
    "para_word",
    "para_xml",
    "para_yaml",
]
