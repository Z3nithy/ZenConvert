from xml.sax.saxutils import escape

from .erros import ConversaoError
from .texto import Blocos, ler_blocos

ORIGENS = {"docx", "pdf", "pptx", "html", "htm", "md", "txt"}
MIMES = {
    "txt": "text/plain; charset=utf-8",
    "md": "text/markdown; charset=utf-8",
    "html": "text/html; charset=utf-8",
}


def _txt(blocos: Blocos) -> str:
    return "\n\n".join(texto for _, texto in blocos)


def _md(blocos: Blocos) -> str:
    return "\n\n".join(
        f"{'#' * int(tipo[1])} {texto}" if tipo != "p" else texto for tipo, texto in blocos
    )


def _html(blocos: Blocos) -> str:
    corpo = "\n".join(f"  <{tipo}>{escape(texto)}</{tipo}>" for tipo, texto in blocos)
    return (
        '<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"  <title>{escape(blocos[0][1][:80])}</title>\n</head>\n<body>\n{corpo}\n</body>\n</html>\n"
    )


_GERADORES = {"txt": _txt, "md": _md, "html": _html}


def converter(extensao: str, conteudo: bytes, formato: str = "txt") -> tuple[bytes, str, str]:
    if formato not in _GERADORES:
        raise ConversaoError("Formato de texto inválido. Use txt, md ou html.", 422)
    if extensao == formato:
        raise ConversaoError("O arquivo já está neste formato.", 422)
    blocos = ler_blocos(extensao, conteudo)
    return _GERADORES[formato](blocos).encode("utf-8"), MIMES[formato], formato
