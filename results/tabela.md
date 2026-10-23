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
