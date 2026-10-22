"""Versão 1: sequencial. Uso: python src/analise_seq.py data/access.log"""
import json
import sys
import time

from comum import resultado_vazio, processar_linha, resumo

def analisar(caminho: str) -> dict:
    acc = resultado_vazio()
    # TODO: abrir o arquivo e chamar processar_linha para cada linha.
    with open(caminho, "rb") as f:
        for linha in f:
            processar_linha(linha.decode("ascii", errors="replace"), acc)
    return acc

if __name__ == "__main__":
    t0 = time.perf_counter()
    r = analisar(sys.argv[1])
    print(f"tempo={time.perf_counter() - t0:.3f}s", file=sys.stderr)
    print(json.dumps(resumo(r), indent=1))