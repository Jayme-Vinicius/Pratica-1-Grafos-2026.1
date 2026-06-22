import sys

def ler_grafo(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()

        # Linha 0: numero de vértices e arestas
        num_vertices, num_arestas = linhas[0].strip().split("\t")
        num_vertices = int(num_vertices)
        num_arestas = int(num_arestas)

        # Linha 1:: origem (S) e destino (T)
        s, t = linhas[1].strip().split("\t")
        s = int(s)
        t = int(t)

        # Cria o dicionario do grafo
        grafo = {v: [] for v in range(num_vertices)}

        # Lê as linhas de arestas (a partir da linha 2)
        for i in range(2, num_arestas + 2):
            u, v, custo = linhas[i].strip().split("\t")
            u = int(u)
            v = int(v)
            custo = float(custo)
            grafo[u].append((v, custo))

    return grafo, s, t, num_vertices

def menor_nao_visitado(dist, visitado):
    # Encontra o vértice não visitado com a menor distância. Vai retornar None se todos os vértices tiverem sido visitados
    menor_vertice = None
    menor_valor = float('inf')
    for v in dist:
        if not visitado[v] and dist[v] < menor_valor:
            menor_valor = dist[v]
            menor_vertice = v
    return menor_vertice

def dijkstra(grafo, s):
    dist = {v: float('inf') for v in grafo}
    dist[s] = 0
    visitado = {v: False for v in grafo}
    predecessor = {v: None for v in grafo}

    while True:
        v = menor_nao_visitado(dist, visitado)
        if v is None:
            break   # Todos os vértices foram visitados

        visitado[v] = True

        # Relaxamento: tenta melhorar a distância para os vizinhos de v
        for vizinho, custo in grafo[v]:
            nova_dist = dist[v] + custo
            if nova_dist < dist[vizinho]:
                dist[vizinho] = nova_dist
                predecessor[vizinho] = v

    return dist, predecessor

def reconstruir_caminho(predecessor, s, t): # Reconstrói o caminho de s para t usando o dicionário de predecessores
    caminho = []
    atual = t
    while atual is not None:
        caminho.append(atual)
        if atual == s:
            break
        atual = predecessor[atual]
    caminho.reverse()

    # Se o primeiro elemento não for s, significa que não há caminho de s para t
    if caminho[0] != s:
        return None
    return caminho

def bellman_ford(grafo, s, num_vertices):   # Suporta arestas com pesos negativos, mas não suporta ciclos negativos
    dist = {v: float('inf') for v in grafo}
    dist[s] = 0
    predecessor = {v: None for v in grafo}

    # Repete o relaxamento para todas as arestas (num_vertices - 1) vezes
    for _ in range(num_vertices - 1):
        houve_atualizacao = False
        for u in grafo:
            for v, custo in grafo[u]:
                if dist[u] + custo < dist[v]:
                    dist[v] = dist[u] + custo
                    predecessor[v] = u
                    houve_atualizacao = True
        # Se não houve atualização em uma iteração, podemos parar antes do final
        if not houve_atualizacao:
            break

    # Se ainda existir relaxamento possível após (num_vertices - 1) iterações, então há um ciclo negativo
    tem_ciclo_negativo = False
    for u in grafo:
        for v, custo in grafo[u]:
            if dist[u] + custo < dist[v]:
                tem_ciclo_negativo = True
    
    return dist, predecessor, tem_ciclo_negativo

def tem_peso_negativo(grafo):
    for u in grafo:
        for v, custo in grafo[u]:
            if custo < 0:
                return True
    return False

def escrever_saida(caminho_arquivo, algoritmo, justificativa, rota, custo):
    """
    Escreve a saída no formato especificado do professor:
        ALGORITMO: <nome>
        JUSTIFICATIVA: <texto>
        ROTA: <v0> <v1> ... <vn>
        CUSTO: <valor>
    """
    rota_str = " ".join(str(v) for v in rota)

    with open(caminho_arquivo, 'w') as f:
        f.write(f"ALGORITMO: {algoritmo}\n")
        f.write(f"JUSTIFICATIVA: {justificativa}\n")
        f.write(f"ROTA: {rota_str}\n")
        f.write(f"CUSTO: {custo}\n")



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 main.py <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)

    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2]

    grafo, s, t, num_vertices = ler_grafo(arquivo_entrada)

    if not tem_peso_negativo(grafo):
        # Sem pesos negativos, podemos usar Dijkstra
        algoritmo = "Dijkstra"
        justificativa = ("Todos os pesos do grafo são positivos, então o algoritmo de Dijkstra é adequado para encontrar o caminho.\n"
        "Ele é mais eficiente do que o Bellman-Ford para grafos com pesos positivos. E, como precisamos apenas do caminho S -> T, \n"
        "não precisamos de um algoritmo como o Floyd-Warshall, que calcula todos os caminhos entre todos os pares de vértices."
        )
        dist, predecessor = dijkstra(grafo, s)
        caminho = reconstruir_caminho(predecessor, s, t)
        custo = dist[t]

    else:
        # Com pesos negativos, precisamos usar Bellman-Ford
        algoritmo = "Bellman-Ford"
        justificativa = (
            "O grafo contém pesos negativos, o que torna o Dijkstra inadequado. O Floyd-Warshall também suportaria, mas resolveria para todos os pares de vértices, \n"
            "sendo desnecessário para o nosso caso. O Bellman-Ford suporta pesos negativos (sem ciclo negativo) e é mais eficiente que o Floyd-Warshall."
        )
        dist, predecessor, ciclo_neg = bellman_ford(grafo, s, num_vertices)

        if ciclo_neg:
            print("ATENÇÃO: foi detectado um ciclo negativo no grafo. Não é possível encontrar o caminho mínimo.")
            sys.exit(1)

        caminho = reconstruir_caminho(predecessor, s, t)
        custo = dist[t]

    escrever_saida(arquivo_saida, algoritmo, justificativa, caminho, custo)
    print(f"Arquivo {arquivo_saida} gerado com sucesso.")
    print(f"    Algoritmo: {algoritmo}")
    print(f"    Rota: {caminho}")
    print(f"    Custo: {custo}")