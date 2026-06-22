# Prática 1 – Grafos: Roteamento e Coloração em Redes

Projeto da disciplina de Teoria dos Grafos. Resolve dois problemas de infraestrutura de redes:

- **Parte 1**: roteamento de menor custo em uma rede de backbone (grafo direcionado com pesos, podendo ter custos negativos).
- **Parte 2**: alocação de canais Wi-Fi em um campus universitário, via coloração de grafos.

## Integrantes

- Thiego Macena Santos — Parte 1 (Roteamento)
- Jayme Vinicius — Parte 2 (Coloração) 

---

## Parte 1 — Roteamento em Rede de Backbone

### Requisitos

- Python 3 (testado com Python 3.10+)
- Nenhuma biblioteca externa é necessária

### Como executar

```bash
cd parte1
python3 main.py <arquivo_entrada> <arquivo_saida>
```

**Exemplos** (usando os arquivos de teste fornecidos):
```bash
python3 main.py grafo_rede_p.txt saida_parte1_p.txt
python3 main.py grafo_rede_m.txt saida_parte1_m.txt
```

O programa lê o grafo, gera o arquivo de saída no formato exigido (`ALGORITMO`, `JUSTIFICATIVA`, `ROTA`, `CUSTO`) e também imprime um resumo no terminal.

### Formato do arquivo de entrada

```
<num_vertices>\t<num_arestas>
<S>\t<T>
<vertice_u>\t<vertice_v>\t<custo>    (repetido para cada aresta)
```
O separador é TAB (`\t`).

### Como o algoritmo é escolhido

O programa lê o grafo e **verifica automaticamente** se existe alguma aresta com custo negativo:

- **Sem peso negativo** → usa **Dijkstra**. É o algoritmo mais eficiente para esse caso (não suporta pesos negativos, mas isso não é um problema aqui).
- **Com peso negativo** → usa **Bellman-Ford**. O Dijkstra deixa de ser válido na presença de pesos negativos. O Floyd-Warshall também resolveria, mas calcula o caminho mínimo entre **todos os pares** de vértices, o que é desnecessário já que só precisamos do caminho S→T — por isso o Bellman-Ford é a escolha mais eficiente entre as opções válidas.

Se for detectado um **ciclo de custo negativo** alcançável a partir da origem, o caminho mínimo não está definido (o custo poderia ser reduzido indefinidamente). Nesse caso, o programa exibe um aviso no terminal e não gera o arquivo de saída.

### Estrutura interna do código (`parte1/main.py`)

| Função | Responsabilidade |
|---|---|
| `ler_grafo` | Lê o arquivo de entrada e monta o grafo como dicionário de listas de adjacência |
| `tem_peso_negativo` | Verifica se existe alguma aresta com custo negativo |
| `dijkstra` | Calcula as distâncias mínimas a partir da origem (grafos sem peso negativo) |
| `bellman_ford` | Calcula as distâncias mínimas a partir da origem, suportando pesos negativos, e detecta ciclos negativos |
| `reconstruir_caminho` | Reconstrói a sequência de vértices do caminho mínimo a partir dos predecessores |
| `escrever_saida` | Gera o arquivo de saída no formato exigido pela atividade |

Mais detalhes de uso rápido em [`parte1/parte1.md`](parte1/parte1.md).

---

## Parte 2 — Alocação de Canais Wi-Fi

<>

### Requisitos

<>

### Como executar

<>

```bash
cd parte2
# 
```

### Formato do arquivo de entrada

```
<>
```

### Algoritmo de coloração utilizado

<>

### Estrutura interna do código

<>

---

## Estrutura do repositório

```
repositorio/
├── README.md
├── parte1/
│   ├── main.py
│   ├── parte1.md
│   ├── grafo_rede_p.txt
│   ├── grafo_rede_m.txt
│   ├── saida_parte1_p.txt
│   └── saida_parte1_m.txt
├── parte2/
│   ├── coloracao_wifi.py
│   ├── saida_parte2_p.txt
│   └── saida_parte2_m.txt
└── comparativo.md
```

## Comparativo

Ver [`comparativo.md`](comparativo.md) para a análise comparativa entre os algoritmos utilizados nas duas partes.
