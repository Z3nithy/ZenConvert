import io

from openpyxl import Workbook

from .erros import ConversaoError
from .tabular import ler_linhas

MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
ORIGENS = {"csv", "tsv", "json", "docx", "xls", "yaml", "yml", "xml"}


def converter(extensao: str, conteudo: bytes) -> tuple[bytes, str, str]:
    linhas = ler_linhas(extensao, conteudo)
    if not linhas:
        raise ConversaoError("O arquivo não possui dados para converter.")

    planilha = Workbook()
    aba = planilha.active
    aba.title = "Dados"
    for linha in linhas:
        aba.append(linha)
    # Texto iniciado por "=" deve permanecer texto, nunca virar fórmula.
    for linha in aba.iter_rows():
        for celula in linha:
            if isinstance(celula.value, str) and celula.value.startswith("="):
                celula.data_type = "s"

    saida = io.BytesIO()
    planilha.save(saida)
    return saida.getvalue(), MIME, "xlsx"
