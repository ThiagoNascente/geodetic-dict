from libs import *

H = nx.path_graph(5)

G = construir_grafo(H)

# Defina G

G = renomear_vertices(G)

n = G.number_of_nodes()
t = 10

D = construir_dicionario_geodesico(G)

S = encontrar_conjunto(D, n, t)

print("Conjunto encontrado:", S)

plotar_grafo(G)
