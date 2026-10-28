import csv
import io

from .erros import ConversaoError
from .tabular import ler_linhas

ORIGENS = {"xlsx", "xls", "json", "yaml", "yml", "xml", "docx"}


def _seguro(valor):
    # Evita que planilhas interpretem o texto como fórmula (CSV injection).
    if isinstance(valor, str) and valor[:1] in ("=", "+", "@"):
        return "'" + valor
    return valor


def converter(extensao: str, conteudo: bytes) -> tuple[bytes, str, str]:
    linhas = ler_linhas(extensao, conteudo)
    if not linhas:
        raise ConversaoError("O arquivo não possui dados para converter.")
    saida = io.StringIO(newline="")
    escritor = csv.writer(saida)
    for linha in linhas:
        escritor.writerow([_seguro(v) for v in linha])
    return saida.getvalue().encode("utf-8-sig"), "text/csv; charset=utf-8", "csv"
