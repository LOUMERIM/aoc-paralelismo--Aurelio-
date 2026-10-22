"""Funções compartilhadas pelas três versões."""
import re
from collections import Counter
from datetime import datetime

PADRAO = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<data>[^\]]+)\] '
    r'"(?P<metodo>\S+) (?P<endpoint>\S+) [^"]*" '
    r'(?P<status>\d{3}) (?P<bytes>\d+)'
)
FORMATO_DATA = "%d/%b/%Y:%H:%M:%S %z"

def resultado_vazio() -> dict:
    return {
        "por_status": Counter(), # {"200": n, "404": n, ...}
        "bytes_por_endpoint": Counter(), # endpoint sem query string -> bytes
        "por_ip": Counter(), # ip -> requisições
        "por_hora": Counter(), # "00".. "23" -> requisições
        "linhas": 0,
        "invalidas": 0,

    }
def processar_linha(linha: str, acc: dict) -> None:
    """Analisa UMA linha e atualiza o acumulador `acc` no lugar.
    Regras:
    - linha que não casa com PADRAO conta em acc["invalidas"] e é ignorada;
    - a hora vem de datetime.strptime(data, FORMATO_DATA).hour (sim, é lento:
    isso é proposital, torna a tarefa CPU-bound);
    - o endpoint é contado sem a query string (parte após '?'). """
    acc["linhas"] += 1
    m = PADRAO.match(linha)
    if m is None:
        acc["invalidas"] += 1
        return
    # TODO: extrair os campos de `m` e atualizar os quatro Counters.
    raise NotImplementedError


def combinar(parciais: list[dict]) -> dict:
    """Agrega os resultados parciais devolvidos pelos workers em um só."""
    total = resultado_vazio()
    # TODO: somar os Counters e os inteiros de cada parcial em `total`.
    raise NotImplementedError

def resumo(resultado: dict) -> dict:
    """Converte o resultado em algo serializável em JSON (para validar.py)."""
    return {
        "linhas": resultado["linhas"],
        "invalidas": resultado["invalidas"],
        "por_status": dict(sorted(resultado["por_status"].items())),
        "por_hora": dict(sorted(resultado["por_hora"].items())),
        "top10_ips": resultado["por_ip"].most_common(10),
        "top10_endpoints_bytes": resultado["bytes_por_endpoint"].most_common(10),
    }
# ----------------------------------------------------------------------
# Divisão do arquivo em blocos — FORNECIDO, não precisa alterar
# ----------------------------------------------------------------------
def dividir_em_blocos(caminho: str, n: int) -> list[tuple[int, int]]:
    """Devolve n pares (inicio, fim) de deslocamentos em bytes. Cada bloco começa no início de uma linha e termina no fim de outra."""
    import os
    tamanho = os.path.getsize(caminho)
    limites = [0]
    with open(caminho, "rb") as f:
        for i in range(1, n):
            f.seek(i * tamanho // n)
            f.readline() # avança até o próximo '\n'
            limites.append(f.tell())
    limites.append(tamanho)
    return [(limites[i], limites[i + 1]) for i in range(n) if limites[i] < limites[i + 1]]

def processar_bloco(caminho: str, inicio: int, fim: int) -> dict:
    """Lê o intervalo [inicio, fim) do arquivo e processa linha a linha. É a unidade de trabalho de cada worker nas versões paralelas."""
    acc = resultado_vazio()
    with open(caminho, "rb") as f:
        f.seek(inicio)
        while f.tell() < fim:
            linha = f.readline()
            if not linha:
                break
            processar_linha(linha.decode("ascii", errors="replace"), acc)
    return acc