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

if __name__ == "__main__":
    grafo, s, t, num_vertices = ler_grafo("grafo_rede_p.txt")
    print("S:", s, "T:", t)
    print("Grafo:")
    for vertice, vizinhos in grafo.items():
        print(f"    {vertice} -> {vizinhos}")