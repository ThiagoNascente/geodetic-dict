import networkx as nx
from itertools import combinations

def encontrar_conjunto(D, n, t, mostrar=True):
    if not 0 <= t <= n:
        raise ValueError("É necessário que 0 <= t <= n")

    S = []

    def verificar(novo):
        # Verifica os novos trios formados pela inclusão de 'novo'
        for a, b in combinations(S, 2):
            testes = [
                ((a, b), novo),
                ((a, novo), b),
                ((b, novo), a)
            ]

            for par, c in testes:
                par = tuple(sorted(par))
                valor = D[par][c]

                if valor == 1:
                    return (par, c)

        return None

    def buscar(inicio):
        nivel = len(S)
        espaco = "  " * nivel

        # Encontramos um conjunto de tamanho t
        if len(S) == t:
            if mostrar:
                print(f"{espaco}SOLUÇÃO: {S}")
            return True

        # Não existem elementos suficientes para completar S
        if n - inicio < t - len(S):
            return False

        for v in range(inicio, n):
            if mostrar:
                print(f"{espaco}Tentando adicionar {v} em {S}")

            conflito = verificar(v)

            if conflito is not None:
                par, c = conflito
                if mostrar:
                    print(
                        f"{espaco}  Rejeitado: "
                        f"D[{par}][{c}] = 1"
                    )
                continue

            # Adiciona o elemento
            S.append(v)

            if mostrar:
                print(f"{espaco}  Adicionado: {S}")

            # Continua buscando
            if buscar(v + 1):
                return True

            # Retrocede caso não encontre solução
            S.pop()

            if mostrar:
                print(f"{espaco}  Retrocesso: {S}")

        return False

    if buscar(0):
        return S.copy()

    return None


def renomear_vertices(G):
    return nx.convert_node_labels_to_integers(
        G,
        first_label=0,
        ordering="default"
    )


def construir_dicionario_geodesico(G):
    if G.is_directed():
        raise ValueError("O grafo deve ser não direcionado.")

    n = G.number_of_nodes()

    if set(G.nodes()) != set(range(n)):
        raise ValueError("Os vértices devem ser de 0 até n-1.")

    # Calcula as distâncias mínimas entre todos os vértices
    dist = dict(nx.all_pairs_shortest_path_length(G))

    D = {}

    # Percorre todos os pares distintos de vértices
    for a, b in combinations(range(n), 2):
        D[(a, b)] = {}

        distancia_ab = dist[a].get(b)

        for c in range(n):
            # Os extremos nunca são marcados
            if c == a or c == b:
                D[(a, b)][c] = 0
                continue

            # Caso não exista caminho entre a e b
            if distancia_ab is None:
                D[(a, b)][c] = 0
                continue

            distancia_ac = dist[a].get(c)
            distancia_bc = dist[b].get(c)

            if (distancia_ac is not None
                and distancia_bc is not None
                and distancia_ac + distancia_bc == distancia_ab):
                D[(a, b)][c] = 1
            else:
                D[(a, b)][c] = 0

    return D
