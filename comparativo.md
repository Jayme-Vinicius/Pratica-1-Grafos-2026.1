# Comparativo de Algoritmos

## Parte 1 – Roteamento em Rede de Backbone

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

## Parte 2 – Alocação de Canais Wi-Fi

A tarefa exigia atribuir canais (cores) aos pontos de acesso (APs) de uma rede Wi-Fi de forma que nenhum par de APs adjacentes (que se interferem) usasse o mesmo canal, utilizando o **menor número possível de canais** — ou seja, o número cromático exato χ(G) do grafo de interferência. Três algoritmos foram avaliados:

### Algoritmos avaliados

| Algoritmo | Garante χ(G) exato? | Complexidade | Quando usar |
|---|---|---|---|
| **Guloso simples** (ordem arbitrária dos vértices) | Não | O(V + E) | Quando velocidade é prioridade e uma coloração apenas válida (não necessariamente mínima) é aceitável |
| **DSatur** | Não em geral, mas frequentemente atinge o ótimo na prática (sempre ótimo em famílias como grafos bipartidos e cordais) | O(V²) nesta implementação | Quando se quer uma boa aproximação rápida ao ótimo, sem custo exponencial |
| **Backtracking (Branch and Bound)** | Sim, sempre — explora exaustivamente o espaço de cores até provar o mínimo | Exponencial no pior caso, O(kᵛ) | Quando é necessário garantir χ(G) exato e o grafo é pequeno/médio o suficiente para a busca ser viável |

### Critério de decisão utilizado

1. **Obter uma cota inferior para χ(G):** foi feita uma busca heurística por uma clique no grafo. Toda clique de tamanho *k* exige pelo menos *k* cores distintas, pois todos os seus vértices são mutuamente adjacentes. Em ambos os grafos (`grafo_wifi_p.txt` e `grafo_wifi_m.txt`) foi encontrado um triângulo (clique de tamanho 3), logo χ(G) ≥ 3 em ambos os casos.

2. **Executar DSatur para obter uma coloração candidata:** o DSatur ordena dinamicamente os vértices pelo grau de saturação (quantidade de cores distintas já usadas pelos vizinhos), e em caso de empate pelo maior grau no grafo. Essa heurística tende a colorir primeiro os vértices mais "restritos", reduzindo a chance de precisar de cores extras.

3. **Comparar o resultado do DSatur com a cota inferior:**
   - Se o número de cores usado pelo DSatur **for igual** à cota inferior (tamanho da maior clique encontrada), a coloração já é **comprovadamente ótima** — não há necessidade de rodar o backtracking exaustivo, pois não existe coloração válida com menos cores do que o tamanho da clique.
   - Se **for maior**, isso não prova que o DSatur é sub-ótimo, mas também não garante que é ótimo; nesse caso, seria necessário recorrer ao backtracking exato, testando k = cota_inferior, cota_inferior+1, ... até encontrar o menor k para o qual existe coloração válida.
   - Nos dois grafos desta atividade, o DSatur atingiu exatamente 3 cores, igualando a cota inferior da clique — logo, **DSatur foi suficiente** e o backtracking exaustivo não precisou ser executado.

### Resultados obtidos

| Grafo | Clique máxima encontrada | Cota inferior para χ(G) | Algoritmo escolhido | NUM_CORES obtido | Coloração |
|---|---|---|---|---|---|
| `grafo_wifi_p.txt` | 3 (vértices 0, 1, 2) | 3 | DSatur | 3 | `0=1 1=2 2=3 3=1 4=2` |
| `grafo_wifi_m.txt` | 3 (vértices 0, 1, 2) | 3 | DSatur | 3 | `0=1 1=2 2=3 3=1 4=2 5=1 6=2 7=1` |

### O que aconteceria com a escolha errada?

- Usar **Guloso simples** sem nenhuma estratégia de ordenação poderia, dependendo da ordem de visita dos vértices, produzir uma coloração **válida porém sub-ótima** (por exemplo, 4 cores em vez de 3). O resultado continuaria correto no sentido de não violar restrições de adjacência, mas desperdiçaria canais Wi-Fi disponíveis — pela rubrica, isso receberia apenas metade dos pontos do critério de correção.
- Rodar **backtracking exaustivo diretamente, sem antes calcular uma cota inferior por clique**, faria o algoritmo testar k = 1 e k = 2 antes de chegar a k = 3. Como existe um triângulo no grafo, testar k = 2 exigiria explorar boa parte do espaço de busca apenas para provar que nenhuma coloração com 2 cores é possível — um custo computacional evitável, já que a clique encontrada garante de antemão que k ≥ 3.
- Aceitar o resultado do **DSatur sem verificar a cota inferior por clique** seria arriscado em grafos diferentes destes: como o DSatur não garante otimalidade em geral, poderia-se reportar como "mínimo" um número de cores que na verdade não é o χ(G) exato, sem nunca ter essa garantia comprovada formalmente.
