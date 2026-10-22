"""Confere que as três versões produzem o mesmo resultado.
Uso: python src/validar.py data/access.log"""
import sys
import analise_seq, analise_threads, analise_processos
from comum import resumo

if __name__ == "__main__":
    caminho = sys.argv[1]
    ref = resumo(analise_seq.analisar(caminho))
    for nome, mod in [("threads", analise_threads), ("processos", analise_processos)]:
        for w in (1, 3, 4):
            r = resumo(mod.analisar(caminho, w))
            assert r == ref, f"{nome} com {w} workers difere da versão sequencial"
    print("OK: as três versões produzem o mesmo resultado.")