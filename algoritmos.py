import networkx as nx
from itertools import combinations


from itertools import combinations

def envoltoria_geodesica(S, D):
    H = set(S)

    # Pares que ainda precisam ser processados
    pares = list(combinations(sorted(H), 2))

    while pares:
        a, b = pares.pop()

        # Vértices pertencentes ao intervalo geodético
        for c, valor in D[(a, b)].items():
            if valor == 1 and c not in H:

                # Novos pares formados com o vértice c
                for v in H:
                    pares.append(tuple(sorted((v, c))))

                H.add(c)

    return H


def verificar_independencia_convexa(S, D):
    for v in S:
        restante = set(S) - {v}

        H = envoltoria_geodesica(restante, D)

        if v in H:
            return False, v

    return True, None


def encontrar_conjunto(D, n, t, mostrar=True, mostrar_solucao=True):
    if not 0 <= t <= n:
        raise ValueError("É necessário que 0 <= t <= n")

    S = []

    def buscar(inicio):
        nivel = len(S)
        espaco = "  " * nivel

        # Encontramos um conjunto de tamanho t
        if len(S) == t:
            if mostrar_solucao:
                print(f"{espaco}SOLUÇÃO: {S}")
            return True

        # Não há vértices suficientes para completar S
        if n - inicio < t - len(S):
            return False

        for v in range(inicio, n):
            if mostrar:
                print(f"{espaco}Tentando adicionar {v} em {S}")

            candidato = S + [v]

            valido, conflito = verificar_independencia_convexa(
                candidato, D
            )

            if not valido:
                if mostrar:
                    print(
                        f"{espaco}  Rejeitado: vértice {conflito} "
                        f"pertence à envoltória dos demais"
                    )
                continue

            # Adiciona o vértice
            S.append(v)

            if mostrar:
                print(f"{espaco}  Adicionado: {S}")

            # Continua a busca
            if buscar(v + 1):
                return True

            # Retrocesso
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
