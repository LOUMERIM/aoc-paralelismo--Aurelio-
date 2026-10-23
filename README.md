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

## Ambiente utilizado

| Componente | Detalhe |
|:--|:--|
| **Sistema operacional** | Bazzite 44 (variante Kinoite, baseado no Fedora 44) |
| **Kernel** | Linux 7.2.9 (`7.2.9-ogc3.1.fc44.x86_64`) |
| **Python** | 3.14.8 |
| **Arquitetura** | x86_64 |
| **Processador** | Intel(R) Core(TM) i5-9300H @ 2,40 GHz (GenuineIntel) |
| **Frequência** | mínima 800 MHz, máxima 4100 MHz |
| **Núcleos / threads** | 4 núcleos físicos, 2 threads por núcleo (hyper-threading), 8 CPUs lógicas, 1 soquete |
| **Identificação da CPU** | família 6, modelo 158, step 10 |
| **BogoMIPS** | 4800,00 |
| **Cache** | L1d 128 KiB (4 × 32 KiB), L2 1 MiB (4 × 256 KiB), L3 8 MiB (compartilhada) |
| **Memória RAM** | ADATA 16 GB (2 × 8 GB), 2666 MHz, CL20 |

## Resultados
Tempos em segundos para analisar 1 milhão de linhas de log (média de 3 repetições). Dados completos em
[results/tabela.md](results/tabela.md) e [results/tempos.csv](results/tempos.csv).

| Versão | Nº de Workers | Tempo Médio | Desvio padrão (s) | Speedup(T_seq / T_par) | Eficiencia(Speedup / workers) |
|:---------|:------:|:--------:|:--------:|:--------:|--------:|
| Sequencial | 1  | 20,69     | 0,54     | 1,00     | 1,00     |
| Threads | 1  | 22,74     | 0,11     | 0,91     | 0,91     |
| Threads | 2  | 30,29     | 1,35     | 0,68     | 0,34     |
| Threads | 4  | 32,74     | 0,24     | 0,63     | 0,16     |
| Threads | 8  | 35,16     | 0,14     | 0,59     | 0,07     |
| Threads | cpu_count = 8  | 35,16     | 0,14     | 0,59     | 0,07     |
| Processos | 1  | 23,06     | 0,09     | 0,90     | 0,90     |
| Processos | 2  | 11,93     | 0,13     | 1,73     | 0,87     |
| Processos | 4  | 6,96     | 0,08     | 2,97     | 0,74     |
| Processos | 8  | 6,84     | 0,02     | 3,02     | 0,38     |
| Processos | cpu_count = 8  | 6,84     | 0,02     | 3,02     | 0,38     |

## Amdahl

Estimativa de f (Lei de Amdahl)

| p | S | f |
|:-:|:-:|:-:|
| 2 | 1,734 | 0,846 |
| 4 | 2,974 | 0,885 |
| 8 | 3,024 | 0,765 |

- Concordam? Sim, entre p = 2 e p = 4: 0,85 e 0,89, e o f caiu menos de 0,04.
- Adotei f ≈ 0,87 (pela média de p = 2 e 4). O speedup máximo com infinitos núcleos seria 1/(1 − f) ≈ 7,5X.
- Com p = 8, o f cai para 0,76. A máquina tem 4 núcleos físicos e 8 lógicos (hyper-threading), então de 4 para 8 workers o speedup mal sobe (2,97 → 3,02). Os 4 workers extras competem pelos mesmos núcleos físicos.

## Perguntas de análise
1. A versão com threads ficou mais rápida que a sequencial? Explique o que é o GIL e por que ele
impede o ganho em tarefas CPU-bound. Em que tipo de tarefa as threads em Python ajudam?

   **Resposta:** Não, ficou mais lenta. A sequencial levou 20,69 s, e as threads levaram 22,74 s com 1 thread, 30,29 s com 2, 32,74 s com 4 e 35,16 s com 8 (speedup de 0,91 a 0,59). Quanto mais threads, pior.
   O GIL (Global Interpreter Lock) é um travamento global do interpretador CPython, ele faz com que só uma thread executa bytecode Python por vez, mesmo com vários núcleos livres. A análise do log é CPU-bound, então a CPU nunca fica ociosa e as threads apenas se revezam no GIL. Não existe execução em paralelo, e ainda se paga o custo de alternar o GIL e de disputá-lo, o que explica a piora com mais threads.
   As threads em Python ajudam em tarefas I/O-bound, porque a thread libera o GIL enquanto espera e outra pode rodar. Também ajudam em código que chama extensões em C que liberam o GIL durante o cálculo.

2. Com processos, o speedup com 2 e 4 workers ficou próximo do ideal? Quais overheads (criação
de processos, envio do resultado parcial pelo pickle, agregação no processo principal) explicam a
diferença? Estime o custo de criar os processos medindo o tempo com 1 worker em relação ao
sequencial.

   **Resposta:** Com 2 workers ficou próximo. O speedup de 1,73 contra 2 ideal (eficiência de 87%). Com 4 workers ficou mais longe: 2,97 contra 4 ideal (eficiência de 74%).
   A diferença vem de partes que não paralelizam ou que custam por processo. a criação dos processos (e a importação dos módulos em cada um), o pickle do resultado parcial (os `Counter` de IPs, endpoints, status e horas) e seu envio ao processo principal, a agregação sequencial em `combinar()` e a divisão em blocos feita antes (`dividir_em_blocos`). Além disso, todos os workers leem o mesmo arquivo do disco e disputam memória e cache. Quanto mais workers, menor o trabalho de cada um e maior o peso relativo desses custos.
   Estimativa do custo de criar os processos: com 1 worker, a versão com processos levou 23,06 s contra 20,69 s da sequencial, ou seja, cerca de **2,37 s a mais (aproximadamente 11,5%)**. Como com 1 worker não há paralelismo nenhum, esse tempo extra é o custo fixo de criação dos processos, do pickle e da agregação.

3. O que aconteceu ao usar 8 workers ou cpu_count() em uma máquina com menos núcleos
físicos? Relacione com hyper-threading e com o conceito de escalabilidade forte do livro.

   **Resposta:** O ganho praticamente sumiu: com 4 workers o tempo foi 6,96 s (speedup 2,97) e com 8 workers foi 6,84 s (speedup 3,02), e a eficiência caiu de 0,74 para 0,38. Nesta máquina `cpu_count()` vale 8 e coincide com a configuração de 8 workers, então são a mesma medição.
   O processador tem 4 núcleos físicos e 8 CPUs lógicas por hyper-threading (2 threads por núcleo). As duas threads de um núcleo dividem as mesmas unidades de execução e as caches L1 e L2, então dois processos CPU-bound no mesmo núcleo físico rendem muito menos que dois núcleos de verdade. O hyper-threading só ajuda a esconder esperas, e aqui a tarefa quase não espera, então os 4 workers extras trouxeram só cerca de 2% de ganho.
   Isso ilustra a escalabilidade forte, pois com o tamanho do problema fixo (1 milhão de linhas), aumentar o número de processadores deveria reduzir o tempo proporcionalmente, mas o ganho satura. Os limites são a fração sequencial (Lei de Amdahl) e os recursos físicos disponíveis.

4. Qual fração paralelizável f você estimou? Segundo a Lei de Amdahl, qual seria o speedup
máximo com infinitos núcleos? Que parte do seu programa é inerentemente sequencial?

   **Resposta:** Estimei f ≈ 0,87, a média de f = 0,846 (p = 2) e f = 0,885 (p = 4), calculados por `f = (1/S − 1) / (1/p − 1)`. O valor de p = 8 (0,765) foi descartado por estar distorcido pelo hyper-threading.
   Pela Lei de Amdahl, o speedup máximo com infinitos núcleos é `1 / (1 − f)`, ou seja, cerca de **7,5X**. Esse é um teto que os 4 núcleos físicos desta máquina nem chegam perto de atingir.
   A parte inerentemente sequencial (cerca de 13% do tempo, com os overheads incluídos) é o que roda só no processo principal: a divisão do arquivo em blocos (`dividir_em_blocos`), a criação do pool de processos, o recebimento e o pickle dos resultados parciais, a agregação em `combinar()` e a montagem do resumo e da saída final.

5. (Opcional) Se o arquivo tivesse 10 milhões de linhas, você esperaria eficiência maior ou menor
com 4 processos? Relacione com escalabilidade fraca.

   **Resposta:** Esperaria eficiência **maior**. Os custos fixos (criação dos processos, divisão em blocos, pickle dos resultados parciais e agregação) não crescem na mesma proporção que o número de linhas, porque dependem mais do número de chaves distintas nos `Counter` do que do total de linhas. Já a parte paralela (regex e `strptime` por linha) cresce cerca de 10 vezes. Assim, a fração paralelizável f aumenta e o speedup com 4 processos chega mais perto de 4.
   Isso se relaciona com a escalabilidade fraca (weak scaling), porque em vez de fixar o tamanho do problema, o trabalho cresce junto com os recursos. Com 10 milhões de linhas e 4 processos, cada processo faz 2,5 milhões de linhas em vez de 250 mil, então o overhead fica diluído e a eficiência sobe. O limite é que a banda de disco e de memória, e o tamanho dos `Counter` (mais IPs distintos), voltam a pesar quando o arquivo cresce muito.
