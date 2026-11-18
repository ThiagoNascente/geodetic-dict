from algoritmos import *

G = nx.Graph()

# Defina G

G = renomear_vertices(G)

n = G.number_of_nodes()
t = 3

D = construir_dicionario_geodesico(G)

S = encontrar_conjunto(D, n, t)

print("Conjunto encontrado:", S)