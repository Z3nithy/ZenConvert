from enum import Enum


class FormatoDestino(str, Enum):
    WORD = "word"
    EXCEL = "excel"
    PDF = "pdf"
    JSON = "json"
    IMAGEM = "imagem"
    CSV = "csv"
    YAML = "yaml"
    XML = "xml"
    TEXTO = "texto"


class FormatoImagem(str, Enum):
    PNG = "png"
    JPG = "jpg"
    WEBP = "webp"


class FormatoTexto(str, Enum):
    TXT = "txt"
    MD = "md"
    HTML = "html"
