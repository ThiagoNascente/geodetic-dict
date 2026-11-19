from libs import *

H = nx.path_graph(5)

G = construir_grafo(H)

GGc = prisma_complementar(G)

GGc = renomear_vertices(GGc)

Gc = gerar_complemento(G)

G = renomear_vertices(G)

Gc = renomear_vertices(Gc)

n = GGc.number_of_nodes()

t = 11 # 15 nao tem

D = construir_dicionario_geodesico(GGc)

S = encontrar_conjunto(D, n, t, False)

print("Conjunto encontrado:", S)

plotar_grafo(G)

plotar_grafo(Gc)