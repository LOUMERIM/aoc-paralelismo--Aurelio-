# aoc-paralelismo--Aurelio-
Atividade do dia 22/10 de Arquitetura e Organização de Computadores 2026.2

Como executar:
    python -m venv .venv && source .venv/bin/activate # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    python src/gerar_dados.py
    cd src && python validar.py ../data/access.log && cd ..
    cd src && python benchmark.py ../data/access.log --repeticoes 3 && cd ..
    python src/grafico.py --f 0.9
    Observação: os scripts importam comum como módulo local, por isso o cd src. Alternativa: executar
    com PYTHONPATH=src.

## Perguntas de análise (responder no README)
1. A versão com threads ficou mais rápida que a sequencial? Explique o que é o GIL e por que ele
impede o ganho em tarefas CPU-bound. Em que tipo de tarefa as threads em Python ajudam?
2. Com processos, o speedup com 2 e 4 workers ficou próximo do ideal? Quais overheads (criação
de processos, envio do resultado parcial pelo pickle, agregação no processo principal) explicam a
diferença? Estime o custo de criar os processos medindo o tempo com 1 worker em relação ao
sequencial.
3. O que aconteceu ao usar 8 workers ou cpu_count() em uma máquina com menos núcleos
físicos? Relacione com hyper-threading e com o conceito de escalabilidade forte do livro.
4. Qual fração paralelizável f você estimou? Segundo a Lei de Amdahl, qual seria o speedup
máximo com infinitos núcleos? Que parte do seu programa é inerentemente sequencial?
5. (Opcional) Se o arquivo tivesse 10 milhões de linhas, você esperaria eficiência maior ou menor
com 4 processos? Relacione com escalabilidade fraca.