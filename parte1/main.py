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

if __name__ == "__main__":
    grafo, s, t, num_vertices = ler_grafo("grafo_rede_p.txt")
    print("S:", s, "T:", t)
    print("Grafo:")
    for vertice, vizinhos in grafo.items():
        print(f"    {vertice} -> {vizinhos}")

    dist, predecessor = dijkstra(grafo, s)
    print("\nDistâncias:", dist)
    print("Predecessores:", predecessor)

    caminho = reconstruir_caminho(predecessor, s, t)
    print("\nCaminho minimo:", caminho)
    print("Custo total:", dist[t])