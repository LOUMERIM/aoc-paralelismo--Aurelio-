"""Versão 2: ThreadPoolExecutor.
Uso: python src/analise_threads.py data/access.log --workers 4
"""
import argparse
import json
import sys
import time

from concurrent.futures import ThreadPoolExecutor
from comum import dividir_em_blocos, processar_bloco, combinar, resumo

def analisar(caminho: str, workers: int) -> dict:
    blocos = dividir_em_blocos(caminho, workers)
    # TODO: criar um ThreadPoolExecutor com `workers` threads, submeter processar_bloco(caminho, inicio, fim) para cada bloco, recolher os
    # resultados parciais e devolver combinar(parciais). Dica: executor.map ou uma lista de futures + future.result().
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futuros = [executor.submit(processar_bloco, caminho, inicio, fim) for inicio, fim in blocos]
        parciais = [f.result() for f in futuros]
    return combinar(parciais)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("caminho")
    p.add_argument("--workers", type=int, default=4)
    a = p.parse_args()
    t0 = time.perf_counter()
    r = analisar(a.caminho, a.workers)
    print(f"tempo={time.perf_counter() - t0:.3f}s", file=sys.stderr)
    print(json.dumps(resumo(r), indent=1))