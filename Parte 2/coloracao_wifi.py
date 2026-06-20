"""
Parte 2 - Alocacao de Canais Wi-Fi
==================================
Le um grafo nao-direcionado sem pesos (formato especificado na Pratica1_Grafos.md)
e calcula uma coloracao de vertices que:
  - e valida (nenhum par de vertices adjacentes recebe a mesma cor/canal);
  - usa o menor numero possivel de cores (numero cromatico exato, X(G)).

Estrategia:
  1. DSatur (Degree of Saturation) e usado para CONSTRUIR uma coloracao de boa
     qualidade rapidamente, ordenando os vertices pelo grau de saturacao
     (numero de cores distintas já usadas pelos vizinhos), com empate
     desfeito pelo maior grau no grafo.
  2. Para GARANTIR que o resultado e o otimo (X(G) exato, e nao apenas uma
     boa aproximacao), o programa:
       a) calcula um limite inferior via busca de uma clique no grafo
          (toda clique de tamanho k exige pelo menos k cores);
       b) tenta colorir o grafo com k = limite_inferior, limite_inferior+1, ...
          cores usando backtracking exato (branch and bound), parando no
          primeiro k que admite coloracao valida. Esse k e, por definicao,
          o numero cromatico X(G).
  3. A coloracao final reportada e uma coloracao valida com exatamente X(G)
     cores (a do backtracking exato; se o DSatur já atingiu X(G), usamos a
     do DSatur por ser a que motiva a justificativa do algoritmo).

Uso:
    python3 coloracao_wifi.py <arquivo_entrada> <arquivo_saida>
"""

import sys


def ler_grafo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        linhas = [l for l in f.read().splitlines() if l.strip() != ""]

    n, m = map(int, linhas[0].split())
    adj = [set() for _ in range(n)]
    for i in range(1, 1 + m):
        partes = linhas[i].split()
        u, v = int(partes[0]), int(partes[1])
        adj[u].add(v)
        adj[v].add(u)
    return n, adj


def dsatur(n, adj):
    """Retorna um dict {vertice: cor} (cores comecando em 0) usando DSatur."""
    cor = {}
    cores_vizinhas = [set() for _ in range(n)]
    grau = [len(adj[v]) for v in range(n)]
    nao_colorido = set(range(n))

    while nao_colorido:
        # escolhe vertice com maior grau de saturacao;
        # em caso de empate, escolhe o de maior grau no grafo original
        escolhido = max(
            nao_colorido,
            key=lambda v: (len(cores_vizinhas[v]), grau[v])
        )

        usadas = cores_vizinhas[escolhido]
        c = 0
        while c in usadas:
            c += 1

        cor[escolhido] = c
        nao_colorido.remove(escolhido)
        for viz in adj[escolhido]:
            cores_vizinhas[viz].add(c)

    return cor


def encontrar_clique_lower_bound(n, adj):
    """Heuristica greedy para achar uma clique razoavelmente grande,
    usada como limite inferior para o numero cromatico."""
    ordem = sorted(range(n), key=lambda v: -len(adj[v]))
    melhor_clique = []
    for inicio in ordem:
        clique = [inicio]
        candidatos = set(adj[inicio])
        for v in ordem:
            if v in candidatos:
                if all(v in adj[u] for u in clique):
                    clique.append(v)
                    candidatos &= adj[v]
        if len(clique) > len(melhor_clique):
            melhor_clique = clique
    return len(melhor_clique)


def k_coloravel(n, adj, k):
    """Backtracking exato: tenta colorir o grafo com k cores.
    Retorna a coloracao (dict) se conseguir, ou None caso contrario."""
    ordem = sorted(range(n), key=lambda v: -len(adj[v]))  # heuristica de ordem
    cor = [-1] * n

    def backtrack(idx):
        if idx == n:
            return True
        v = ordem[idx]
        usadas_vizinhas = {cor[u] for u in adj[v] if cor[u] != -1}
        for c in range(k):
            if c not in usadas_vizinhas:
                cor[v] = c
                if backtrack(idx + 1):
                    return True
                cor[v] = -1
        return False

    if backtrack(0):
        return {v: cor[v] for v in range(n)}
    return None


def numero_cromatico_exato(n, adj):
    """Calcula X(G) exato por busca incremental de k, comecando no
    limite inferior dado por uma clique encontrada no grafo."""
    lb = encontrar_clique_lower_bound(n, adj)
    k = max(lb, 1)
    while True:
        resultado = k_coloravel(n, adj, k)
        if resultado is not None:
            return k, resultado
        k += 1


def main():
    entrada, saida = sys.argv[1], sys.argv[2]
    n, adj = ler_grafo(entrada)

    cor_dsatur = dsatur(n, adj)
    num_cores_dsatur = len(set(cor_dsatur.values()))

    x_exato, cor_exata = numero_cromatico_exato(n, adj)

    # Se o DSatur ja atingiu o otimo, usamos sua coloracao (e o algoritmo
    # citado na justificativa). Caso contrario, usamos a coloracao exata
    # encontrada por backtracking, garantindo o numero minimo de cores.
    if num_cores_dsatur == x_exato:
        algoritmo = "DSatur"
        justificativa = (
            "DSatur ordena os vertices pelo grau de saturacao (numero de "
            "cores distintas ja usadas pelos vizinhos), produzindo coloracoes "
            "proximas ao otimo sem busca exaustiva. Neste grafo o resultado "
            "do DSatur coincide com o limite inferior obtido por uma clique, "
            "confirmando que e otimo."
        )
        coloracao_final = cor_dsatur
        k_final = num_cores_dsatur
    else:
        algoritmo = "Backtracking (Branch and Bound)"
        justificativa = (
            "DSatur nao atingiu o limite inferior obtido por clique, entao "
            "foi usado backtracking exato, testando k = limite_inferior, "
            "limite_inferior+1, ... ate achar o menor k para o qual existe "
            "coloracao valida, garantindo o numero cromatico exato."
        )
        coloracao_final = cor_exata
        k_final = x_exato

    # cores comecando em 1
    coloracao_str = " ".join(
        f"{v}={coloracao_final[v] + 1}" for v in range(n)
    )

    with open(saida, "w", encoding="utf-8") as f:
        f.write(f"ALGORITMO: {algoritmo}\n")
        f.write(f"JUSTIFICATIVA: {justificativa}\n")
        f.write(f"NUM_CORES: {k_final}\n")
        f.write(f"COLORACAO: {coloracao_str}\n")

    print(f"[{entrada}] X(G) = {k_final} -> escrito em {saida}")


if __name__ == "__main__":
    main()
