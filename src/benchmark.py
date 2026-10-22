"""Mede as três versões e grava results/tempos.csv.
Uso: python src/benchmark.py data/access.log --repeticoes 3
"""
import argparse
import csv
import os
import statistics
import time
from pathlib import Path
import analise_seq, analise_threads, analise_processos

def medir(func, repeticoes: int, *args) -> tuple[float, float]:
    """Executa func(*args) `repeticoes` vezes e devolve (média, desvio padrão)."""
    tempos = []
    for _ in range(repeticoes):
        # TODO: medir com time.perf_counter() antes e depois de func(*args)
        raise NotImplementedError
    return statistics.mean(tempos), statistics.stdev(tempos)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("caminho")
    p.add_argument("--repeticoes", type=int, default=3)
    a = p.parse_args()
    workers = sorted({1, 2, 4, 8, os.cpu_count()})

    linhas = []
    t_seq, dp = medir(analise_seq.analisar, a.repeticoes, a.caminho)
    linhas.append(["sequencial", 1, t_seq, dp])
    for nome, mod in [("threads", analise_threads), ("processos", analise_processos)]:
        for w in workers:
            # TODO: medir mod.analisar com w workers e acrescentar a linha
            raise NotImplementedError

    Path("results").mkdir(exist_ok=True)
    with open("results/tempos.csv", "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["versao", "workers", "tempo_medio_s", "desvio_padrao_s", "speedup", "eficiencia"])
        for versao, w, t, d in linhas:
            s = t_seq / t
            wr.writerow([versao, w, f"{t:.4f}", f"{d:.4f}", f"{s:.3f}", f"{s / w:.3f}"])
    print("Gravado results/tempos.csv")