"""Gera data/access.log com linhas no formato Common Log Format estendido.
Uso: python src/gerar_dados.py [--linhas 1000000] [--seed 42]
"""
import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

ENDPOINTS = ["/", "/produto/{}", "/carrinho", "/busca?q={}", "/api/estoque/{}",
            "/login", "/checkout", "/static/app.js", "/static/style.css"]
STATUS = [200] * 70 + [301] * 5 + [304] * 10 + [404] * 10 + [500] * 3 + [503] * 2
METODOS = ["GET"] * 85 + ["POST"] * 15
AGENTES = ["Mozilla/5.0", "curl/8.4", "Googlebot/2.1", "okhttp/4.12"]

def gerar(caminho: Path, linhas: int, seed: int) -> None:
    rng = random.Random(seed)
    inicio = datetime(2026, 10, 19, 0, 0, 0)
    # 50 IPs "quentes" recebem 30% do tráfego, para que exista um top-10 significativo
    ips_quentes = [f"203.0.113.{rng.randint(1, 254)}" for _ in range(50)]
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="ascii") as f:
        for i in range(linhas):
            if rng.random() < 0.3:
                ip = rng.choice(ips_quentes)
            else:
                ip = f"{rng.randint(1, 223)}.{rng.randint(0, 255)}.{rng.randint(0, 255)}.{rng.randint(1, 254)}" 
            ts = inicio + timedelta(seconds=i * 86400 / linhas)
            endpoint = rng.choice(ENDPOINTS).format(rng.randint(1, 20000))
            status = rng.choice(STATUS)
            tamanho = 0 if status == 304 else rng.randint(200, 50000)
            f.write(
                f'{ip} - - [{ts.strftime("%d/%b/%Y:%H:%M:%S")} +0000] '
                f'"{rng.choice(METODOS)} {endpoint} HTTP/1.1" {status} {tamanho} '
                f'"-" "{rng.choice(AGENTES)}"\n'
            )
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--linhas", type=int, default=1_000_000)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--saida", default="data/access.log")
    a = p.parse_args()
    gerar(Path(a.saida), a.linhas, a.seed)
    print(f"Gerado {a.saida} com {a.linhas} linhas (seed={a.seed}).")