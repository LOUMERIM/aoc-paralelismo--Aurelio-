"""Gera results/speedup.png a partir de results/tempos.csv.
Uso: python src/grafico.py --f 0.9 (f = fração paralelizável estimada)
"""
import argparse
import csv
import matplotlib.pyplot as plt

p = argparse.ArgumentParser()
p.add_argument("--f", type=float, default=None, help="fração paralelizável estimada")
a = p.parse_args()

dados = {"threads": [], "processos": []}
with open("results/tempos.csv") as f:
    for r in csv.DictReader(f):
        if r["versao"] in dados:
            dados[r["versao"]].append((int(r["workers"]), float(r["speedup"])))

fig, ax = plt.subplots(figsize=(7, 4.5))
max_w = max(w for serie in dados.values() for w, _ in serie)
ax.plot([1, max_w], [1, max_w], "k--", label="Ideal (S = p)")
for nome, serie in dados.items():
    serie.sort()
    ax.plot([w for w, _ in serie], [s for _, s in serie], "o-",
label=nome.capitalize())
if a.f is not None:
    # TODO: traçar a curva de Amdahl S(p) = 1 / ((1 - f) + f / p) para p = 1..max_w
    pass
ax.set_xlabel("Número de workers (p)")
ax.set_ylabel("Speedup")
ax.set_title("Speedup × workers — análise de 1 milhão de linhas de log")
ax.grid(True, alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig("results/speedup.png", dpi=150)
print("Gravado results/speedup.png")