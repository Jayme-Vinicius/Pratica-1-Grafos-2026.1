# Comparativo de Algoritmos

## Parte 1 — Roteamento em Rede de Backbone

A tarefa exigia encontrar o caminho de menor custo entre um roteador de origem (S) e um de destino (T), considerando que a rede poderia conter enlaces de custo negativo (SLAs). Três algoritmos foram avaliados:

| Algoritmo | Suporta peso negativo? | Complexidade | Resolve | Quando usar |
|---|---|---|---|---|
| **Dijkstra** | Não | O(V²) nesta implementação (O((V+E)logV) com fila de prioridade) | Origem única → todos os destinos | Grafos sem pesos negativos |
| **Bellman-Ford** | Sim (sem ciclo negativo) | O(V·E) | Origem única → todos os destinos | Grafos com pesos negativos, quando só se precisa de uma origem |
| **Floyd-Warshall** | Sim (sem ciclo negativo) | O(V³) | Todos os pares de vértices | Quando se precisa das distâncias entre todos os pares, não só de uma origem |

### Critério de decisão utilizado

1. **Existe peso negativo no grafo?**
   - Não → **Dijkstra** é o mais eficiente e está apto a resolver o problema sem nenhuma restrição.
   - Sim → Dijkstra é descartado, pois sua corretude depende de pesos não-negativos (ele marca vértices como "definitivos" assim que visitados, o que pode ser invalidado por uma aresta negativa descoberta depois).

2. **Entre Bellman-Ford e Floyd-Warshall, qual escolher quando há peso negativo?**
   - O problema pede apenas o caminho de **uma origem (S) para um destino (T) específico** — não todos os pares de vértices.
   - Floyd-Warshall resolveria corretamente, mas calcula as distâncias entre **todos os pares**, o que é desperdício de processamento para esse caso de uso. Sua complexidade O(V³) também é maior que a do Bellman-Ford O(V·E) em grafos esparsos (poucas arestas em relação ao número de vértices), como os utilizados nesta atividade.
   - Por isso, **Bellman-Ford** foi escolhido: suporta pesos negativos e é mais eficiente que Floyd-Warshall para este caso de origem única.

### Resultados obtidos

| Grafo | Peso negativo? | Algoritmo escolhido | Rota | Custo |
|---|---|---|---|---|
| `grafo_rede_p.txt` | Não | Dijkstra | 0 → 1 → 3 → 4 | 7 |
| `grafo_rede_m.txt` | Sim | Bellman-Ford | 0 → 1 → 2 → 4 → 3 → 6 → 9 | 6 |

### O que aconteceria com a escolha errada?

- Usar **Dijkstra** no grafo médio (`grafo_rede_m.txt`) produziria um resultado **incorreto**, pois o algoritmo fixa a distância de um vértice como definitiva no momento em que o visita, sem considerar que uma aresta negativa descoberta posteriormente poderia reduzir esse valor.
- Usar **Floyd-Warshall** em qualquer um dos dois grafos produziria o resultado **correto**, mas com custo computacional desnecessário, já que calcularia distâncias entre pares de vértices que não são relevantes para o problema (apenas S→T é solicitado).

---

## Parte 2 — Alocação de Canais Wi-Fi

<>

### Algoritmos avaliados

<>


### Critério de decisão utilizado

<>

### Resultados obtidos



### O que aconteceria com a escolha errada?

<>