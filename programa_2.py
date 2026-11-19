from itertools import combinations
from algoritmos import *
n = 6
t = 4

# Inicializa todas as relações com zero
D = {
    (a, b): {c: 0 for c in range(n)}
    for a, b in combinations(range(n), 2)
}

# Define algumas relações proibidas
D[(0, 2)][1] = 1
D[(0, 3)][1] = 1
D[(0, 4)][1] = 1
D[(0, 4)][3] = 1
D[(1, 4)][3] = 1
D[(2, 4)][3] = 1
D[(0, 5)][1] = 1
D[(4, 5)][3] = 1

resultado = encontrar_conjunto(D, n, t)

print("Resultado final:", resultado)

