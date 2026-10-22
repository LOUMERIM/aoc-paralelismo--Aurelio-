"""Versão 3: ProcessPoolExecutor.
Uso: python src/analise_processos.py data/access.log --workers 4
"""
import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from comum import dividir_em_blocos, processar_bloco, combinar, resumo

def analisar(caminho: str, workers: int) -> dict:
    blocos = dividir_em_blocos(caminho, workers)
    # TODO: igual à versão com threads, trocando o executor.
    # Atenção: o que é enviado aos processos (argumentos) e o que volta
    # (resultado parcial) precisa ser serializável com pickle.
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futuros = [executor.submit(processar_bloco, caminho, inicio, fim) for inicio, fim in blocos]
        parciais = [f.result() for f in futuros]
    return combinar(parciais)

if __name__ == "__main__":
    # O bloco `if __name__ == "__main__"` é OBRIGATÓRIO com processos no
    # Windows e no macOS (método de início 'spawn'). Sem ele, os processos
    # filhos reimportam o módulo e disparam novos processos sem parar.
    p = argparse.ArgumentParser()
    p.add_argument("caminho")
    p.add_argument("--workers", type=int, default=4)
    a = p.parse_args()
    t0 = time.perf_counter()
    r = analisar(a.caminho, a.workers)
    print(f"tempo={time.perf_counter() - t0:.3f}s", file=sys.stderr)
    print(json.dumps(resumo(r), indent=1))